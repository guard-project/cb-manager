from pathlib import Path
from types import FunctionType as Function_Type

from lib.http import HTTP_Method
from utils.sequence import wrap
from utils.string import format


def docstring(ext='docstring', methods=(HTTP_Method.GET, HTTP_Method.POST, HTTP_Method.PUT, HTTP_Method.DELETE)):
    """Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def copy_func(func, name=None):
        """Copy function with a new name.

        :param func: function to copy
        :param name: new name
        :returns: copied function
        """
        return Function_Type(func.__code__, func.__globals__, name or func.__name__,
                             func.__defaults__, func.__closure__)

    def decorator(self):
        if self.__name__.endswith('Selected_Resource'):
            mode = 'selected'
        else:
            mode = 'base'
        for method in wrap(methods):
            base_mth = getattr(self, f'on_base_{method}')
            mth = getattr(self, f'on_{method}', None)
            if not callable(mth):
                setattr(self, f'on_{method}', copy_func(base_mth, f'on_{method}'))
                mth = getattr(self, f'on_{method}', None)
            path = Path(__file__).parent / f'../docstring/{mode}/{method}.{ext}'
            with path.open('r') as file:
                mth.__doc__ = format(file.read(), self=self)
            if self.schema.__doc__ is not None:
                self.tag = {'name': self.doc.Index.name, 'description': self.schema.__doc__.strip(' \n')}
        return self

    return decorator
