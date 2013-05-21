# -*- coding: utf-8 -*-
# rapla-cleaner
# Copyright: (c) 2013 Christoph Heer
# License: BSD


from setuptools import setup

setup(
    name='rapla-cleaner',
    version='0.2',
    url='https://github.com/jarus/rapla-cleaner',
    license='BSD',
    author='Christoph Heer',
    author_email='Christoph.Heer@googlemail.com',
    description='Wrapper WebService for rapla.dhbw-karlsruhe.de',
    packages=['rapla_cleaner'],
    zip_safe=False,
    install_requires=[
        'Flask==0.9'
    ]
)