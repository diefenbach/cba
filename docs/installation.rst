Install CBA
===========

.. warning::

    CBA is alpha with all well known consequences.

.. warning::

    This installation is based on the master branch. So it might be broken from
    time to time. If so please upgrade. There will be a released based
    installation any time soon.

#. Create a virtual environment::

    $ virtualenv myenv

#. Install Django::

    $ pip install Django

#. Install CBA::

    $ pip install https://github.com/diefenbach/cba/archive/master.zip

#. Create a new Django project::

    $ django-admin startproject cba_project

#. Add CBA to your INSTALLED_APPS (within settings.py)::

    INSTALLED_APPS = [
        ...
        'cba',
    ]

#. Add Middleware (within settings.py)::

    MIDDLEWARE = [
        ...
        'cba.RequestMiddleware',
    ]

#. Add other settings (within settings.py)::

    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
    DATA_UPLOAD_MAX_MEMORY_SIZE = 10000000
    MEDIA_ROOT = BASE_DIR + "/media"
    MEDIA_URL = "/media/"
    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

#. Migrate Database::

    $ cd cba_project
    $ bin/manage.py migrate

Install the Examples reference application
==========================================

#. Install cba-examples::

    $ pip install https://github.com/diefenbach/cba-examples/archive/master.zip

#. Add the examples app to your INSTALLED_APPS (within settings.py)::

    INSTALLED_APPS = [
        ...
        'cba_examples',
    ]

#. Register urls (within urls.py)::

    from django.conf import settings
    from django.conf.urls import include
    from django.conf.urls.static import static

    ...

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^examples/', include("cba_examples.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#. Start development server::

    $ python manage.py runserver

#. Open browser::

    http://localhost:8000/examples

Install the Notes reference application
=======================================

#. Install cba-notes::

    pip install https://github.com/diefenbach/cba-notes/archive/master.zip

#. Add the notes app and taggit to INSTALLED_APPS::

    INSTALLED_APPS = [
        ...
        'taggit',
        'notes',
    ]

#. Register urls (within urls.py)::

    from django.conf.urls.static import static
    from notes import views as notes_views

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^examples/', include("cba_examples.urls")),
        url(r'^$', notes_views.NotesView.as_view(), name='notes'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#. Migrate the database::

    $ python manage.py migrate

#. Create superuser::

    $ python manage.py createsuperuser

#. Start development server::

    $ python manage.py runserver

#. Open browser::

    http://localhost:8000
