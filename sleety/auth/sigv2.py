import base64
import copy
import hashlib
import hmac

from future.moves.urllib.parse import quote, urlencode
import requests


class SignatureV2:

    def __init__(self, access_key, secret_access_key, endpoint):
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.endpoint = endpoint

    @classmethod
    def calculate_signature(cls, secret_access_key, method, endpoint, path, params):
        payload = ""
        for item in sorted(params.items()):
            payload += '&{0}={1}'.format(item[0], quote(str(item[1]), ''))
        payload = payload[1:]

        string_to_sign = [method, endpoint, path, payload]
        msg = '\n'.join(string_to_sign).encode('utf-8')
        digest = hmac.new(secret_access_key.encode('utf-8'), msg, hashlib.sha256).digest()

        return base64.b64encode(digest)

    def get(self, path, action, params=None, timeout=None):
        self.request(path, action, params, 'GET', timeout)

    def post(self, path, action, params=None, timeout=None):
        self.request(path, action, params, 'POST', timeout)

    def request(self, path, action, params=None, method='POST', timeout=None):
        request_params = copy.deepcopy(params) if params else {}
        request_params['Action'] = action
        request_params['AccessKeyId'] = self.access_key
        request_params['SignatureMethod'] = 'HmacSHA256'
        request_params['SignatureVersion'] = '2'

        request_params['Signature'] = self.calculate_signature(self.secret_access_key, method, self.endpoint, path, request_params)

        if method == 'GET':
            url = 'https://{0}{1}?{2}'.format(self.endpoint, path, urlencode(params))
            response = requests.get(url, timeout=timeout)

        elif method == 'POST':
            url = 'https://{0}{1}'.format(self.endpoint, path)
            response = requests.post(url, urlencode(request_params), timeout=timeout)

        return response
