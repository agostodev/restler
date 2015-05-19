restler
=======

Restler is an object Serialization library for the web. It supports
translating objects to JSON or XML. Currently, it is targeted at
Google App Engine with python 2.7. Documentation can be found at:
http://substrate-docs.appspot.com/restler.html

If you are using App Engine, you may also be interested in Substrate,
which packages Restler and several other useful libraries into an
application template: http://substrate-docs.appspot.com

Installation
------------

Install Restler from PyPi using easy_install or pip; or download the
package and run::

  python setup.py install

(Running ``setup.py`` requires setuptools.)

For use on Google App Engine, you will need to install the code in the
``restler`` directory somewhere in your path.

Running Tests
-------------

To run restler's tests::

  ./run_tests.py

Running tests requires python 2.7 the Google App Engine SDK.
  
Usage
-----

A db.Model or ndb.Model instance can be serialized with the default settings using ``to_json`` or ``to_xml``.

>>> jean = Person(first_name="Jeanne", last_name="d'Arc", ssn="N/A")
>>> to_json(jean)
'{"first_name": "Jeanne", "last_name": "d\'Arc", "ssn": "N/A"}'

To include only certain fields, use a ``ModelStrategy``.
When using a ``ModelStrategy``, you will need to use a restler model decorator.

>>> @ae_db_serializer
>>> class User(db.Model)
>>>    ...

Now setup the ``ModelStrategy``

>>> person_strategy = ModelStrategy(Person).include("first_name", "last_name")
>>> to_json(jean, person_strategy)
'{"first_name": "Jeanne", "last_name": "d'Arc"}'

Or, to exclude specified fields:

>>> person_strategy = ModelStrategy(Person, include_all_fields=True).exclude("ssn")
>>> to_json(jean, person_strategy)
'{"first_name": "Jeanne", "last_name": "d'Arc"}'

For more details on customizing serialization, see the documentation.


TODO
----

https://bitbucket.org/curtis/restler/issues?status=new&status=open
