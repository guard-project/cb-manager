from colorama import Fore, Style
from datetime import datetime
from pint import UnitRegistry

import configparser
import hashlib
import importlib
import os
import types
import uuid


def subset(elements, *keys, negation=False):
    def match(element):
        if negation:
            return element[0] not in keys
        else:
            return element[0] in keys
    return dict(filter(match, elements.items()))


def copy_func(func, name=None):
    """
    Copy function with a new name.

    :param func: function to copy
    :param name: new name
    :returns: copied function
    """
    return types.FunctionType(func.__code__, func.__globals__, name or func.__name__, func.__defaults__, func.__closure__)


def swagger(**kwrd_params):
    """
    Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def decorator(self):
        kwrd_params['tag'] = self.doc_cls.Index.name
        if self.__name__.endswith('SelectedResource'):
            kwrd_params['docstring'] = 'selected'
        else:
            kwrd_params['docstring'] = 'base'
        kwrd_params['schema'] = self.schema_cls.__name__
        method = kwrd_params['method']
        base_mth = getattr(self, f'on_base_{method}')
        mth = getattr(self, f'on_{method}', None)
        if not callable(mth):
            setattr(self, f'on_{method}', copy_func(
                base_mth, f'on_{method}'))
            mth = getattr(self, f'on_{method}', None)
        with open(f'./api/{kwrd_params.get("docstring")}/{method}.docstring', 'r') as file:
            mth.__doc__ = file.read().format(**kwrd_params)
        setattr(self, 'tag', {'name': kwrd_params.get('tag'),
                              'description': self.schema_cls.__doc__.strip(' \n')})
        return self
    return decorator


def fix_target(prop):
    """
    Fix the field name for ElasticSearch.

    :param prop: field name to fix
    :returns: field name fixed
    """
    return '_id' if prop == 'id' else prop


def generate_password():
    """
    Generate a random password.

    :returns: random password
    """
    return hash(str(uuid.uuid1()))


ureg = UnitRegistry()
Q_ = ureg.Quantity


def get_seconds(text, to_int=False):
    """
    Parse the text to get the equivalent number of seconds (e.g., 1min => 60).

    :params text: input time in human format, e.g.: 1m
    :params to_int: convert to int the result
    :returns: number of seconds
    """
    n = (Q_(text).to(ureg.second)).magnitude
    return int(n) if to_int else n


def str_to_datetime(date_time_str, format='%Y/%m/%d %H:%M:%S'):
    """
    Get a datatime object from the string.

    :params date_time_str: datetime in string
    :params format: datetime format
    :returns datetime object
    """
    return datetime.strptime(date_time_str, format)


def datetime_to_str(date_time=None, format='%Y/%m/%d %H:%M:%S'):
    """
    Convert the datetime to string in the given format.

    :params data_time: datetime input
    :params format: datetime format
    :returns: datetime string in format %Y/%m/%d %H:%M:%S
    """
    if date_time is None:
        date_time = datetime.now()
    return date_time.strftime(format)


def hash(text):
    """
    Make a hash of the text

    :param text: text to make the hash
    :returns: hashed version of the text
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) is list or type(data) is tuple else [data]


class EnvInterpolation(configparser.BasicInterpolation):
    """
    Interpolation which expands environment variables in values.
    """

    def before_get(self, parser, section, option, value, defaults):
        """
        Executes before getting the value.

        :param self: class instance
        :param parser: configparser instance
        :param section: section value
        :param option: option value
        :param value: current value
        :param defaults: default values
        :returns value with expanded variables
        """
        return os.path.expandvars(value)
