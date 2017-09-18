def create_fw_group(conn, params=None):
    res = conn.query('CreateSecurityGroup', params)
    return res.dict['return']


def delete_fw_group(conn, params=None):
    res = conn.query('DeleteSecurityGroup', params)
    return res.dict['return']


def describe_fw_groups(conn, params=None):
    res = conn.query('DescribeSecurityGroups', params)
    return res.dict['securityGroupInfo']
