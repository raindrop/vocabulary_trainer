"""
Module with class UserTest, which inherits from unittest.TestCase.
"""

from src.model.user import User
from hashlib import md5
import unittest


class UserTest(unittest.TestCase):
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 13.06.2016
    @summary: Test case for class User, using PyUnit test framework.
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
        self.user = User("Tim", "Berners - Lee", "www", "333333")
        print(self.user)

    def tearDown(self):
        """
        clean-up steps, after each test case
        """
        print("tearDown")
        del self.user
        self.assertRaises(AttributeError, lambda: print(self.user))

    def test_information_hiding(self):
        """
        test method, testing properties, get_md5 method and string
        representation of User instance
        """
        self.assertIsInstance(self.user, User)
        self.assertIsNotNone(self.user)
        self.assertRaises(AttributeError, lambda: self.user.__first_name)
        self.assertRaises(AttributeError, lambda: self.user.__last_name)
        self.assertRaises(AttributeError, lambda: self.user.__nickname)
        self.assertRaises(AttributeError, lambda: self.user.__password)
        self.assertIs(self.user.user_id_property, None)
        self.assertIsNone(self.user.user_id_property)
        self.assertEqual(self.user.first_name_property, "Tim")
        self.assertEqual(self.user.last_name_property, "Berners - Lee")
        self.assertEqual(self.user.nickname_property, "www")
        self.assertEqual(self.user.password_property, "333333")
        self.assertEqual(md5(bytes(self.user.password_property, "utf-8")).hexdigest(),
                         self.user.get_md5())
        self.assertEqual(str(self.user), "None Tim Berners - Lee www 333333")


if __name__ == "__main__":
    unittest.main()
