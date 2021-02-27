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

import json
from pathlib import Path
from io import TextIOBase

import pytest

from microlib import XDict, StandardConfigFile


def test_init(mocker):
    mock_os_environ_get = mocker.patch('os.environ.get')
    mock_os_environ_get.return_value = None
    mock_pathlib_Path_home = mocker.patch('pathlib.Path.home')
    mock_pathlib_Path_home.return_value = Path('/home/user1/')

    cfg = StandardConfigFile('myapp')
    assert cfg._fmt == json
    assert cfg.fullpath == Path('/home/user1/.config/myapp/myapp.json')

    mock_os_environ_get.return_value = Path('/home/user2/conf')

    cfg = StandardConfigFile('app')
    assert cfg.fullpath == Path('/home/user2/conf/app/app.json')
    assert cfg._default_config_file == \
        Path(__file__).parent.parent / 'microlib' \
        / 'data/empty_default_config.json'

    cfg2 = StandardConfigFile('app2', default_config_dir='/defaultconfig/dir/')
    assert cfg2._firstrun_dialog() == cfg._default_firstrun_dialog()
    assert cfg2._default_config_file == Path('/defaultconfig/dir/app2.json')

    with pytest.raises(TypeError) as excinfo:
        StandardConfigFile('app3', firstrun_dialog='not_callable')
    assert str(excinfo.value) == \
        'Argument \'firstrun_dialog\' must be a callable.'


def test_create_user_config_file(mocker):
    mock_path_exists = mocker.patch('pathlib.Path.exists')
    mock_path_exists.return_value = False
    mock_path_mkdir = mocker.patch('pathlib.Path.mkdir')
    mock_shutil_copyfile = mocker.patch('shutil.copyfile')
    cfg = StandardConfigFile('myapp')
    cfg._create_user_config_file()
    mock_path_mkdir.assert_called()
    mock_shutil_copyfile.assert_called()


def test_from(mocker):
    content = """language = 'en_US'
enable_devtools = false
show_toolbar_labels = true"""
    expected = {'language': 'en_US', 'enable_devtools': False,
                'show_toolbar_labels': True}

    def firstrun():
        return {'language': 'fr_FR', 'enable_devtools': False,
                'show_toolbar_labels': True}

    m = mocker.patch('builtins.open', mocker.mock_open(read_data=content))
    cfg = StandardConfigFile('myapp', firstrun_dialog=firstrun,
                             fileformat='toml')
    assert cfg._from('dummy.toml') == expected

    m.side_effect = FileNotFoundError
    mocker.patch('microlib.configfile.StandardConfigFile'
                 '._create_user_config_file')
    assert cfg._from('nonexistent.json', ioerror_handling='firstrun_dialog') \
        == firstrun()

    with pytest.raises(FileNotFoundError):
        cfg._from('nonexistent.json')


def test_load(mocker):
    data = XDict({'language': 'en_US', 'enable_devtools': False,
                  'show_toolbar_labels': True})
    userdata = XDict({'language': 'fr_FR'})
    mock_from = mocker.patch('microlib.configfile.StandardConfigFile._from')
    mock_from.side_effect = [data, userdata]
    cfg = StandardConfigFile('myapp')
    assert cfg.load() == {'language': 'fr_FR', 'enable_devtools': False,
                          'show_toolbar_labels': True}


def test_save(mocker):
    # We will update only key2's value.
    data = XDict({'key1': 'value1', 'key2': False, 'key3': 10})
    updated = XDict({'key1': 'value1', 'key2': True, 'key3': 10})
    mock_from = mocker.patch('microlib.configfile.StandardConfigFile._from')
    mock_from.return_value = data
    mock_file_object = mocker.MagicMock(spec=TextIOBase)
    m = mocker.mock_open()
    m.return_value = mock_file_object
    mock_dump = mocker.patch('json.dump')
    cfg = StandardConfigFile('myapp')
    cfg.save({'key2': True})
    assert mock_dump.call_args.args[0] == updated
