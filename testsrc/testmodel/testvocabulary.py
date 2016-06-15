"""
Module with class VocabularyTest, which inherits from unittest.TestCase
"""

from src.model.vocabulary import Vocabulary
import unittest


class VocabularyTest(unittest.TestCase):
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 13.06.2016
    @summary: Test case for class Vocabulary, using PyUnit test framework.
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
        self.vocabulary = Vocabulary("Haus", "house", 1)
        print(self.vocabulary)

    def tearDown(self):
        """
        clean-up steps, after each test case
        """
        print("tearDown")
        del self.vocabulary
        self.assertRaises(AttributeError, lambda: print(self.vocabulary))

    def test_information_hiding(self):
        """
        test method, testing properties, string representation of Vocabulary instance
        via magic method __str__.
        """
        self.assertIsInstance(self.vocabulary, Vocabulary)
        self.assertIsNotNone(self.vocabulary)
        self.assertRaises(AttributeError, lambda: self.vocabulary.__name_german)
        self.assertRaises(AttributeError, lambda: self.vocabulary.__name_foreign_language)
        self.assertIs(self.vocabulary.vocabulary_id_property, None)
        self.assertIsNone(self.vocabulary.vocabulary_id_property)
        self.assertEqual(self.vocabulary.name_german_property, "Haus")
        self.assertEqual(self.vocabulary.name_foreign_language_property, "house")
        self.assertEqual(self.vocabulary.language_id_property, 1)
        self.assertEqual(str(self.vocabulary), "None Haus house 1")


if __name__ == "__main__":
    unittest.main()
