class RegionConnection(object):

    def __init__(self, access_key, secret_access_key, region, path, timeout):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region = region
        self.path = path
        self.timeout = timeout
