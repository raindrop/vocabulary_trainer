"""
Module with business class Language, part of model.
"""


class Language:
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 12.06.2016
    @summary: This class models a language used in vocabulary trainer. Instead of
              public getters and setters we use public properties to access private
              attributes. getters and setters are private, too. This is a strategy
              to ensure the principle of data encapsulation.
    """

    def __init__(self, name, user_id, language_id=None):
        """
        constructor of class Language, description of method parameters
        @param name: name of language
        @type name: str
        @param user_id: user`s ID
        @type user_id: int
        @param language_id: ID of language, default parameter
        @type language_id: int
        """
        self.__name = name
        """
        @ivar self.__name: private instance variable for language name
        @type self.__name: str
        """
        self.__user_id = user_id
        """
        @ivar self.__user_id: private instance variable for user`s ID
        @type self.__user_id: int
        """
        self.__language_id = language_id
        """
        @ivar self.__language_id: private instance variable for language ID
        @type self.__language_id: int
        """

    def __get_language_id(self):
        """
        private getter for language ID
        @return: language ID
        @rtype: int
        """
        return self.__language_id

    def __set_language_id(self, language_id):
        """
        private setter for language ID
        @param language_id: ID of language
        @type language_id: int
        """
        self.__language_id = language_id

    def __get_name(self):
        """
        private getter for language name
        @return: language name
        @rtype: str
        """
        return self.__name

    def __set_name(self, name):
        """
        private setter for language name
        @param name: language name
        @type name: str
        """
        self.__name = name

    def __get_user_id(self):
        """
        private getter for user`s ID
        @return: user`s ID
        @rtype: int
        """
        return self.__user_id

    def __set_user_id(self, user_id):
        """
        private setter for user`s ID
        @param user_id: user`s ID
        @type user_id: int
        """
        self.__user_id = user_id

    """
    public properties
    """
    language_id_property = property(__get_language_id, __set_language_id)
    name_property = property(__get_name, __set_name)
    user_id_property = property(__get_user_id, __set_user_id)

    def __str__(self):
        """
        String representation of an instance
        @return: string representation
        @rtype: str
        """
        return "{} {} {}".format(self.__language_id, self.__name, self.__user_id)
