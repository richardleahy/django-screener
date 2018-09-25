import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-screener',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD 3-Clause',
    description='Phone screen management for interviewers',
    long_description=README,
    author='Richard Leahy',
    author_email='richard-james.leahy@hotmail.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django', 
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
