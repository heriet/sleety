from sleety.errors import SleetyResponseError

def describe_instances(conn, params=None):
    res = conn.query('DescribeInstances', params)

    if res.has_error():
        raise SleetyResponseError()

    return res.dict
