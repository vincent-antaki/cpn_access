from distutils.core import setup
from Cython.Build import cynthonize

setup(
    name='ift4055-',
    description='Reachability of petri nets and d-VASS',
    requires=['numpy (>=1.9)','scipy (>=0.15)','nose'])
    

