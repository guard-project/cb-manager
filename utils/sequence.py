from toolz import valmap


def expand(elements, **kwrds):
    return dict(**elements, **kwrds)


def extract(elements, **kwargs):
    return {key: elements.get(val, None) for key, val in kwargs.items()}


def format(elements, data):
    def frmt(val):
        return val.format(**data)

    def element_map(element):
        return valmap(frmt, element)

    return list(map(element_map, wrap(elements)))


def is_dict(obj):
    return isinstance(obj, dict)


def is_list(obj):
    return isinstance(obj, list)


def iterate(source, *keys):
    """Iterate a nested dict based on list of keys.

    :param source: nested dict
    :param keys: list of keys
    :returns: value
    """
    d = source
    for k in keys:
        if type(d) is list:
            d = d[int(k)]
        elif k not in d:
            d[k] = {}
        else:
            d = d[k]
    return d


def subset(elements, *keys, negation=False):
    def match(element):
        return element[0] not in keys if negation else element[0] in keys

    return dict(filter(match, elements.items()))


def table_to_dict(data, sep=" "):
    keys = data.pop(0).split(sep)
    output = []
    for dr in data:
        vals = dr.split(sep)
        item = dict(zip(keys, vals))
        if item:
            output.append(item)
    return output


def wrap(data):
    """Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) in [list, tuple] else [data]
