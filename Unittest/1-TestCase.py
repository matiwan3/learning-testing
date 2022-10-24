# Python Unittest is a Python Unit-Testing framework. Inspired by JUnit,
# it is much like the unit testing frameworks we have with other languages.

# Here are some features it supports-

# Test automation
# Sharing setup and shutdown code for tests
# Aggregating tests into collections
# Independence of tests from the framework

# Concepts in an object-oriented way for Python Unittest
# Test fixture- the preparation necessary to carry out test(s) and related cleanup actions.
# Test case- the individual unit of testing.
# A Test suite- collection of test cases, test suites, or both.
# Test runner- component for organizing the execution of tests and for delivering the outcome to the user.
# In this Python Unittest tutorial, we will use the unittest module to demonstrate our examples to you.

import unittest
def modthree(x):
    return x%3

class Tests(unittest.TestCase):
    def test(self):
        self.assertEqual(modthree(4),1)

if __name__ == "__main__":
    unittest.main()