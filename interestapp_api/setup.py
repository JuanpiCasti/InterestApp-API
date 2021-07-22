from setuptools import setup

setup(
    name='interestapp_api',
    packages=['Models', 'Schemas'],
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-SQLAlchemy',
        'flask-marshmallow'
    ],
)