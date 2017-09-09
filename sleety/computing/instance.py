def describe_instances(conn, params=None):
    res = conn.query('DescribeInstances', params)

    reservations = res.dict['reservationSet']['item']

    if not reservations:
        return []

    instances = reservations[0]['instancesSet']['item']

    return instances
