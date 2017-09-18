import time


class RegionConnection(object):

    def __init__(self, access_key, secret_access_key, region, path, timeout, request_interval):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.region = region
        self.path = path
        self.timeout = timeout
        self.request_interval = request_interval

        self.last_request_time = 0

    def wait_interval(self):
        now = time.time()
        diff = now - self.last_request_time

        if diff < self.request_interval:
            time.sleep(self.request_interval - diff)

        self.last_request_time = time.time()
