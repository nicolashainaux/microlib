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

import filecmp
from pathlib import Path
from shutil import copyfile


def pytest_sessionstart(session):
    # Copy the pyproject.toml file to microlib/meta/, if it changed, to make it
    # available on any OS (it is used to retrieve __version__'s value).
    root = Path(__file__).parent.parent
    pp_orig = root / 'pyproject.toml'
    pp_copy = root / 'microlib/meta/pyproject.toml'

    if pp_orig.is_file():
        if not filecmp.cmp(pp_orig, pp_copy, shallow=False):
            print('Update microlib/meta/pyproject.toml')
            copyfile(pp_orig, pp_copy)
        else:
            print('Found pyproject.toml, but no difference with the copy.')
    else:
        print('Cannot find pyproject.toml, skipping its possible update.')
