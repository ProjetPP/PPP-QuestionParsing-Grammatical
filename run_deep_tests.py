#!/usr/bin/env python3

# The following unit tests require Stanford CoreNLP library.
# Please launch the server before running these tests.

import os
import unittest

os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = 'example_config.json'

def main(): # pragma: no cover
    testsuite = unittest.TestLoader().discover('tests/')
    results = unittest.TextTestRunner(verbosity=1).run(testsuite)
    if results.errors or results.failures:
        exit(1)
    testsuite = unittest.TestLoader().discover('deep_tests/')
    results = unittest.TextTestRunner(verbosity=1).run(testsuite)
    if results.errors or results.failures:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    main()
