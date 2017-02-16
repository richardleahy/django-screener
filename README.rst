=====
Screener
=====

Screener is a simple Django REST app to manage phone screening. For each
screen, users add questions and candidates.


Requires
--------
Django REST framework,
AngularJS,
Bootstrap

PyPI download
-------------
pip install django-screener


Important Info
--------------
Requires a valid session. Your site must provide its own login functionality to
get this. This app uses AngularJS and Bootstrap and includes CDN links for these
automatically in index.html. If you do not have a valid internet connection or do not wish to use a CDN,
swap these out for local copies. 


Quick start
-----------

1. Add "screener and the Django REST framework" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'screener.apps.ScreenerConfig',
    ]

2. Include the screener URLconf in your project urls.py like this::

    url(r'^screener/', include('screener.urls')),

3. Run `python manage.py migrate` to create the screener models.

4. Start the development server (python manage.py runserver) and visit the AngularJS front-end http://127.0.0.1:8000/screener/
   
5. Visit http://127.0.0.1:8000/screener/api/ to view the API. Need to add url(r'^api-auth/', include('rest_framework.urls')),
   to your root urls.py to be able to login if you do not already have login functionality.
You can uncomment the url below in screener/urls.py to log in using the django rest framework:
screener/urls.py:
    # Remove comment to login into the API if you do not have any login functionality then navigate back to http://127.0.0.1:8000/screener/
    # http://127.0.0.1:8000/screener/api/
    #url(r'^api-auth/', include('rest_framework.urls')),

6. Add some questions.

7. Add some screens.

8. Create candidates and add them to screens

9. Start phone screening! 
