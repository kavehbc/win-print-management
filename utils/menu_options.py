def get_dic_keys(dic):
    return list(dic.keys())


def get_dic_code(dic, key):
    return dic.get(key)


def get_dic_index_by_value(dic, value):
    dict_values = list(dic.values())
    return dict_values.index(value)


def get_dic_index_by_key(dic, value):
    dict_keys = list(dic.keys())
    return dict_keys.index(value)
