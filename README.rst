=============================
Django Moderation Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-moderation-model-mixin.svg/?style=flat-square
    :target: https://badge.fury.io/py/django-moderation-model-mixin

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://django-moderation-model-mixin.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/django-moderation-model-mixin/master?style=flat-square
    :target: https://coveralls.io/github/frankhood/django-moderation-model-mixin?branch=master
    :alt: Coverage Status

This package adds the possibility of handle a moderation to django models and associated admins.
This means being able to mark an entry as accepted, rejected or to be moderated (default).
Querysets, Managers and Signals are included.


Documentation
-------------

The full documentation is at https://django-moderation-model-mixin.readthedocs.io.

Quickstart
----------

Install Django Moderation Model Mixin::

    pip install django-moderation-model-mixin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'moderation_model_mixin',
        ...
    )

Features
--------

* ModerationModelMixin
* ModerationModelMixinAdmin
* ModerableQuerySet
* Actions in admin changelist
* Signals associated to moderation action

Example of usage
----------------
.. code-block:: python

    # in your admin.py
    class ExampleModelAdmin(ModerationModelMixinAdmin, admin.ModelAdmin):
        ...

    admin.site.register(ExampleModel, ExampleModelAdmin)

    # in your models.py
    from moderation_model_mixin.models import ModerationModelMixin

    class ExampleModel(ModerationModelMixin, models.Model):
        ...

Admin Interface
---------------

Here some users interface example.

.. image:: docs/images/not_moderated_instance.png
    :alt: Not moderated instance image

First one is how the change form is shown. There are two new buttons in the submit row that allows to accept or reject entries that not yet moderated.

.. image:: docs/images/accepted_instance.png
    :alt: Accepted instance image

This is how an accepted entry looks.

.. image:: docs/images/rejected_instance.png
    :alt: Rejected instance image

This is how a rejected entry looks.

.. image:: docs/images/pop_up.png
    :alt: Pop-up image
A confirmation pop-up is shown when an acceptance or rejection request is made

.. image:: docs/images/actions_available.png
    :alt: Actions image
Last image shows actions in the changelist.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
