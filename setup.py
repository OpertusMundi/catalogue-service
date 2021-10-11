from setuptools import setup, find_packages

setup(
    name='catalogueapi',
    version='0.0.2',
    description='A RESTful catalogue API based on Flask-RESTX',
    author='Nikiforos Leonidakis',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Development',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='rest restful api flask swagger openapi flask-restx',
    packages=find_packages(exclude=('tests*',)),
    include_package_data=True,
    package_data={'catalogueapi': [
        'resources/*.json',
    ]},
    install_requires=['flask-restx==0.5.1', 'Flask-SQLAlchemy==2.4.1'],
    zip_safe=False,
)
