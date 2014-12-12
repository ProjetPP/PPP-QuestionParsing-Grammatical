#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ppp_questionparsing_grammatical',
    version='0.4.7',
    description='Natural language processing module for the PPP.',
    url='https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical',
    author='Projet Pensées Profondes',
    author_email='ppp2014@listes.ens-lyon.fr',
    license='MIT',
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
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
        'ppp_libmodule>=0.6,<0.7',
        'jsonrpclib-pelix',
        'nltk'
    ],
    packages=[
        'ppp_questionparsing_grammatical',
        'ppp_questionparsing_grammatical.data',
    ],
)

import sys
if 'install' in sys.argv:
    import nltk
    nltk.download("wordnet")
