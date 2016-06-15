"""
Module with class LanguageTest, which inherits from unittest.TestCase
"""

from src.model.language import Language
import unittest


class LanguageTest(unittest.TestCase):
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 13.06.2016
    @summary: Test case for class Language, using PyUnit test framework.
              Every new test case has the base class TestCase.
              A test case is an individual unit of testing.
              A test suite is a collection of test cases, test
              suites, or both.
    @see: https://docs.python.org/3/library/unittest.html#module-unittest
    """
    def setUp(self):
        """
        test fixture, preparation needed for test cases.
        setUp will be executed before each test case
        """
        print("setUp")
        self.language = Language("English", 3)
        print(self.language)

    def tearDown(self):
        """
        clean-up steps, after each test case
        """
        print("tearDown")
        del self.language
        self.assertRaises(AttributeError, lambda: print(self.language))

    def test_information_hiding(self):
        """
        test method, testing properties, string representation of Language
        instance via magic method __str__.
        """
        self.assertIsInstance(self.language, Language)
        self.assertIsNotNone(self.language)
        self.assertRaises(AttributeError, lambda: self.language.__name)
        self.assertRaises(AttributeError, lambda: self.language.__user_id)
        self.assertIs(self.language.language_id_property, None)
        self.assertIsNone(self.language.language_id_property)
        self.assertEqual(self.language.name_property, "English")
        self.assertEqual(self.language.user_id_property, 3)
        self.assertEqual(str(self.language), "None English 3")


if __name__ == "__main__":
    unittest.main()
