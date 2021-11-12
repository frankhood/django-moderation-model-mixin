=====
Usage
=====

To use Django Moderation Model Mixin in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'moderation_model_mixin.apps.ModerationModelMixinConfig',
        ...
    )

Add Django Moderation Model Mixin's URL patterns:

.. code-block:: python

    from moderation_model_mixin import urls as moderation_model_mixin_urls


    urlpatterns = [
        ...
        url(r'^', include(moderation_model_mixin_urls)),
        ...
    ]
