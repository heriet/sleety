def describe_fw_groups(conn, params=None):
    res = conn.query('DescribeSecurityGroups', params)
    return res.dict['securityGroupInfo']
