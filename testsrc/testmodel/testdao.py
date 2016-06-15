"""
Module with class DAOTest, which inherits from unittest.TestCase
"""

from src.model.dao import DAO
from src.model.user import User
from src.model.language import Language
from src.model.vocabulary import Vocabulary
import unittest


class DAOTest(unittest.TestCase):
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 13.06.2016
    @summary: Test case for class DAO, using PyUnit test framework.
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
        create test database and test objects
        """
        print("setUp")
        DAO()  # Create database tables, if db does not exists
        self.user = User("Ada", "Lovelace", "heart", "444444")
        self.language = Language("English", 1)
        self.vocabulary = Vocabulary("Haus", "house", 1)
        print(self.user)
        print(self.language)
        print(self.vocabulary)

    def tearDown(self):
        """
        clean-up steps, after each test case
        delete instances of class User, Language, Vocabulary
        """
        print("tearDown")
        del self.user
        del self.language
        del self.vocabulary
        self.assertRaises(AttributeError, lambda: print(self.user))
        self.assertRaises(AttributeError, lambda: print(self.language))
        self.assertRaises(AttributeError, lambda: print(self.vocabulary))

    def test_crud_operations(self):
        """
        test method for CRUD operations
        """
        # CRUD for user
        self.assertTrue(DAO.create_user(self.user))
        user_lovelace = DAO.read_user("heart")
        self.assertIsNotNone(user_lovelace)
        self.assertIsInstance(user_lovelace, User)
        user_list = DAO.read_all_users()
        self.assertEqual(len(user_list), 1)
        self.assertEqual(user_lovelace.user_id_property, user_list[0].user_id_property)
        self.assertEqual(user_lovelace.first_name_property, user_list[0].first_name_property)
        self.assertEqual(user_lovelace.last_name_property, user_list[0].last_name_property)
        self.assertEqual(user_lovelace.nickname_property, user_list[0].nickname_property)
        self.assertEqual(user_lovelace.password_property, user_list[0].password_property)
        user_lovelace.nickname_property = "Bernoulli numbers"
        self.assertTrue(DAO.update_user(user_lovelace))
        user_list = DAO.read_all_users()
        self.assertEqual(user_list[0].nickname_property, "Bernoulli numbers")
        DAO.delete_user(user_list[0])
        user_list = DAO.read_all_users()
        self.assertEqual(len(user_list), 0)
        user_lovelace = DAO.read_user("Bernoulli numbers")
        self.assertIsNone(user_lovelace)

        # CRUD for language
        self.assertTrue(DAO.create_user(self.user))
        user_lovelace = DAO.read_user("heart")
        self.assertIsNotNone(user_lovelace)
        self.assertIsInstance(user_lovelace, User)
        self.assertEqual(user_lovelace.first_name_property, "Ada")
        self.assertEqual(user_lovelace.last_name_property, "Lovelace")
        DAO.create_language(user_lovelace, self.language)
        language_list = DAO.read_all_languages_of_one_user(user_lovelace)
        self.assertEqual(len(language_list), 1)
        self.assertEqual(self.language.name_property, language_list[0].name_property)
        language_list[0].name_property = "French"
        DAO.update_language(language_list[0])
        language_list = DAO.read_all_languages_of_one_user(user_lovelace)
        self.assertEqual(language_list[0].name_property, "French")
        DAO.delete_language(language_list[0])
        language_list = DAO.read_all_languages_of_one_user(user_lovelace)
        self.assertEqual(len(language_list), 0)
        DAO.delete_user(user_lovelace)

        # CRUD for vocabulary
        self.assertTrue(DAO.create_user(self.user))
        user_lovelace = DAO.read_user("heart")
        self.assertIsNotNone(user_lovelace)
        self.assertIsInstance(user_lovelace, User)
        self.assertEqual(user_lovelace.first_name_property, "Ada")
        self.assertEqual(user_lovelace.last_name_property, "Lovelace")
        DAO.create_language(user_lovelace, self.language)
        language_list = DAO.read_all_languages_of_one_user(user_lovelace)
        self.assertEqual(len(language_list), 1)
        DAO.create_vocabulary(language_list[0], self.vocabulary)
        vocabulary_list = DAO.read_all_vocabularies_to_one_language_id(language_list[0])
        self.assertEqual(len(vocabulary_list), 1)
        self.assertEqual(vocabulary_list[0].name_german_property, "Haus")
        self.assertEqual(vocabulary_list[0].name_foreign_language_property, "house")
        vocabulary_list[0].name_german_property = "Baum"
        vocabulary_list[0].name_foreign_language_property = "tree"
        DAO.update_vocabulary(vocabulary_list[0])
        vocabulary_list = DAO.read_all_vocabularies_to_one_language_id(language_list[0])
        self.assertEqual(vocabulary_list[0].name_german_property, "Baum")
        self.assertEqual(vocabulary_list[0].name_foreign_language_property, "tree")
        DAO.delete_vocabulary(vocabulary_list[0])
        vocabulary_list = DAO.read_all_vocabularies_to_one_language_id(language_list[0])
        self.assertEqual(len(vocabulary_list), 0)
        DAO.delete_language(language_list[0])
        DAO.delete_user(user_lovelace)


if __name__ == "__main__":
    unittest.main()
