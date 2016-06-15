"""
Module with business class Vocabulary, part of model.
"""


class Vocabulary:
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 12.06.2016
    @summary: This class models a vocabulary used in vocabulary trainer.
    """

    def __init__(self, name_german, name_foreign_language, language_id, vocabulary_id=None):
        """
        constructor of class Vocabulary, description of method parameters
        @param name_german: german name of vocabulary
        @type name_german: str
        @param name_foreign_language: translation
        @type name_foreign_language: str
        @param language_id: ID of language
        @type language_id: int
        @param vocabulary_id: ID of vocabulary, default parameter with value None
        @type vocabulary_id: int
        """
        self.__name_german = name_german
        """
        @ivar self.__name_german: private instance variable for german name
        @type self.__name_german: str
        """
        self.__name_foreign_language = name_foreign_language
        """
        @ivar self.__name_foreign_language: private instance variable for translation
        @type self.__name_foreign_language: str
        """
        self.__language_id = language_id
        """
        @ivar self.__language_id: private instance variable for language ID
        @type self.__language_id: int
        """
        self.__vocabulary_id = vocabulary_id
        """
        @ivar self.__vocabulary_id: private instance variable for vocabulary ID
        @type self.__vocabulary_id: int
        """

    def __get_vocabulary_id(self):
        """
        private getter for vocabulary ID
        @return: vocabulary ID
        @rtype: int
        """
        return self.__vocabulary_id

    def __set_vocabulary_id(self, vocabulary_id):
        """
        private setter for vocabulary ID
        @param vocabulary_id: ID of vocabulary
        @type vocabulary_id: int
        """
        self.__vocabulary_id = vocabulary_id

    def __get_name_german(self):
        """
        private getter for german name
        @return: german name
        @rtype: str
        """
        return self.__name_german

    def __set_name_german(self, name_german):
        """
        private setter for german name
        @param name_german: german name of vocabulary
        @type name_german: str
        """
        self.__name_german = name_german

    def __get_name_foreign_language(self):
        """
        private getter for translation
        @return: translation
        @rtype: str
        """
        return self.__name_foreign_language

    def __set_name_foreign_language(self, name_foreign_language):
        """
        private setter for translation
        @param name_foreign_language: translation
        @type name_foreign_language: str
        """
        self.__name_foreign_language = name_foreign_language

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

    """
    public properties
    """
    vocabulary_id_property = property(__get_vocabulary_id, __set_vocabulary_id)
    name_german_property = property(__get_name_german, __set_name_german)
    name_foreign_language_property = property(__get_name_foreign_language, __set_name_foreign_language)
    language_id_property = property(__get_language_id, __set_language_id)

    def __str__(self):
        """
        String representation of an instance from this class
        @return: string representation
        @rtype: str
        """
        return "{} {} {} {}".format(self.__vocabulary_id, self.__name_german,
                                    self.__name_foreign_language, self.__language_id)
