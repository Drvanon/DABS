#!/usr/bin/env python

from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='DABS',
    version='1.0',
    description='Dorstijn Automated Building System',
    long_description=readme(),
    author='Robin & Danny Dorstijn',
    author_email='robbiedorstijn@gmail.com',
    url='https://github.com/Drvanon/DABS',
    license='MIT',
    install_requires=['PyYAML', 'docopt', 'ninja-syntax'],
    packages=['dabs'],
    zip_safe=False
    )
