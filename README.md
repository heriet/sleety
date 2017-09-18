# sleety

[![Build Status](https://travis-ci.org/heriet/sleety.svg)](https://travis-ci.org/heriet/sleety)

python SDK for Niftycloud

python >= 2.7 or 3.x

## Installation

```
$ pip install sleety
```

or manual install:

```
$ git clone https://github.com/heriet/sleety
$ cd sleety
$ python setup.py install
```

## Quick Start

```
import os

from sleety.region import NiftyCloudRegion
from sleety.computing import region
from sleety.computing.connection import ComputingConnection

def main():
    access_key = os.environ.get('NIFTYCLOUD_ACCESS_KEY')
    secret_access_key = os.environ.get('NIFTYCLOUD_SECRET_ACCESS_KEY')

    east1 = NiftyCloudRegion('jp-east-1')
    conn = ComputingConnection(access_key, secret_access_key, east1)
    print(region.describe_regions(conn))

if __name__ == '__main__':
    main()
```

## supported service

### computing

* DescribeRegions
* DescribeInstances
* CreateSecurityGroups
* DeleteSecurityGroups
* DescribeSecurityGroups