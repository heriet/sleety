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
    EndpointFormat = 'computing.{0}.api.cloud.nifty.com'

    @classmethod
    def generate_endpoint(cls, region):
        return ComputingConnection.EndpointFormat.format(region.name)

    def __init__(self, access_key, secret_access_key, region=None, timeout=None, request_interval=0, path='/api/', endpoint=None):
        super(ComputingConnection, self).__init__(access_key, secret_access_key, region, path, timeout, request_interval)

        if not self.region:
            self.region = NiftyCloudRegion(self.DefaultRegionName, is_default=True)

        self.endpoint = endpoint
        if not self.endpoint:
            self.endpoint = self.generate_endpoint(region)

    def send_request(self, action, params=None, method='POST', signature_version='v2'):
        self.wait_interval()

        if signature_version == 'v2':
            sigv2 = SignatureV2(self.access_key, self.secret_access_key, self.endpoint)
            response = sigv2.request(self.path, action, params, method, self.timeout)
            return response
        else:
            # TODO: impl v0, v1
            raise SleetyUnsupportedError('Unsupported sigunature version')

    def query(self, action, params=None, method='POST', signature_version='v2', is_squashed=True):
        response = self.send_request(action, params, method, signature_version)
        cp_res = self._create_response(response)
        cp_res.parse_schema()

        if is_squashed:
            cp_res.squash_dict()

        if cp_res.has_error():
            raise SleetyComputingResponseError(cp_res)

        return cp_res

    def _create_response(self, response):
        return ComputingResponse(response)


class ComputingResponse():

    _ONLY_RETURN_RESPONSES = [
        'CreateSecurityGroupResponse',
        'DeleteSecurityGroupResponse',
    ]

    @staticmethod
    def squash_item_to_list(source):

        if isinstance(source, list):
            return [ComputingResponse.squash_item_to_list(x) for x in source]

        if not isinstance(source, dict):
            return source

        keys = source.keys()
        if len(keys) and list(keys)[0] == 'item' and isinstance(source['item'], list):
            return [ComputingResponse.squash_item_to_list(x) for x in source['item']]

        squashed = {}
        for key, value in source.items():
            if isinstance(value, dict):
                squashed[key] = ComputingResponse.squash_item_to_list(value)
            elif isinstance(value, list):
                squashed[key] = [ComputingResponse.squash_item_to_list(x) for x in value]
            else:
                squashed[key] = value

        return squashed

    def __init__(self, response):
        self.response = response

        self.xml_root = etree.fromstring(response.text.encode('utf-8'))
        self.xml_namespace = self.xml_root.tag[1:].split('}')[0]

        self.dict = None
        self.schema_dir_path = os.path.join(os.path.dirname(__file__), 'schema')

    def parse_schema(self):
        schema_content = self._load_shcema()
        schema = XMLSchema(schema_content)
        self.dict = schema.to_dict(self.xml_root)

        return self.dict

    def _load_shcema(self):
        root_tag = self.xml_root.tag.replace('{{{0}}}'.format(self.xml_namespace), '')
        schema_path = os.path.join(self.schema_dir_path, '{0}.xsd'.format(root_tag))

        if root_tag in self._ONLY_RETURN_RESPONSES:
            schema_path = os.path.join(self.schema_dir_path, '_OnlyReturnResponse.xsd')

        if not os.path.exists(schema_path):
            raise SleetySchemaError('schema not found: {0}'.format(root_tag))

        schema_content = open(schema_path, 'r').read()
        schema_content = schema_content.replace(
            'targetNamespace="https://cp.cloud.nifty.com/api/"',
            'targetNamespace="{0}"'.format(self.xml_namespace))

        if root_tag in self._ONLY_RETURN_RESPONSES:
            schema_content = schema_content.replace('_OnlyReturnResponse', root_tag)

        return schema_content

    def squash_dict(self):
        self.dict = ComputingResponse.squash_item_to_list(self.dict)

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
