from pathlib import Path
from types import FunctionType as Function_Type

from lib.http import HTTPMethod
from utils.sequence import wrap
from utils.string import formatter


def docstring(ext='docstring', methods=(HTTPMethod.GET, HTTPMethod.POST,
                                        HTTPMethod.PUT, HTTPMethod.DELETE)):
    """Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """

    def copy_func(func, name=None):
        """Copy function with a new name.

        :param func: function to copy
        :param name: new name
        :returns: copied function
        """
        return Function_Type(func.__code__, func.__globals__,
                             name or func.__name__, func.__defaults__,
                             func.__closure__)

    def decorator(self):
        mode = 'selected' if self.__name__.endswith(
            'Selected_Resource') else 'base'
        for method in wrap(methods):
            base_mth = getattr(self, f'on_base_{method}')
            setattr(self, f'on_{method}', copy_func(base_mth, f'on_{method}'))
            mth = getattr(self, f'on_{method}', None)
            path = Path(__file__).parent / \
                f'../docstring/{mode}/{method}.{ext}'
            with path.open('r') as file:
                mth.__doc__ = formatter(file.read(), self=self)
            if self.schema.__doc__ is not None:
                self.tag = {'name': self.doc.Index.name,
                            'description': self.schema.__doc__.strip(' \n')}
        return self

    return decorator
