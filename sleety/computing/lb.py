def describe_load_balancers(conn, params=None):
    res = conn.query('DescribeLoadBalancers', params)
    return res.dict['DescribeLoadBalancersResult']['LoadBalancerDescriptions']
