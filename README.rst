|coveralls|

Overview
========

Microlib contains some useful functions or classes:

- XDict is a dict with recursive_update() and flat() methods,
- StandardConfigFile helps to manage user config files,
- terminal.ask_yes_no() and terminal.ask_user_choice() to ask questions to the user for cli tools,
- terminal.tabulate() is a very simple function to display tabulated data in the terminal,
- terminal.echo_info() echo_warning() and echo_error() display info, warning and error messages with some color.
- rotate() and grouper() help to handle iterators.
- read_text() reads text files and concatenates their contents.
- database offers a ContextManager for sqlite3 database, an Operator and a Ts_Operator classes to provide shortcuts for common sqlite3 commands.

`Source code <https://gitlab.com/nicolas.hainaux/microlib>`__

.. |coveralls| image:: https://coveralls.io/repos/gitlab/nicolas.hainaux/microlib/badge.svg?branch=master
  :target: https://coveralls.io/gitlab/nicolas.hainaux/microlib?branch=master
