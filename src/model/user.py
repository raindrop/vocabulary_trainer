"""
Module with business class User, part of model.
"""

from hashlib import md5


class User:
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 11.06.2016
    @summary: This class models a user of vocabulary trainer. Instead of
              public getters and setters we use public properties to access
              private attributes. getters and setters are private, too.
              This is a strategy to ensure the principle of data encapsulation.
    """

    def __init__(self, first_name, last_name, nickname, password, user_id=None):
        """
        constructor of class User, description of method parameters
        @param first_name: user`s first name
        @type first_name: str
        @param last_name: user`s last name
        @type last_name: str
        @param nickname: user`s nickname
        @type nickname: The expected type for the parameter is str.
        @param password: user`s password
        @type password: str
        @param user_id: user`s ID, default parameter
        @type user_id: int
        """
        self.__first_name = first_name
        """
        @ivar self.__first_name: private instance variable for first name
        @type self.__first_name: str
        """
        self.__last_name = last_name
        """
        @ivar self.__last_name: private instance variable for last name
        @type self.__last_name: str
        """
        self.__nickname = nickname
        """
        @ivar self.__nickname: private instance variable for nickname
        @type self.__nickname: str
        """
        self.__password = password
        """
        @ivar self.__password: private instance variable for password
        @type self.__password: str
        """
        self.__user_id = user_id
        """
        @ivar self.__user_id: private instance variable for user ID
        @type self.__user_id: int
        """

    def __get_user_id(self):
        """
        private getter for user ID
        @return: user ID
        @rtype: int
        """
        return self.__user_id

    def __set_user_id(self, user_id):
        """
        private setter for user ID
        @param user_id: user`s ID
        @type user_id: int
        """
        self.__user_id = user_id

    def __get_first_name(self):  # private
        """
        private getter for first name
        @return: user`s first name
        @rtype: str
        """
        return self.__first_name

    def __set_first_name(self, first_name):
        """
        private setter for first name
        @param first_name: user`s first name
        @type first_name: str
        """
        self.__first_name = first_name

    def __get_last_name(self):
        """
        private getter for last name
        @return: user`s last name
        @rtype: str
        """
        return self.__last_name

    def __set_last_name(self, last_name):
        """
        private setter for last name
        @param last_name: user`s last name
        @type last_name: str
        """
        self.__last_name = last_name

    def __get_nickname(self):
        """
        private getter for nickname
        @return: user`s nickname
        @rtype: str
        """
        return self.__nickname

    def __set_nickname(self, nickname):
        """
        private setter for nickname
        @param nickname: user`s nickname
        @type nickname: str
        """
        self.__nickname = nickname

    def __get_password(self):
        """
        private getter for password
        @return: user`s password
        @rtype: str
        """
        return self.__password

    def __set_password(self, password):
        """
        private setter for password
        @param password: user`s password
        @type password: str
        """
        self.__password = password

    """
    public properties
    """
    user_id_property = property(__get_user_id, __set_user_id)
    first_name_property = property(__get_first_name, __set_first_name)
    last_name_property = property(__get_last_name, __set_last_name)
    nickname_property = property(__get_nickname, __set_nickname)
    password_property = property(__get_password, __set_password)

    def __str__(self):
        """
        String representation of an instance
        If a class has a __str__ method, the method will be used for an instance of
        that class, if the function str is applied to it or if it is used in a print
        function.
        @return: string representation
        @rtype: str
        """
        return "{} {} {} {} {}".format(self.__user_id, self.__first_name, self.__last_name,
                                       self.__nickname, self.__password)

    def get_md5(self):
        """
        public method to get md5 hash value for password
        @return: md5 hash value
        @rtype: str
        """
        return md5(bytes(self.__password, "utf-8")).hexdigest()
