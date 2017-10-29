from sleety.utils.response import remove_request_id


def attach_volume(conn, params=None):
    res = conn.query('AttachVolume', params)
    return remove_request_id(res.dict)


def create_volume(conn, params=None):
    res = conn.query('CreateVolume', params)
    return remove_request_id(res.dict)


def delete_volume(conn, params=None):
    res = conn.query('DeleteVolume', params)
    return res.dict['return']


def describe_volumes(conn, params=None):
    res = conn.query('DescribeVolumes', params)
    return res.dict['volumeSet']


def detach_volume(conn, params=None):
    res = conn.query('DetachVolume', params)
    return remove_request_id(res.dict)


def modify_volume_attribute(conn, params=None):
    res = conn.query('ModifyVolumeAttribute', params)
    return res.dict['return']
