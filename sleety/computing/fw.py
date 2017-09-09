from sleety.errors import SleetyResponseError


def describe_fw_groups(conn, params=None):
    res = conn.query('DescribeSecurityGroups', params)

    if res.has_error():
        raise SleetyResponseError()

    return res.dict
