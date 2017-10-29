from nose.tools import eq_

from sleety.computing.connection import ComputingResponse


class TestComputingResponse:

    def test_squash_list_element(self):
        source = {
            'requestId': 'aaa',
            'reservationSet': {
                'item': [
                    {
                        'productCodes': {
                            'item': [],
                        },
                    },
                    {
                        'productCodes': {
                            'member': [
                                {'productCode': None}
                            ],
                        },
                    },
                ],
            },
        }
        actual = ComputingResponse.squash_list_element(source)
        expected = {
            'requestId': 'aaa',
            'reservationSet': [
                {
                    'productCodes': []
                },
                {
                    'productCodes': [
                            {'productCode': None}
                        ],
                },
            ],
        }

        eq_(actual, expected)
