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

from decimal import Decimal

import pytest

from microlib import rotate, grouper, read_text
from microlib import fracdigits_nb, turn_to_capwords


def test_rotate():
    assert rotate([1, 2, 3, 4]) == [4, 1, 2, 3]
    assert rotate([1, 2, 3, 4], -1) == [2, 3, 4, 1]
    assert rotate([1, 2, 3, 4], 3) == [2, 3, 4, 1]


def test_grouper():
    assert list(grouper('abcdefg', 3, 'x')) \
        == [('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'x', 'x')]
    assert list(grouper('abcdefg', 4)) \
        == [('a', 'b', 'c', 'd'), ('e', 'f', 'g', None)]


def test_read_text(fs):
    fs.create_file('file1.txt', contents='ABC')
    fs.create_file('file2.txt', contents='DEF')
    with pytest.warns(DeprecationWarning):
        assert read_text('file1.txt', 'file2.txt') == 'ABC\nDEF'


def test_fracdigits_nb():
    assert fracdigits_nb(Decimal('1')) == 0
    assert fracdigits_nb(Decimal('1.0')) == 1
    assert fracdigits_nb(Decimal('1.2')) == 1
    assert fracdigits_nb(Decimal('1.23')) == 2
    assert fracdigits_nb(Decimal('1.236')) == 3


def test_turn_to_capwords():
    assert turn_to_capwords('abc_def') == 'AbcDef'
    assert turn_to_capwords('GhI_kLm') == 'GhiKlm'
