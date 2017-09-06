from sleety.errors import SleetyResponseError

def describe_regions(conn):
    res = conn.query('DescribeRegions')

    if res.has_error():
        raise SleetyResponseError()

    return res.dict
