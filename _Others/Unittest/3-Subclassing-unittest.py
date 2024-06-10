import unittest

    # Here, we subclass unittest.TestCase. What we mean is we make our class 
    # TestStringMethods inherit from the class unittest.TestCase. 
    # Then, we define three methods, the names for which begin with ‘test’:
    
    # assertEqual()- Tests that the two arguments are equal in value.
    # assertNotEqual()- Tests that the two arguments are unequal in value.
    # assertTrue()- Tests that the argument has a Boolean value of True.
    # assertFalse()- Tests that the argument has a Boolean value of False.
    # assertIs()- Tests that the arguments evaluate to the same object.
    # assertIsNot()- Tests that the arguments do not evaluate to the same object.
    # assertIsNone()- Tests that the argument evaluates to none.
    # assertIsNotNone()- Tests that the argument does not evaluate to none.
    # assertIn()- Tests that the first argument is in the second.
    # assertNotIn()- Tests that the first argument is not in the second.
    # assertIsInstance()- Tests that the first argument (object) is an instance of the second (class).
    # assertRaises()- Tests that Python raises an exception when we call the callable with positional/ keyword arguments we also passed to this method.
    # assertRaisesRegex()- Tests that regex matches on the string representation of the exception raised; similar to assertRaises().
    # assertWarns()- Tests that Python triggers a warning when we call the callable with positional/ keyword arguments we also passed to this method.
    # assertWarnsRegex()- Tests that regex matches on the message for the triggered warning; similar to assertWarns().
    # assertLogs()- Tests that Python has logged at least one message on the logger or a child of the logger; ensures this is with at least the level we mention.
    # assertAlmostEqual()- Tests that the first and second arguments have approximately equal values.
    # assertNotAlmostEqual()- Tests that the first and second arguments do not have approximately equal values.
    # assertGreater()- Tests that the first argument is greater than the second.
    # assertGreaterEqual()- Tests that the first argument is greater than or equal to the second.
    # assertLess()- Tests that the first argument is lesser than the second.
    # assertLessEqual()- Tests that the first argument is lesser than or equal to the second.
    # assertRegex()- Tests that a regex search matches the text.
    # assertNotRegex()- Tests that a regex search does not match the text.
    # assertCountEqual()- Tests that the first argument, which is a sequence, contains the same as does the second.
    # assertMultiLineEqual()- Tests that the first argument, which is a multiline string, is equal to the second.
    # assertSequenceEqual()- Tests that two sequences are equal.
    # assertListEqual()- Tests that two lists are equal.
    # assertTupleEqual()- Tests that two lists are equal.
    # assertSetEqual()- Tests that two sets are equal.
    # assertDictEqual()- Tests that two dictionaries are equal.
    
class TestStringMethods(unittest.TestCase):
      def test_lstrip(self):
              self.assertEqual('   hello '.lstrip(),'hello ')
      def test_isupper(self):
              self.assertTrue('HELLO'.isupper())
              self.assertFalse('HELlO'.isupper())
      def test_split(self):
              self.assertEqual('Hello World'.split(),['Hello','World'])
              with self.assertRaises(TypeError):
                s.split(2)
if __name__=='__main__':
    unittest.main()