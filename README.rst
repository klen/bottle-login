Bottle Login
############

.. _description:

Bottle Login -- Implement users' sessions in Bottle web framework.

.. _badges:

.. image:: http://img.shields.io/travis/klen/bottle-login.svg?style=flat-square
    :target: http://travis-ci.org/klen/bottle-login
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/klen/bottle-login.svg?style=flat-square
    :target: https://coveralls.io/r/klen/bottle-login
    :alt: Coverals

.. image:: http://img.shields.io/pypi/v/bottle-login.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-login

.. image:: http://img.shields.io/pypi/dm/bottle-login.svg?style=flat-square
    :target: https://pypi.python.org/pypi/bottle-login

.. image:: http://img.shields.io/gratipay/klen.svg?style=flat-square
    :target: https://www.gratipay.com/klen/
    :alt: Donate

.. _contents:

.. contents::

.. _requirements:

Requirements
=============

- python >= 2.6

.. _installation:

Installation
=============

**Bottle Login** should be installed using pip: ::

    pip install bottle-login

.. _usage:

Usage
=====

::

    from bottle import Bottle, request, redirect
    from bottle_login import LoginPlugin

    app = Bottle()
    app.config['SECRET_KEY'] = 'secret'

    login = app.install(LoginPlugin())

    @login.load_user
    def load_user_by_id(user_id):
        # Load user by id here


    # Some application views

    @app.route('/')
    def index():
        current_user = login.get_user()
        return current_user.name

    @app.route('/signout')
    def signout():
        # Implement logout
        login.logout_user()
        return redirect('/')

    @app.route('/signin')
    def signin():
        # Implement login (you can check passwords here or etc)
        user_id = int(request.GET.get('user_id'))
        login.login_user(user_id)
        return redirect('/')


.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/bottle-login/issues

.. _contributing:

Contributing
============

Development of Bottle Login happens at: https://github.com/klen/bottle-login


Contributors
=============

* klen_ (Kirill Klenov)

.. _license:

License
=======

Licensed under a `BSD license`_.

.. _links:

.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: https://github.com/klen
