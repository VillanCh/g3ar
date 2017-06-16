#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: G3ar setup
  Created: 2016/12/20
"""

from codecs import open as copen
from setuptools import setup, find_packages

packages = find_packages()

requires = ['IPy', 'ipwhois', 'colorama', 'prettytable']

version = '0.5.7'

#
# LOAD README.md
#
try:
    readme = None
    with copen('README.md',  encoding='utf-8') as f:
        readme = f.read()

    history = None
    with copen('HISTORY.md', encoding='utf-8') as f:
        history = f.read()
except:
    readme = 'Python Coding Toolkit for Pentester.' + \
        '\nGithub: https://github.com/VillanCh/g3ar' + \
        '\nREADME.md: https://github.com/VillanCh/g3ar/blob/master/README.md\n\n'
    history = 'https://github.com/VillanCh/g3ar/blob/master/HISTORY.md'


setup(
    name='g3ar',
    version=version,
    description='Python Coding Toolkit for Pentester.',
    long_description=readme + '\n\n' + history,
    author='v1ll4n',
    author_email='v1ll4n@villanch.top',
    url='https://github.com/VillanCh/g3ar',
    packages=packages,
    package_data={"":["LICENSE", 'README.md', 'HISTORY.md']},
    package_dir={'g3ar':'g3ar'},
    include_package_data=True,
    install_requires=requires,
    license='BSD 2-Clause License',
    zip_safe=False,
)
