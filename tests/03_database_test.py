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

import sqlite3
from pathlib import Path

import pytest

from microlib.database import ContextManager, Operator, intspan2sqllist
from microlib.database import Ts_Operator

TESTDB_PATH = Path(__file__).parent / 'data/test.db'
TESTDB_TS_PATH = Path(__file__).parent / 'data/test_with_ts.db'


def test_intspan2sqllist():
    assert intspan2sqllist('1-3,14,29,92-97') == \
        '(1, 2, 3, 14, 29, 92, 93, 94, 95, 96, 97)'


def test_ContextManager():
    with ContextManager(':memory:') as cursor:
        cmd = """CREATE TABLE test1
                 (id INTEGER PRIMARY KEY, col1 INTEGER, col2 INTEGER)"""
        cursor.execute(cmd)
    # Check that, out of the with statement, the connection is *closed*
    # (not only committed)
    with pytest.raises(sqlite3.ProgrammingError) as excinfo:
        cursor.execute('SELECT 1 FROM test1;')
    assert str(excinfo.value) == 'Cannot operate on a closed database.'


def test_list_tables():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db.list_tables() == ['table1', 'table2']


def test_table_exists():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db.table_exists('table1')
        assert not db.table_exists('TABLE1')


def test_assert_table_exists():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db._assert_table_exists('table1')
        with pytest.raises(ValueError) as excinfo:
            db._assert_table_exists('table4')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table4"'


def test_assert_row_exists():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db._assert_row_exists('table1', 1)
        with pytest.raises(ValueError) as excinfo:
            db._assert_row_exists('table1', 10)
        assert str(excinfo.value) == \
            'In database, cannot find a row number 10 in table "table1"'


def test_get_cols():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db.get_cols('table1') == ['col1', 'col2']
        assert db.get_cols('table2') == ['col1', 'col2', 'col3']
        assert db.get_cols('table1', include_id=True) == ['id', 'col1', 'col2']
        assert db.get_cols('table2', include_id=True) == ['id', 'col1', 'col2',
                                                          'col3']


def test_get_cols_TS():
    with ContextManager(TESTDB_TS_PATH) as cursor:
        db = Ts_Operator(cursor)
        assert db.get_cols('table1') == ['col1', 'col2']
        assert db.get_cols('table2') == ['col1', 'col2', 'col3']
        assert db.get_cols('table1', include_id=True) == ['id', 'col1', 'col2']
        assert db.get_cols('table2', include_id=True) == ['id', 'col1', 'col2',
                                                          'col3']


def test_get_rows_nb():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db.get_rows_nb('table1') == 4


