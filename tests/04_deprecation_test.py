# -*- coding: utf-8 -*-

# Microlib is a small collection of useful tools.
# Copyright 2020 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Microlib.

# Microlib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Microlib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Microlib; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import warnings

import pytest

from microlib import Deprecated


@Deprecated()
def f1(*args):
    pass


@Deprecated(use_instead='F1', func_name='fancy_one', removal_version='2.0')
def f2(*args):
    pass


@Deprecated(use_instead='f4', extra_msg='Some more info.',
            ref_url='https://readthedoc.com')
def f3(*args):
    pass


class AnyObject(object):

    def new_func(self, *args):
        return 'Return value of new_func'


def test_calls_to_deprecated_functions():
    with pytest.warns(DeprecationWarning) as record:
        f1()
    assert len(record) == 1
    assert record[0].message.args[0] \
        == 'Call to deprecated function f1. It might be removed in a '\
           'future release.'

    with pytest.warns(DeprecationWarning) as record:
        f2()
    assert len(record) == 1
    assert record[0].message.args[0] \
        == 'Call to deprecated function fancy_one. It will be removed in '\
           'release 2.0. Use F1 instead.'

    with pytest.warns(DeprecationWarning) as record:
        f3()
    assert len(record) == 1
    assert record[0].message.args[0] \
        == 'Call to deprecated function f3. It might be removed in a '\
           'future release. Use f4 instead. Some more info. See '\
           'https://readthedoc.com'


def test_redirect_call_to_removed_function():
    Deprecated.add(AnyObject, AnyObject.new_func, 'old_func')
    Deprecated.add(AnyObject, AnyObject.new_func, 'old_func2',
                   removal_version='3.0', extra_msg='Some more info.',
                   ref_url='https://readthedoc.com')
    obj = AnyObject()

    with pytest.warns(DeprecationWarning) as record:
        ret = obj.old_func()
    assert len(record) == 1
    assert ret == 'Return value of new_func'
    assert record[0].message.args[0] == \
        'Call to deprecated function old_func. It has been removed in a '\
        'previous release. Use new_func instead.'

    with pytest.warns(DeprecationWarning) as record:
        ret = obj.old_func2()
    assert len(record) == 1
    assert ret == 'Return value of new_func'
    assert record[0].message.args[0] == \
        'Call to deprecated function old_func2. It has been removed in '\
        'release 3.0. Use new_func instead. Some more info. See '\
        'https://readthedoc.com'


def test_disable_deprecation_warnings():
    Deprecated.show_warnings = False
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        f1()
