=====
Screener
=====

Screener is a simple Django REST app to manage phone screening. For each
screen, users add questions and candidates.


Requires
--------
Django REST framework

PyPI download
-------------
pip install django-screener


Important Info
--------------
Requires a valid token to access the API. Your site must provide its own login functionality.
You can use the django-rest-auth package to handle token authentication for you.
https://django-rest-auth.readthedocs.io/en/latest/installation.html

If you want to browse the API in the browser, a valid session will be required. You can uncomment the default session login
provided by the Django Rest Framework in the project root urls.py for this if you do not have session login 
functionality. Documentation for this can be found below.
http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#adding-login-to-the-browsable-api

This is just an API. Grab the client side code from this repo https://github.com/richardleahy/ng-screener


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

4. Start the development server (python manage.py runserver)

5. Grab the GUI from this repo https://github.com/richardleahy/ng-screener
   
5. Visit http://127.0.0.1:8000/screener/ to view the API. Need to add url(r'^api-auth/', include('rest_framework.urls')),
   to your root urls.py to be able to login if you do not already have login functionality.

6. Add some questions.

7. Add some screens.

8. Create candidates and add them to screens

9. Start phone screening! 
