#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ppp_nlp_classical',
    version='0.1.1',
    description='Natural language processing module for the PPP.',
    url='https://github.com/ProjetPP',
    author='Projet Pensées Profondes',
    author_email='ppp2014@listes.ens-lyon.fr',
    license='MIT',
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'ppp_datamodel>=0.5,<0.6',
        'ppp_core>=0.5,<0.6',
    ],
    packages=[
        'ppp_nlp_classical',
    ],
)
