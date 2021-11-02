import sys


def extract_info(exception):
    try:
        reason = eval(str(exception))
    except Exception:
        reason = str(exception)
    output = {'reason': reason}
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if exc_tb:
        filename = exc_tb.tb_frame.f_code.co_filename
        output.update(filename=filename, line=exc_tb.tb_lineno)
    return output


def to_str(exception):
    info = extract_info(exception)
    reason = info["reason"]
    filename = info.get('filename', None)
    line = info.get('line', None)
    if filename and line:
        return f'{reason} on filename:{filename} at line:{line}'
    else:
        return reason
