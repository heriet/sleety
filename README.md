# sleety

[![Build Status](https://travis-ci.org/heriet/sleety.svg)](https://travis-ci.org/heriet/sleety)

python SDK for NIFCLOUD

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

from sleety.computing import region
from sleety.computing.connection import ComputingConnection
from sleety.region import NifcloudRegion


def main():
    access_key = os.environ.get('NIFCLOUD_ACCESS_KEY')
    secret_access_key = os.environ.get('NIFCLOUD_SECRET_ACCESS_KEY')

    east1 = NifcloudRegion('jp-east-1')
    conn = ComputingConnection(access_key, secret_access_key, east1)
    print(region.describe_regions(conn))

if __name__ == '__main__':
    main()
```

## supported service

### computing

- region
  - describe_regions
- instance
  - describe_instances
- fw
  - create_security_groups
  - delete_security_groups
  - describe_security_groups
- disk
  - attach_volume
  - create_volume
  - delete_volume
  - describe_volumes
  - detach_volume
  - modify_volume_attribute
- lb
  - describe_lb