def test_get_table():
    with ContextManager(TESTDB_PATH) as cursor:
        db = Operator(cursor)
        assert db.get_table('table2') \
            == [('1', 'begin', 'began, begun', 'commencer'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('3', 'do', 'did, done', 'faire'),
                ('4', 'give', 'gave, given', 'donner')]
        assert db.get_table('table2', include_headers=True) \
            == [('id', 'col1', 'col2', 'col3'),
                ('1', 'begin', 'began, begun', 'commencer'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('3', 'do', 'did, done', 'faire'),
                ('4', 'give', 'gave, given', 'donner')]
        with pytest.raises(ValueError) as excinfo:
            db.get_table('table3')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.get_table('table1', sort=3)
        assert str(excinfo.value) == \
            'In database, cannot find a column number 3 in table "table1"'
        assert db.get_table('table2', include_headers=True, sort=3) \
            == [('id', 'col1', 'col2', 'col3'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('1', 'begin', 'began, begun', 'commencer'),
                ('4', 'give', 'gave, given', 'donner'),
                ('3', 'do', 'did, done', 'faire')]


def test_get_table_TS():
    with ContextManager(TESTDB_TS_PATH) as cursor:
        db = Ts_Operator(cursor)
        assert db.get_table('table2') \
            == [('1', 'begin', 'began, begun', 'commencer'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('3', 'do', 'did, done', 'faire'),
                ('4', 'give', 'gave, given', 'donner')]
        assert db.get_table('table2', include_headers=True) \
            == [('id', 'col1', 'col2', 'col3'),
                ('1', 'begin', 'began, begun', 'commencer'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('3', 'do', 'did, done', 'faire'),
                ('4', 'give', 'gave, given', 'donner')]
        with pytest.raises(ValueError) as excinfo:
            db.get_table('table3')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.get_table('table1', sort=3)
        assert str(excinfo.value) == \
            'In database, cannot find a column number 3 in table "table1"'
        assert db.get_table('table2', include_headers=True, sort=3) \
            == [('id', 'col1', 'col2', 'col3'),
                ('2', 'break', 'broke, broken', 'casser'),
                ('1', 'begin', 'began, begun', 'commencer'),
                ('4', 'give', 'gave, given', 'donner'),
                ('3', 'do', 'did, done', 'faire')]


def test_rename_table():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        table1_content = db.table_to_text('table1')
        db.rename_table('table1', 'table4')
        assert not db.table_exists('table1')
        assert db.table_exists('table4')
        with pytest.raises(ValueError) as excinfo:
            db.rename_table('table1', 'table4')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table1"'
        assert table1_content == db.table_to_text('table4')


def test_rename_table_TS():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        table1_content = db.table_to_text('table1')
        db.rename_table('table1', 'table4')
        assert not db.table_exists('table1')
        assert db.table_exists('table4')
        with pytest.raises(ValueError) as excinfo:
            db.rename_table('table1', 'table4')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table1"'
        assert table1_content == db.table_to_text('table4')


def test_copy_table():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.copy_table('table1', 'table4')
        assert db.table_exists('table1')
        assert db.table_exists('table4')
        assert db.get_cols('table1') == ['col1', 'col2']
        assert db.get_cols('table4') == ['col1', 'col2']
        import sys
        sys.stderr.write(f"table1=\n{db.table_to_text('table1')}\n")
        sys.stderr.write(f"table4=\n{db.table_to_text('table4')}\n")
        assert db.table_to_text('table1') == db.table_to_text('table4')
        with pytest.raises(ValueError) as excinfo:
            db.copy_table('table4', 'table2')
        assert str(excinfo.value) == \
            'In database, action cancelled: a table named '\
            '"table2" already exists. Please rename or '\
            'remove it before using this name.'


def test_copy_table_TS():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db.copy_table('table1', 'table4')
        assert db.table_exists('table1')
        assert db.table_exists('table4')
        assert db.get_cols('table1') == ['col1', 'col2']
        assert db.get_cols('table4') == ['col1', 'col2']
        import sys
        sys.stderr.write(f"table1=\n{db.table_to_text('table1')}\n")
        sys.stderr.write(f"table4=\n{db.table_to_text('table4')}\n")
        assert db.table_to_text('table1') == db.table_to_text('table4')
        with pytest.raises(ValueError) as excinfo:
            db.copy_table('table4', 'table2')
        assert str(excinfo.value) == \
            'In database, action cancelled: a table named '\
            '"table2" already exists. Please rename or '\
            'remove it before using this name.'


def test_update_table():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.update_table('table1', 3, ['spes, ei f', 'espoir'])
        assert db.get_table('table1') == \
            [('1', 'adventus,  us, m.', 'arrivée'),
             ('2', 'aqua , ae, f', 'eau'),
             ('3', 'spes, ei f', 'espoir'),
             ('4', 'sol, solis, m', 'soleil')]
        with pytest.raises(ValueError) as excinfo:
            db.update_table('table1', 3, ['spes, ei', 'f', 'espoir'])
        assert str(excinfo.value) == "In database, ['spes, ei', 'f', "\
            "'espoir'] requires 3 columns, but table table1 has only 2 "\
            "columns."


def test_update_table_TS():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db.update_table('table1', 3, ['spes, ei f', 'espoir'])
        assert db.get_table('table1') == \
            [('1', 'adventus,  us, m.', 'arrivée'),
             ('2', 'aqua , ae, f', 'eau'),
             ('3', 'spes, ei f', 'espoir'),
             ('4', 'sol, solis, m', 'soleil')]
        with pytest.raises(ValueError) as excinfo:
            db.update_table('table1', 3, ['spes, ei', 'f', 'espoir'])
        assert str(excinfo.value) == "In database, ['spes, ei', 'f', "\
            "'espoir'] requires 3 columns, but table table1 has only 2 "\
            "columns."


def test_original_name():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        assert db._original_name('table1') == 'table1_0'
        db.create_table('table2_0', ['col1', 'col2'])
        db.create_table('table2_1', ['col1', 'col2'])
        db.create_table('table2_2', ['col1', 'col2'])
        assert db._original_name('table2') == 'table2_3'


def test_sort_table():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.sort_table('table1', 2)
        assert db.table_exists('table1')
        assert not db.table_exists('table1_copy')
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'candidus,  a, um', 'blanc'),
                ('3', 'aqua , ae, f', 'eau'),
                ('4', 'sol, solis, m', 'soleil')]
        with pytest.raises(ValueError) as excinfo:
            db.sort_table('table1', 3)
        assert str(excinfo.value) == 'In database, cannot find a column '\
            'number 3 in table "table1"'
        db.sort_table('table2', 3)
        assert db.get_table('table2', include_headers=True) \
            == [('id', 'col1', 'col2', 'col3'),
                ('1', 'break', 'broke, broken', 'casser'),
                ('2', 'begin', 'began, begun', 'commencer'),
                ('3', 'give', 'gave, given', 'donner'),
                ('4', 'do', 'did, done', 'faire')]


def test_remove_table(mocker):
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.remove_table('table1')
        assert db.list_tables() == ['table2']
        with pytest.raises(ValueError) as excinfo:
            db.remove_table('table1')
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table1"'


def test_create_table(mocker):
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.create_table('table3', ['infinitif', 'passé', 'français'],
                        [('bieten', 'bot, hat geboten', 'offrir'),
                        ('bleiben', 'blieb, ist geblieben', 'rester'),
                        ('gelingen', 'gelang, ist gelungen', 'réussir'),
                        ('schmelzen', 'schmolz, ist geschmolzen', 'fondre'),
                        ('ziegen', 'zog, hat OU ist gezogen',
                         'tirer OU déménager'),
                         ])
        assert db.list_tables() == ['table1', 'table2', 'table3']
        assert db.get_table('table3') \
            == [('1', 'bieten', 'bot, hat geboten', 'offrir'),
                ('2', 'bleiben', 'blieb, ist geblieben', 'rester'),
                ('3', 'gelingen', 'gelang, ist gelungen', 'réussir'),
                ('4', 'schmelzen', 'schmolz, ist geschmolzen', 'fondre'),
                ('5', 'ziegen', 'zog, hat OU ist gezogen',
                 'tirer OU déménager'),
                ]


def test_create_table_TS(mocker):
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db.create_table('table3', ['infinitif', 'passé', 'français'],
                        [('bieten', 'bot, hat geboten', 'offrir'),
                        ('bleiben', 'blieb, ist geblieben', 'rester'),
                        ('gelingen', 'gelang, ist gelungen', 'réussir'),
                        ('schmelzen', 'schmolz, ist geschmolzen', 'fondre'),
                        ('ziegen', 'zog, hat OU ist gezogen',
                         'tirer OU déménager'),
                         ])
        assert db.list_tables() == ['table1', 'table2', 'table3']
        assert db.get_table('table3') \
            == [('1', 'bieten', 'bot, hat geboten', 'offrir'),
                ('2', 'bleiben', 'blieb, ist geblieben', 'rester'),
                ('3', 'gelingen', 'gelang, ist gelungen', 'réussir'),
                ('4', 'schmelzen', 'schmolz, ist geschmolzen', 'fondre'),
                ('5', 'ziegen', 'zog, hat OU ist gezogen',
                 'tirer OU déménager'),
                ]


def test_insert_rows():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        db.insert_rows('table1', [('spes, ei f', 'espoir')])
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'aqua , ae, f', 'eau'),
                ('3', 'candidus,  a, um', 'blanc'),
                ('4', 'sol, solis, m', 'soleil'),
                ('5', 'spes, ei f', 'espoir')]
        with pytest.raises(ValueError) as excinfo:
            db.insert_rows('table3', [('spes, ei', 'f', 'espoir')])
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.insert_rows('table1', [('spes, ei', 'f', 'espoir')])
        assert str(excinfo.value) == "In database, 'spes, ei', 'f', 'espoir'"\
            " requires 3 columns, but table table1 has only 2 columns."
        db.insert_rows('table1', [('amor,  oris, m.', 'amour'),
                                  ('anima,  ae, f.', 'coeur, âme'),
                                  ('hiems, mis,f', 'hiver')])
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'aqua , ae, f', 'eau'),
                ('3', 'candidus,  a, um', 'blanc'),
                ('4', 'sol, solis, m', 'soleil'),
                ('5', 'spes, ei f', 'espoir'),
                ('6', 'amor,  oris, m.', 'amour'),
                ('7', 'anima,  ae, f.', 'coeur, âme'),
                ('8', 'hiems, mis,f', 'hiver')]


