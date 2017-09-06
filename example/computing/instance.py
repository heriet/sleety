from __future__ import print_function

import os

from sleety.region import NiftyCloudRegion
from sleety.computing import connection, instance


def main():
    access_key = os.environ.get('NIFTYCLOUD_ACCESS_KEY')
    secret_access_key = os.environ.get('NIFTYCLOUD_SECRET_ACCESS_KEY')

    east1 = NiftyCloudRegion('jp-east-1')
    conn_east1 = connection.create_connection(access_key, secret_access_key, east1)
    print(instance.describe_instances(conn_east1))

if __name__ == '__main__':
    main()
