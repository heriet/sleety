import os

from lxml import etree

from sleety.auth import SignatureV2
from sleety.computing.error import SleetyComputingResponseError
from sleety.connection import RegionConnection
from sleety.error import SleetySchemaError, SleetyUnsupportedError
from sleety.region import NiftyCloudRegion

from xmlschema import XMLSchema


class ComputingConnection(RegionConnection):

    DefaultRegionName = 'jp-east-1'

    @classmethod
    def generate_endpoint(cls, region):
        return "computing.{0}.api.cloud.nifty.com".format(region.name)

    def __init__(self, access_key, secret_access_key, region=None, timeout=None, path='/api/', endpoint=None):
        super(ComputingConnection, self).__init__(access_key, secret_access_key, region, path, timeout)

        if not self.region:
            self.region = NiftyCloudRegion(self.DefaultRegionName, is_default=True)

        self.endpoint = endpoint
        if not self.endpoint:
            self.endpoint = self.generate_endpoint(region)

    def send_request(self, action, params=None, method='POST', signature_version='v2'):
        if signature_version == 'v2':
            sigv2 = SignatureV2(self.access_key, self.secret_access_key, self.endpoint)
            response = sigv2.request(self.path, action, params, method, self.timeout)
            return response
        else:
            # TODO: impl v0, v1
            raise SleetyUnsupportedError('Unsupported sigunature version')

    def query(self, action, params=None, method='POST', signature_version='v2'):
        response = self.send_request(action, params, method, signature_version)
        cp_res = ComputingResponse(response)
        cp_res.parse_schema()

        if cp_res.has_error():
            raise SleetyComputingResponseError(cp_res)

        return cp_res


class ComputingResponse():

    def __init__(self, response):
        self.response = response

        self.xml_root = etree.fromstring(response.text.encode('utf-8'))
        self.xml_namespace = self.xml_root.tag[1:].split('}')[0]

        self.dict = None
        self.schema_dir_path = os.path.join(os.path.dirname(__file__), 'schema')

    def parse_schema(self):
        root_tag = self.xml_root.tag.replace('{{{0}}}'.format(self.xml_namespace), '')
        schema_path = os.path.join(self.schema_dir_path, '{0}.xsd'.format(root_tag))

        if not os.path.exists(schema_path):
            raise SleetySchemaError('schema not found: {0}'.format(root_tag))

        schema_content = open(schema_path, 'r').read()
        replaced_schema = schema_content.replace('targetNamespace="https://cp.cloud.nifty.com/api/"', 'targetNamespace="{0}"'.format(self.xml_namespace))

        schema = XMLSchema(replaced_schema)
        self.dict = schema.to_dict(self.xml_root)

        return self.dict

    def has_error(self):
        if self.response.status_code != 200:
            print(self.response.status_code)
            return True

        elif self.xml_root.tag == self.format_tag('Response') \
                and self.xml_root.find(self.format_tag('Error')):
            return True

        return False

    def format_tag(self, tag_name):
        return '{{{0}}}{1}'.format(self.xml_namespace, tag_name)
