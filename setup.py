from setuptools import setup, find_packages

setup(
    name='catalogueapi',
    version='0.0.1',
    description='Boilerplate code for a RESTful API based on Flask-RESTX',
    author='Nikiforos Leonidakis',

    classifiers=[
        'Development Status :: 5 - Development',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest restful api flask swagger openapi flask-restx',

    packages=find_packages(),

    install_requires=['flask-restx==0.2', 'Flask-SQLAlchemy==2.4.1'],
)