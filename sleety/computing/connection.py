import os

from lxml import etree
from xmlschema import XMLSchema

from sleety.auth import SignatureV2
from sleety.connection import RegionConnection
from sleety.errors import SleetyUnsupportedError
from sleety.region import NiftyCloudRegion, supply_region_name
from sleety.computing import region as region_api


class ComputingConnection(RegionConnection):

    DefaultRegionName = 'jp-east-1'

    def __init__(self, access_key, secret_access_key, region=None, path='/api/', endpoint=None):
        super(ComputingConnection, self).__init__(
            access_key, secret_access_key, region, path)

        if not self.region:
            self.region = NiftyCloudRegion(self.DefaultRegionName, is_default=True)

        self.endpoint = endpoint
        if not self.endpoint:
            self.endpoint = self.generate_endpoint(region)


    def generate_endpoint(self, region):
        return "computing.{0}.api.cloud.nifty.com".format(region.name)


    def send_request(self, action, params=None, method='POST', signature_version='v2'):
        if signature_version == 'v2':
            sigv2 = SignatureV2(self.access_key, self.secret_access_key, self.endpoint)
            response = sigv2.request(self.path, action, params, method)
            return response
        else:
            # TODO: impl v0, v1
            raise SleetyUnsupportedError('Unsupported sigunature version')


    def query(self, action, params=None, method='POST', signature_version='v2'):
        response = self.send_request(action, params, method, signature_version)
        cp_res = ComputingResponse(response)
        cp_res.parse_schema()
        return cp_res


class ComputingResponse():
    def __init__(self, response):
        self.response = response

        self.xml_root = etree.fromstring(response.text.encode('utf-8'))
        self.xml_namespace = self.xml_root.tag[1:].split('}')[0]

        self.dict = None


    def parse_schema(self):
        root_tag = self.xml_root.tag.replace('{{{0}}}'.format(self.xml_namespace), '')
        schema_path = os.path.join(os.path.dirname(__file__), 'schema', '{0}.xsd'.format(root_tag))

        schema_content = open(schema_path, 'r').read()
        replaced_schema = schema_content.replace(
            'targetNamespace="https://cp.cloud.nifty.com/api/"',
            'targetNamespace="{0}"'.format(self.xml_namespace))

        schema = XMLSchema(replaced_schema)
        parsed = schema.to_dict(self.xml_root)
        self.dict = parsed

        return parsed


    def has_error(self):
        if self.response.status_code != 200:
            print(self.response.status_code)
            return True

        elif self.xml_root.tag == '{{{0}}}ErrorResponse'.format(self.xml_namespace):
            return True

        return False


def create_all_connections(access_key, secret_access_key, default_region=None, path='/api/'):

    first_conn = ComputingConnection(access_key, secret_access_key, default_region)

    res_regions = region_api.describe_regions(first_conn)
    region_info = res_regions['regionInfo']

    conns = []
    for item in region_info:
        is_default = (item['isDefault'] == 'true')
        region_name = supply_region_name(item['regionName'])
        region = NiftyCloudRegion(region_name, is_default)
        conn = ComputingConnection(access_key, secret_access_key, region, path)
        conns.append(conn)

    return conns


def create_connection(access_key, secret_access_key, region=None, path='/api/'):
    return ComputingConnection(access_key, secret_access_key, region, path)
