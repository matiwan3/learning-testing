# Now let’s try testing for string methods; we won’t need a function for this.
# self represents the instance of the class. By using the “self” we can access the 
# attributes and methods of the class in python. It binds the attributes with 
# the given arguments. The reason you need to use self. is because Python does not 
# use the @ syntax to refer to instance attributes
import unittest

class TestStringMethods(unittest.TestCase):
    def test_lstrip(self): #testing for left stripping
                self.assertEqual('   hello '.lstrip(),'hello ')
    def test_isupper(self): #testing for isupper
                self.assertTrue('HELLO'.isupper())
                self.assertFalse('HELlO'.isupper())
    def test_split(self): #testing for split
                self.assertEqual('Hello World'.split(),['Hello','World'])
                with self.assertRaises(TypeError):
                        'Hello World'.split(2)
if __name__=='__main__':
    unittest.main()