def test_insert_rows_TS():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db.insert_rows('table1', [('spes, ei f', 'espoir')])
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'aqua , ae, f', 'eau'),
                ('3', 'candidus,  a, um', 'blanc'),
                ('4', 'sol, solis, m', 'soleil'),
                ('5', 'spes, ei f', 'espoir')]
        with pytest.raises(ValueError) as excinfo:
            db.insert_rows('table3', [('spes, ei', 'f', 'espoir')])
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.insert_rows('table1', [('spes, ei', 'f', 'espoir')])
        assert str(excinfo.value) == "In database, 'spes, ei', 'f', 'espoir'"\
            " requires 3 columns, but table table1 has only 2 columns."
        db.insert_rows('table1', [('amor,  oris, m.', 'amour'),
                                  ('anima,  ae, f.', 'coeur, âme'),
                                  ('hiems, mis,f', 'hiver')])
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'aqua , ae, f', 'eau'),
                ('3', 'candidus,  a, um', 'blanc'),
                ('4', 'sol, solis, m', 'soleil'),
                ('5', 'spes, ei f', 'espoir'),
                ('6', 'amor,  oris, m.', 'amour'),
                ('7', 'anima,  ae, f.', 'coeur, âme'),
                ('8', 'hiems, mis,f', 'hiver')]


