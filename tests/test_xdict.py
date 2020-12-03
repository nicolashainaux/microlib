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

from microlib import XDict


def test_recursive_update():
    d = XDict({'a': 1, 'b': {'a': 7, 'c': 10}})
    d.recursive_update({'a': 24, 'd': 13, 'b': {'c': 100}})
    assert d == {'a': 24, 'd': 13, 'b': {'a': 7, 'c': 100}}
    d = XDict()
    d.recursive_update({'d': {'f': 13}})
    assert d == {'d': {'f': 13}}
    d = XDict({'a': 1, 'b': {'a': 7, 'c': 10}})
    d.recursive_update({'h': {'z': 49}})
    assert d == {'a': 1, 'b': {'a': 7, 'c': 10}, 'h': {'z': 49}}


def test_flat():
    d = XDict({'a': {'a1': 3, 'a2': {'z': 5}}, 'b': 'data'})
    assert d.flat() == {'a.a1': 3, 'a.a2.z': 5, 'b': 'data'}
