#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Mail Sender Setup
Created on 2018-01-18
@author: Mellcap
'''

from setuptools import setup, find_packages
VERSION = '0.1.0'

setup(
    name='MailSender',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'Flask==0.12.2',
        'Flask-MySQLdb==0.2.0',
        'Flask-Script==2.0.6',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-Mail==0.9.1',
        'Flask-Migrate==2.1.1',
        'celery==4.1.0',
        'redis==2.10.6',
        'Flask-WTF==0.14.2',
        'Jinja2==2.10',
        'Flask-Bootstrap==3.3.7.1',
        'docker-compose==1.18.0',
        'arrow==0.12.0',
        'Flask-Admin==1.5.0'
    ],

    license='MIT',
    author='Mellcap',
    author_email='imellcap@gmail.com',
    url='https://github.com/Mellcap/mail_sender',
    description='A mail sender example powers by Flask.',
    keywords=['mail_sender', 'Flask'],
)
