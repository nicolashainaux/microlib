|coveralls|

License
=======
Microlib is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or any later version. See LICENSE file.

Microlib also includes third party open source software components: the Deprecated class. It has its own license. Please see ./microlib/deprecation.py

Overview
========

Microlib contains some useful functions or classes:

- XDict is a dict with recursive_update() and flat() methods,
- StandardConfigFile helps to manage user config files,
- terminal.ask_yes_no() and terminal.ask_user_choice() to ask questions to the user for cli tools,
- terminal.tabulate() is a very simple function to display tabulated data in the terminal,
- terminal.echo_info() echo_warning() and echo_error() display info, warning and error messages with some color.
- rotate() and grouper() help to handle iterators.
- database offers a ContextManager for sqlite3 database, an Operator and a Ts_Operator classes to provide shortcuts for common sqlite3 commands.
- a Deprecated class, that provides a decorator to deprecate functions (emit a warning when it is called).

`Source code <https://gitlab.com/nicolas.hainaux/microlib>`__

.. |coveralls| image:: https://coveralls.io/repos/gitlab/nicolas.hainaux/microlib/badge.svg?branch=master
  :target: https://coveralls.io/gitlab/nicolas.hainaux/microlib?branch=master
