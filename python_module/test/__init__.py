"""
Definision of test suite
"""
import os
from unittest import TestLoader, TextTestRunner

def run():
    """ test suite """
    tests = TestLoader().discover(os.path.dirname(__file__))
    TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    run()
