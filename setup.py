# Cython compile instructions

from setuptools import setup

from setuptools import Extension, find_packages
import numpy
import os
import glob
from sys import platform
import sys
import sysconfig
py_modules = ['tinyImpute', 'tinyMgsAssign']

src_modules = []
src_modules += glob.glob(os.path.join('src','tinyhouse-tinyassign', '*.py'))
src_modules += glob.glob(os.path.join('src','Assign', '*.py'))

src_modules = [os.path.splitext(file)[0] for file in src_modules]
py_modules += src_modules

setup(
    name="AlphaAssign",
    version="0.0.1",
    author="Andrew Whalen",
    author_email="awhalen@roslin.ed.ac.uk",
    description="A pedigree assignement algorithm.",
    long_description="AlphaAssign is a parentage assignement algorithm that was designed to handle SNP and GBS data.",
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    py_modules = py_modules,

    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points = {
    'console_scripts': [
        'AlphaAssign=tinyAssign:main',
        'TinyMGSAssign=tinyMgsAssign:main',
        ],
    },
    install_requires=[
        'numpy',
        'numba',
        'scipy',
        'alphaplinkpython'
    ]
)
