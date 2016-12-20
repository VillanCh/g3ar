#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar setup
  Created: 2016/12/20
"""

from codecs import open as copen
from setuptools import setup, find_packages

packages = [
    'g3ar',
    'g3ar.decologger',
    'g3ar.dict_parser',
    'g3ar.taskbulter',
    'g3ar.threadutils',
]

requires = []

version = '0.0.1alpha3'

#
# LOAD README.md
#
readme = None
with copen('README.md', encoding='utf-8') as f:
    readme = f.read()
    
history = None
with copen('HISTORY.md', encoding='utf-8') as f:
    history = f.read()
    
setup(
    name='g3ar',
    version=version,
    description='Python Coding Toolkit for Pentester.',
    long_description=readme + '\n\n' + history,
    author='v1ll4n/VillanCh',
    author_email='v1ll4n@villanch.top',
    url='https://github.com/VillanCh/g3ar',
    packages=packages,
    package_data={"":"LICENSE"},
    package_dir={'g3ar':'g3ar'},
    include_package_data=True,
    install_requires=requires,
    license='BSD 2-Clause License',
    zip_safe=False,
)