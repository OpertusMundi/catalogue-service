from setuptools import setup, find_packages

setup(
    name='catalogueapi',
    version='0.0.1',
    description='Boilerplate code for a RESTful API based on Flask-RESTPlus',
    author='Nikiforos Leonidakis',

    classifiers=[
        'Development Status :: 5 - Development',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.13', 'Flask-SQLAlchemy==2.4.1'],
)