def test_merge_tables():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        with pytest.raises(ValueError) as excinfo:
            db.merge_tables('table1', 'table2')
        assert str(excinfo.value) == "In database, cannot merge table table1"\
            " into table table2 because they have different numbers of "\
            "columns (['col1', 'col2'] and ['col1', 'col2', 'col3'])."
        db.create_table('table3', ['col3', 'col4'],
                        [('spes, ei f', 'espoir'),
                        ('amor,  oris, m.', 'amour'),
                        ('anima,  ae, f.', 'coeur, âme'),
                        ('hiems, mis,f', 'hiver')])
        db.merge_tables('table1', 'table3')
        assert db.get_table('table3') \
            == [('1', 'spes, ei f', 'espoir'),
                ('2', 'amor,  oris, m.', 'amour'),
                ('3', 'anima,  ae, f.', 'coeur, âme'),
                ('4', 'hiems, mis,f', 'hiver'),
                ('5', 'adventus,  us, m.', 'arrivée'),
                ('6', 'aqua , ae, f', 'eau'),
                ('7', 'candidus,  a, um', 'blanc'),
                ('8', 'sol, solis, m', 'soleil')
                ]


def test_merge_tables_TS():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        with pytest.raises(ValueError) as excinfo:
            db.merge_tables('table1', 'table2')
        assert str(excinfo.value) == "In database, cannot merge table table1"\
            " into table table2 because they have different numbers of "\
            "columns (['col1', 'col2'] and ['col1', 'col2', 'col3'])."
        db.create_table('table3', ['col3', 'col4'],
                        [('spes, ei f', 'espoir'),
                        ('amor,  oris, m.', 'amour'),
                        ('anima,  ae, f.', 'coeur, âme'),
                        ('hiems, mis,f', 'hiver')])
        db.merge_tables('table1', 'table3')
        assert db.get_table('table3') \
            == [('1', 'spes, ei f', 'espoir'),
                ('2', 'amor,  oris, m.', 'amour'),
                ('3', 'anima,  ae, f.', 'coeur, âme'),
                ('4', 'hiems, mis,f', 'hiver'),
                ('5', 'adventus,  us, m.', 'arrivée'),
                ('6', 'aqua , ae, f', 'eau'),
                ('7', 'candidus,  a, um', 'blanc'),
                ('8', 'sol, solis, m', 'soleil')
                ]


