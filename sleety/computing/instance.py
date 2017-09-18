def describe_instances(conn, params=None):
    res = conn.query('DescribeInstances', params)
    return res.dict['reservationSet']
