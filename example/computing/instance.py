from __future__ import print_function

import json
import os

from sleety.computing import instance
from sleety.computing.connection import ComputingConnection
from sleety.region import NifcloudRegion


def main():
    access_key = os.environ.get('NIFCLOUD_ACCESS_KEY')
    secret_access_key = os.environ.get('NIFCLOUD_SECRET_ACCESS_KEY')

    east1 = NifcloudRegion('jp-east-1')
    conn = ComputingConnection(access_key, secret_access_key, east1)
    print(json.dumps(instance.describe_instances(conn)))


if __name__ == '__main__':
    main()
