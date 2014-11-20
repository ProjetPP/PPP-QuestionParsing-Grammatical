#!/bin/bash
python3-coverage run --source=ppp_questionparsing_grammatical run_tests.py
python3-coverage html
xdg-open htmlcov/index.html
