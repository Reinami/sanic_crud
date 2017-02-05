from setuptools import setup

setup(
    name='sanic_crud',
    version='0.1.5',
    url='https://github.com/Typhon66/sanic_crud',
    license='MIT',
    author='Typhon',
    author_email='typhonnge@gmail.com',
    description='A REST API framework for building CRUD APIs using Sanic and peewee',
    packages=['sanic_crud'],
    platforms='any',
    install_requires=[
        'peewee==2.8.5',
        'sanic==0.3.0'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sanic api rest crud'
)