def test_remove_row():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        with pytest.raises(ValueError) as excinfo:
            db.remove_row('table3', 2)
        assert str(excinfo.value) == \
            'In database, cannot find a table named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.remove_row('table1', 7)
        assert str(excinfo.value) == \
            'In database, cannot find a row number 7 in table "table1"'
        db.remove_row('table1', 2)
        assert db.get_table('table1') \
            == [('1', 'adventus,  us, m.', 'arrivée'),
                ('2', 'candidus,  a, um', 'blanc'),
                ('3', 'sol, solis, m', 'soleil')]


def test_remove_rows():
    with ContextManager(TESTDB_PATH, testing=True) as cursor:
        db = Operator(cursor)
        with pytest.raises(ValueError) as excinfo:
            db.remove_rows('table1', '2-5')
        assert str(excinfo.value) == \
            'In database, cannot find a row number 5 in table "table1"'
        db.remove_rows('table1', '1-3')
        assert db.get_table('table1') \
            == [('1', 'sol, solis, m', 'soleil')]


def test_timestamp():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db._timestamp('table1', 1)
        stamped = \
            cursor.execute('SELECT id FROM table1 WHERE timestamp != 0;')\
            .fetchall()
        assert stamped == [(1, )]


def test_reset():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        db._timestamp('table1', 1)
        db._timestamp('table1', 2)
        db._timestamp('table1', 3)
        db._timestamp('table1', 4)
        db._reset('table1', 1)
        stamped = \
            cursor.execute('SELECT id FROM table1 WHERE timestamp != 0;')\
            .fetchall()
        assert len(stamped) == 3
        db._timestamp('table1', 1)
        db._timestamp('table1', 2)
        db._timestamp('table1', 3)
        db._timestamp('table1', 4)
        db._reset('table1', 3)
        stamped = \
            cursor.execute('SELECT id FROM table1 WHERE timestamp != 0;')\
            .fetchall()
        assert len(stamped) == 1
        db._timestamp('table1', 1)
        db._timestamp('table1', 2)
        db._timestamp('table1', 3)
        db._full_reset('table1')
        stamped = \
            cursor.execute('SELECT id FROM table1 WHERE timestamp != 0;')\
            .fetchall()
        assert len(stamped) == 0


def test_draw_rows():
    with ContextManager(TESTDB_TS_PATH, testing=True) as cursor:
        db = Ts_Operator(cursor)
        with pytest.raises(ValueError) as excinfo:
            db.draw_rows('table3', 2)
        assert str(excinfo.value) == 'In database, cannot find a table '\
            'named "table3"'
        with pytest.raises(ValueError) as excinfo:
            db.draw_rows('table1', 5)
        assert str(excinfo.value) == '5 rows are required from "table1", '\
            'but it only contains 4 rows.'
        result = db.draw_rows('table1', 2)
        assert len(result) == 2
        assert all([type(r) == tuple for r in result])
        assert all([len(r) == 2 for r in result])
        db._full_reset('table1')
        db._timestamp('table1', 1)
        db._timestamp('table1', 2)
        result = db.draw_rows('table1', 2, oldest_prevail=True)
        assert ('candidus,  a, um', 'blanc') in result
        assert ('sol, solis, m', 'soleil') in result
        db._full_reset('table1')
        db._timestamp('table1', 1)
        db._timestamp('table1', 2)
        db._timestamp('table1', 3)
        result = db.draw_rows('table1', 2, oldest_prevail=True)
        assert ('sol, solis, m', 'soleil') in result
