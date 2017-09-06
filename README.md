# sleety

WIP

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
import sleety

from sleety.region import NiftyCloudRegion
from sleety.computing import connection, instance

access_key = 'XXXXXXXXXXXX'
secret_access_key = 'YYYYYYYYYYY'

east1 = NiftyCloudRegion('jp-east-1')
conn_east1 = connection.make_region_connection(access_key, secret_access_key, east1)
print(instance.describe_instances(conn_east1))
```

## supported service

### computing

* DescribeRegions
