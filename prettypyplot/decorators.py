"""Decorators for prettypyplot.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import functools
import warnings


# ~~~ DECORATROS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def copy_doc(source):
    """Copy docstring from source."""
    def wrapper_copy_doc(func):
        if source.__doc__:
            func.__doc__ = source.__doc__  # noqa: WPS125
        return func
    return wrapper_copy_doc


def copy_doc_params(source):
    """Copy parameters from docstring source.

    The docstring needs to be formatted according to numpy styleguide.

    .. todo:: Catch if after parameters is further docstring

    """
    def wrapper_copy_doc(func):
        PARAMS_STRING = 'Parameters'
        doc_source = source.__doc__
        doc_func = func.__doc__
        if doc_source and doc_func and doc_source.find(PARAMS_STRING) != -1:
            # find last \n before keyphrase
            idx = doc_source[:doc_source.find(PARAMS_STRING)].rfind('\n')
            doc_params = doc_source[idx:]

            doc_params = doc_source[doc_source.find(PARAMS_STRING):]
            func.__doc__ = '{0}\n\n{1}'.format(  # noqa: WPS125
                doc_func.rstrip(),  # ensure that doc_func ends on empty line
                doc_params,
            )
        return func
    return wrapper_copy_doc


def deprecated(msg=None, since=None, remove=None):
    """Add deprecated warning.

    Parameters
    ----------
    msg : str
        Message of deprecated warning.

    since : str
        Version since deprecated, e.g. '1.0.2'

    remove : str
        Version this function will be removed, e.g. '0.14.2'

    Returns
    -------
    f : function
        Return decorated function.

    Examples
    --------
    >>> @deprecated(msg='Use lag_time instead.', remove='1.0.0')
    >>> def lagtime(args):
    ...     pass  # function goes here
    # If function is called, you will get warning
    >>> lagtime(...)
    Calling deprecated function lagtime. Use lag_time instead.
    -- Function will be removed starting from 1.0.0

    """
    def deprecated_msg(func, msg, since, remove):
        warn_msg = 'Calling deprecated function {0}.'.format(func.__name__)
        if msg:
            warn_msg += ' {0}'.format(msg)
        if since:
            warn_msg += ' -- Deprecated since version {v}'.format(v=since)
        if remove:
            warn_msg += (
                ' -- Function will be removed starting from ' +
                '{v}'.format(v=remove)
            )
        return warn_msg

    def decorator_deprecated(func):
        @functools.wraps(func)
        def wrapper_deprecated(*args, **kwargs):
            warnings.warn(
                deprecated_msg(func, msg, since, remove),
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)  # pragma: no cover

        return wrapper_deprecated

    return decorator_deprecated
