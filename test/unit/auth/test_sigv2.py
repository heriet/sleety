from nose.tools import eq_

from sleety.auth import SignatureV2


class TestSignatureV2:

    def test_calculate_signature(self):
        # see http://cloud.nifty.com/api/rest/authenticate.htm
        params = {}
        params['Action'] = 'DescribeImages'
        params['AccessKeyId'] = 'AKIAIZXJ5ZDCD7NZ73XQ'
        params['SignatureMethod'] = 'HmacSHA256'
        params['SignatureVersion'] = '2'

        secret_access_key = 'AAAAAAAAAAAAAAAAAAAAAAAAAA'
        endpoint = 'cp.cloud.nifty.com'
        path = '/api/services/NiftyCloud/'
        actual = SignatureV2.calculate_signature(secret_access_key, 'GET', endpoint, path, params)

        eq_(actual, b'lWD2/WxeLucO71mW3uoJH2Agd5tT8ZiBb1kXpZmP44w=')
