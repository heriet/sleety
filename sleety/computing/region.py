from sleety.computing.connection import ComputingConnection
from sleety.region import NiftyCloudRegion


def describe_regions(conn, params=None):
    res = conn.query('DescribeRegions', params)
    return res.dict['regionInfo']


def create_all_region_connections(access_key, secret_access_key, default_region=None, path='/api/'):
    first_conn = ComputingConnection(access_key, secret_access_key, default_region)
    regions = describe_regions(first_conn)

    conns = []
    for item in regions:
        is_default = (item['isDefault'] == 'true')
        region_name = NiftyCloudRegion.correct_region_name(item['regionName'])
        region = NiftyCloudRegion(region_name, is_default)

        conn = ComputingConnection(access_key, secret_access_key, region, path)
        conns.append(conn)

    return conns
