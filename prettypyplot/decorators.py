"""
Decorators for prettypyplot.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import functools
import warnings


# ~~~ DECORATROS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def copy_doc(source):
    """Copy docstring from source."""
    def wrapper_copy_doc(func):
        if source.__doc__:
            func.__doc__ = source.__doc__
        return func
    return wrapper_copy_doc


def copy_doc_params(source):
    """Copy parameters from docstring source.

    The docstring needs to be formatted according to numpy styleguide.

    .. todo:: Catch if after parameters is further docstring

    """
    def wrapper_copy_doc(func):
        PARAMS_STRING = '\n\n    Parameters'
        doc_source = source.__doc__
        doc_func = func.__doc__
        if doc_source and doc_func and doc_source.find(PARAMS_STRING) != -1:
            doc_params = doc_source[doc_source.find(PARAMS_STRING):]
            func.__doc__ = doc_func + doc_params
        return func
    return wrapper_copy_doc


def deprecated(msg=None, since=None, remove=None):
    """Add deprecated warning."""
    def deprecated_msg(func, msg, since, remove):
        warn_msg = 'Calling deprecated function {0}.'.format(func.__name__)
        if msg:
            warn_msg += ' {0}'.format(msg)
        if since:
            warn_msg += ' -- Deprecated since version {v}.'.format(v=since)
        if remove:
            warn_msg += (' -- Function will be removed starting from {v}.'
                         .format(v=remove))
        return warn_msg

    def decorator_deprecated(func):
        @functools.wraps(func)
        def wrapper_deprecated(*args, **kwargs):
            warnings.warn(deprecated_msg(func, msg, since, remove),
                          category=DeprecationWarning,
                          stacklevel=2)
            return func(*args, **kwargs)
        return wrapper_deprecated
    return decorator_deprecated
