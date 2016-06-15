"""
Module with class DAO (Data Access Object), part of model.
"""

from os.path import exists
from .user import User
from .language import Language
from .vocabulary import Vocabulary
from os.path import abspath
import sqlite3


class DAO:
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 13.06.2016
    @summary: DAO class contains the CRUD operations for business objects, like
              User-, Language- or Vocabulary-Objects.
              All methods are static methods, a utility class for data manipulation
              in sqlite3 database tables.
    """
    def __init__(self):
        """
        constructor of DAO class. Invoking the constructor creates database tables,
        if they do not exist.
        """
        print(abspath("../vocabulary_trainer/db.sqlite"))
        if exists(abspath("../vocabulary_trainer/db.sqlite")):
            print("Database exists, nothing to do.")
        else:
            connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
            cursor = connection.cursor()

            sql = "CREATE TABLE user(" \
                  "user_id INTEGER PRIMARY KEY, " \
                  "first_name TEXT NOT NULL, " \
                  "last_name TEXT NOT NULL, " \
                  "nickname TEXT NOT NULL UNIQUE, " \
                  "password TEXT NOT NULL)"

            cursor.execute(sql)

            sql = "CREATE TABLE language(" \
                  "language_id INTEGER PRIMARY KEY, " \
                  "name TEXT NOT NULL, " \
                  "user_id INTEGER, " \
                  "FOREIGN KEY(user_id) REFERENCES user(user_id))"

            cursor.execute(sql)

            sql = "CREATE TABLE vocabulary(" \
                  "vocabulary_id INTEGER PRIMARY KEY, " \
                  "name_german TEXT NOT NULL, " \
                  "name_foreign_language TEXT NOT NULL, " \
                  "language_id INTEGER, " \
                  "FOREIGN KEY(language_id) REFERENCES language(language_id))"

            cursor.execute(sql)

            connection.commit()
            cursor.close()
            connection.close()
            print("Database with tables are created now.")

    # CRUD for user

    @staticmethod
    def create_user(user):
        """
        create operation, object relational mapping: a User object is written
        down as tuple in table user of database file.
        @param user: instance of business class User
        @type user: User
        @return: True, if operation is done, otherwise False
        @rtype: bool
        """
        result = DAO.read_user(user.nickname_property)
        if result is not None:
            print("The nickname must be unique. Another user has the nickname.")
            return False
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO user VALUES(?, ?, ?, ?, ?)""",
                       (None, user.first_name_property, user.last_name_property,
                        user.nickname_property, user.get_md5()))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def read_all_users():
        """
        read all existing user operation
        @return: list of User objects
        @rtype: list, contains instances of type User
        """
        user_list = []
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        for row in cursor:
            user = User(row[1], row[2], row[3], row[4], row[0])
            user_list.append(user)
        cursor.close()
        connection.close()
        return user_list

    @staticmethod
    def read_user(nickname):
        """
        For a given nickname, you can find the user.
        @param nickname: nickname of user
        @type nickname: str
        @return: None, if user with given nickname does not exist, otherwise
                 a User instance.
        @rtype: NoneType or User
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""SELECT *
                          FROM user
                          WHERE nickname = ?""", (nickname,))
        row = cursor.fetchone()
        if row is None:
            print("User with nickname '{}' not found.".format(nickname))
            return None
        user = User(row[1], row[2], row[3], row[4], row[0])
        cursor.close()
        connection.close()
        return user

    @staticmethod
    def update_user(user):
        """
        update operation, change values of a User instance: first name, last name,
        nickname or password.
        @param user: instance of class User
        @type user: User
        @return: True, if operation is done, otherwise False (nickname must be unique).
        @rtype: bool
        """
        result = DAO.read_user(user.nickname_property)
        if result is not None and result.user_id_property != user.user_id_property:
            print("The nickname must be unique. Another user has the nickname.")
            print(user)
            print(result)
            return False
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""UPDATE user
                          SET first_name = ?,
                              last_name = ?,
                              nickname = ?,
                              password = ?
                          WHERE user_id = ?
                       """,
                       (user.first_name_property,
                        user.last_name_property,
                        user.nickname_property,
                        user.get_md5(),
                        user.user_id_property))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    @staticmethod
    def delete_user(user):
        """
        delete operation for user, referential integrity is considered.
        @param user: instance of class User, who should be deleted
        @type user: User
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute(
            """DELETE FROM vocabulary
               WHERE language_id IN (SELECT language_id
                                     FROM language WHERE user_id = ?)""",
            (user.user_id_property,))
        cursor.execute("DELETE FROM language WHERE user_id = {}".format(user.user_id_property))
        cursor.execute("DELETE FROM user WHERE user_id = '{}'".format(user.user_id_property))
        connection.commit()
        cursor.close()
        connection.close()

    # CRUD for language

    @staticmethod
    def create_language(user, language):
        """
        create operation for language
        @param user: instance of class User
        @type user: User
        @param language: instance of class Language
        @type language: Language
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO language VALUES(?, ?, ?)""",
                       (None, language.name_property, user.user_id_property))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def read_all_languages_of_one_user(user):
        """
        result of operation is a list of all languages for one given user
        @param user: instance of class User
        @type user: User
        @return: list of languages, contains instances of class Language
        @rtype: list
        """
        language_list = []
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("SELECT * \
                        FROM language \
                        WHERE user_id = '{}'".format(user.user_id_property))
        for row in cursor:
            language = Language(row[1], row[2], row[0])
            language_list.append(language)
        cursor.close()
        connection.close()
        return language_list

    @staticmethod
    def update_language(language):
        """
        update operation for language, change name of Language instance
        @param language: instance of class Language
        @type language: Language
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""UPDATE language
                          SET name = ?
                          WHERE language_id = ?
                       """,
                       (language.name_property,
                        language.language_id_property))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete_language(language):
        """
        delete operation for language, referential integrity is considered.
        @param language: instance of class Language
        @type language: Language
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vocabulary "
                       "WHERE language_id = {}".format(language.language_id_property))
        cursor.execute("""DELETE FROM language WHERE language_id = ?""",
                       (language.language_id_property,))
        connection.commit()
        cursor.close()
        connection.close()

    # CRUD for vocabulary

    @staticmethod
    def create_vocabulary(language, vocabulary):
        """
        create operation for vocabulary, create a tuple in table vocabulary
        with data of an instance of class Vocabulary.
        @param language: instance of class Language
        @type language: Language
        @param vocabulary: instance of class Vocabulary
        @type vocabulary: Vocabulary
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO vocabulary VALUES(?, ?, ?, ?)""",
                       (None, vocabulary.name_german_property,
                        vocabulary.name_foreign_language_property,
                        language.language_id_property))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def read_all_vocabularies_to_one_language_id(language):
        """
        result of operation is a list of vocabularies
        @param language: instance of class Language
        @type language: Language
        @return: list of instances of class Vocabulary
        @rtype: list, contains type Vocabulary
        """
        vocabulary_list = []
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""SELECT *
                          FROM vocabulary
                          WHERE language_id = ?""", (language.language_id_property,))
        rows = cursor.fetchall()
        for row in rows:
            vocabulary = Vocabulary(row[1], row[2], row[3], row[0])
            vocabulary_list.append(vocabulary)
        cursor.close()
        connection.close()
        return vocabulary_list

    @staticmethod
    def update_vocabulary(vocabulary):
        """
        update operation for vocabulary, change names of vocabulary.
        @param vocabulary: instance of class Vocabulary
        @type vocabulary: Vocabulary
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""UPDATE vocabulary
                          SET name_german = ?,
                              name_foreign_language = ?
                          WHERE vocabulary_id = ?
                       """,
                       (vocabulary.name_german_property,
                        vocabulary.name_foreign_language_property,
                        vocabulary.vocabulary_id_property))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete_vocabulary(vocabulary):
        """
        delete operation for vocabulary
        @param vocabulary: instance of class Vocabulary, which should be deleted.
        @type vocabulary: Vocabulary
        """
        connection = sqlite3.connect(abspath("../vocabulary_trainer/db.sqlite"))
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM vocabulary
                          WHERE vocabulary_id = ?
                       """, (vocabulary.vocabulary_id_property,))
        connection.commit()
        cursor.close()
        connection.close()
