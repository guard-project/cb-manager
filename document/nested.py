from script import read as script_read


def __filter(data, op, def_op='edit'):
    return list(filter(lambda d: d.get('__op', def_op) == op, data))


def __update(obj, data, op, field):
    if len(data) > 0:
        return obj.update(script=script_read(f'nested_field/{op}.pl', nested_field=field), data=data)
    else:
        return 'noop'


def edit(obj, data, field, def_op='edit'):
    return __update(obj, data=__filter(data, op='edit'), op='edit', field=field)


def rm(obj, data, field, def_op='edit'):
    return __update(obj, data=list(map(lambda d: d['id'], __filter(data, op='rm'))), op='rm', field=field)
