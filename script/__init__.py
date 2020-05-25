
def read(path, **kwargs):
    with open(f'script/{path}') as f:
        return f.read().format(**kwargs)
    return None
