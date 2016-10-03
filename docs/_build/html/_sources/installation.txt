Installation
============

1. Create a virtual environment
2. Install Django
3. Create a new Django project
4. Add SESSION_SERIALIZER
3. Install CBA

$ pip install https://github.com/diefenbach/cba/archive/master.zip

4. Add CBA to your installed apps
5. migrate

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

Example Application
===================

1. Install cba-notes
1. Add settings middleware
2. Add URL
3. migrate
5. create superuser
4. runserver

