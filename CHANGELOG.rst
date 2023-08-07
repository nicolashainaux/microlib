Unreleased
----------


Version 1.9.3 (2023-08-07)
--------------------------

* Patch release

Version 1.9.2 (2022-08-25)
--------------------------

* Patch release


Version 1.9.1 (2022-07-21)
--------------------------

* Patch release


Version 1.9 (2022-07-19)
------------------------

* Provides a Deprecated class (provides a decorator to deprecate functions (emit a warning when it is called))
* Deprecates read_text() (in favor of pathlib.Path.read_text() from standard library, what's almost the same)


Version 1.8 (2022-03-23)
------------------------

* Provides fracdigits_nb() and turn_to_capwords()


Version 1.7 (2021-08-31)
------------------------

* Provides terminal.ask_user_choice()


Version 1.6 (2021-08-27)
------------------------

* Improve database (add drop_table() to Operator objects)


Version 1.5 (2021-08-26)
------------------------

* Provides terminal.ask_user_choice()


Version 1.4 (2021-08-25)
------------------------

* Improve database (add get_rows() to Operator objects)


Version 1.3 (2021-08-06)
------------------------

* Provides database (offers a ContextManager for sqlite3 database, an Operator and a Ts_Operator classes to provide shortcuts for common sqlite3 commands)

Version 1.2.1 (2021-06-29)
--------------------------

* Patch release


Version 1.2 (2021-06-29)
------------------------

* Provides read_text() (reads text files and concatenates their contents)
* Provides terminal.echo_info() echo_warning() and echo_error() (display info, warning and error messages with some color)

Version 1.1.1 (2021-03-10)
--------------------------

* Patch release


Version 1.1 (2021-02-27)
------------------------

* Provides StandardConfigFile


Version 1.0 (2020-12-11)
------------------------

* Provides XDict (dict with recursive_update() and flat() methods)
* Provides terminal.ask_yes_no() (to ask a [y/N] question to the user for cli tools)
* Provides terminal.tabulate() (very simple function to display tabulated data in the terminal)
* Provides rotate() and grouper() (help to handle iterators)
