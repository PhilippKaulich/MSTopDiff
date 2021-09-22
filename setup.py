# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:56:34 2021

@author: Philipp
"""

from setuptools import setup, find_packages


setup(
    name = 'MSTopDif',
    version = '1.0.0',
    url = '',
    author = 'Philipp Theodor Kaulich',
    author_email = 'p.kaulich@iem.uni-kiel.de',
    description = 'MSTopDif is a command line script with graphical user'
                  ' interface for the database-free detection of modifications '
                  'in top-down mass spectrometric data.',
    license = 'BSD-3-Clause',
    packages = find_packages(),
    include_package_data = True,
    classifiers=[
        'Development Status :: ',
        'Intended Audience :: End users :: Developers',
        'Topic :: command line script :: GUI',
        'Programming Language :: Python :: 3.7.3'
    ],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'pandas',
		'PyQT5',
    ]
)