from nose.tools import eq_

from sleety.computing.connection import ComputingResponse


class TestComputingResponse:

    def test_squash_item_to_list(self):
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
                            'item': [
                                {'productCode': None}
                            ],
                        },
                    },
                ],
            },
        }
        actual = ComputingResponse.squash_item_to_list(source)
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
