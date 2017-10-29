import copy


def remove_request_id(res_dict):
    d = copy.deepcopy(res_dict)
    d.pop('requestId')
    return d
