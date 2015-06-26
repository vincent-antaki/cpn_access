#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='cpn_access',
    description='Algorithm to solve the reachability problem in continuous petri nets',
    author='Vincent Antaki',
    requires=['numpy (>=1.9)', 'python-qsoptex'],
    dependency_link = ['https://github.com/jonls/python-qsoptex'])
