# -*- coding: utf-8 -*-
"""Tests for the decorators module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import warnings

from prettypyplot import decorators


def test_deprecated():
    """Test deprecated warning."""
    # define function
    kwargs = {'msg': 'msg', 'since': '1.0.0', 'remove': '1.2.0'}

    @decorators.deprecated(**kwargs)
    def func():
        return True

    warning_msg = (
        'Calling deprecated function func. {msg}'.format(**kwargs) +
        ' -- Deprecated since version {since}'.format(**kwargs) +
        ' -- Function will be removed starting from {remove}'.format(**kwargs)
    )

    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            assert func()
        except DeprecationWarning as dw:
            assert str(dw) == warning_msg
        else:
            raise AssertionError()


def test_copy_doc():
    """Test copy doc decorator."""
    docstring = 'This is an example docstring.'

    def func():
        """This is an example docstring."""
        pass

    # test for function
    @decorators.copy_doc(func)
    def functest():
        pass

    assert functest.__doc__ == docstring


def test_copy_doc_params():
    """Test copy doc decorator."""
    # spacing is taken from copied function, this does not to be treated
    # due to help ignoring it anyway
    docstring = """This is another example docstring.

Parameters
        ----------
        var : type
            Var and so on.

        """

    def func():
        """This is an example docstring.

        Some further details.

        Parameters
        ----------
        var : type
            Var and so on.

        """
        pass

    # test for function
    @decorators.copy_doc_params(func)
    def functest():
        """This is another example docstring."""
        pass

    assert functest.__doc__ == docstring
