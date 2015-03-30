#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='ift4055-projet-honor-Antaki',
    description='Algorithm for evaluation of the accessibilty problem in continuous petri nets',
    author='Vincent Antaki',
    requires=['numpy (>=1.9)','scipy (>=0.15)','nose', 'python-qsoptex'],
    dependency_link = ['https://github.com/DjAntaki/python-qsoptex'])
