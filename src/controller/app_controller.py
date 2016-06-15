"""
Module with class AppController
MVC pattern: the controller
"""

from gi.repository import Gtk, GLib
from ..view.app_gui import VocabularyTrainerWindow
from ..model.user import User
from ..model.language import Language
from ..model.vocabulary import Vocabulary
from ..model.dao import DAO
import re
from hashlib import md5
import random


class AppController:
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 12.06.2016
    @summary: This class defines all callback functions, which are needed in the view
              for registration on widgets with connect method.
              Invoking the constructor of this class starts the application. GTK is an
              event driven toolkit, which means it will sleep in Gtk.main() loop until
              an event occurs and control is passed to a callback function.
              The Controller changes the view and reacts to user interaction.
              Furthermore the controller contains the program logic of vocabulary test.
              The Controller uses the CRUD operations of DAO class (Data Access Object) for
              Data Manipulation in sqlite3 database tables.
              The Model contains the business classes User, Language and Vocabulary and
              the DAO class for access to database file.
    @see: http://stackoverflow.com/questions/29923621/gtk-python-display-message-for-given-time
    """

    def __init__(self):
        """
        constructor of class AppController
        """
        self.win = VocabularyTrainerWindow(self.get_to_register_page,
                                           self.get_to_login_page,
                                           self.get_to_crud_vocabulary,
                                           self.get_to_crud_language,
                                           self.register_clicked,
                                           self.get_to_welcome_page,
                                           self.login_clicked,
                                           self.language_selected,
                                           self.direction_selected,
                                           self.start_training,
                                           self.stop_test,
                                           self.vocabulary_record_selected,
                                           self.create_vocabulary,
                                           self.read_all_vocabulary,
                                           self.update_vocabulary,
                                           self.delete_vocabulary,
                                           self.language_record_selected,
                                           self.create_language,
                                           self.read_all_language,
                                           self.update_language,
                                           self.delete_language,
                                           self.user_record_selected,
                                           self.read_all_user,
                                           self.update_user,
                                           self.delete_user,
                                           self.from_admin_vocabulary_to_preparation,
                                           self.from_admin_language_to_preparation,
                                           self.next_vocabulary_test)
        """
        @ivar self.win: instance variable of type VocabularyTrainerWindow, this is the place,
                        where the callback functions, defined in class AppController, are passed to
                        the view, that means class VocabularyTrainerWindow. It`s a composition.
        @type self.win: VocabularyTrainerWindow
        """
        self.direction_of_asking = False
        """
        @ivar self.direction_of_asking: instance variable. Is a Radiobutton chosen on preparation page ?
                                        The direction says, if words are asked in German or foreign language.
        @type self.direction_of_asking: bool
        """
        self.language_choice = False
        """
        @ivar self.language_choice: instance variable, Gtk.ComboBox on preparation page offers to choose a
                                    language from a list of languages. Is a language selected ?
        @type self.language_choice: bool
        """
        self.language_instance_combobox = None
        """
        @ivar self.language_instance_combobox: instance variable, to remember the chosen language instance.
        @type self.language_instance_combobox: NoneType, after a language is chosen, type Language
        """
        self.which_language_first = ""
        """
        @ivar self.which_language_first: instance variable, to remember, whether the words are asked in German or not.
        @type self.which_language_first: str
        """
        self.actual_user_nickname = ""
        """
        @ivar self.actual_user_nickname: nickname of user
        @type self.actual_user_nickname: str
        """
        self.vocabulary_list_test = []
        """
        @ivar self.vocabulary_list_test: a list of vocabularies, that are asked in test
        @type self.vocabulary_list_test: list
        """
        self.actual_vocabulary_test = None
        """
        @ivar self.actual_vocabulary_test: actual vocabulary, which is asked
        @type self.actual_vocabulary_test: NoneType, as initial value None, then type Vocabulary
        """
        self.random_index_test = None
        """
        @ivar self.random_index_test: a random index to ask a vocabulary
        @type self.random_index_test: int
        """
        self.win.connect("delete-event", Gtk.main_quit)  # delete event signal of the top level window
        # Gtk.main_quit function terminate the application
        self.win.show_all()
        Gtk.main()  # main loop, waiting for user input

    def get_to_register_page(self, button_widget):
        """
        change view, welcome page -> register page, uses next_page() method on
        Gtk.Notebook
        @param button_widget: Gtk.Button, which is clicked
        @type button_widget: Gtk.Button
        """
        print(button_widget, "get_to_register_page")
        self.win.notebook.next_page()

    def get_to_login_page(self, button_widget):
        """
        change view, welcome page -> login page, uses set_current_page() method on
        Gtk.Notebook
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "get_to_login_page")
        self.win.notebook.set_current_page(2)

    def get_to_crud_vocabulary(self, button_widget):
        """
        change view, preparation page -> administrate vocabulary page, show all
        vocabularies to chosen language, reset the preparation page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """

        def remove_message():
            self.win.message_preparation.set_label("Dummy")
            self.win.vbox_preparation_of_test.remove(self.win.hbox_message_preparation)
            self.win.start_test_button.set_sensitive(True)
            self.win.get_to_crud_vocabulary_page_button.set_sensitive(True)

        if self.language_choice:
            print(button_widget, "get_to_crud_vocabulary")
            self.read_all_vocabulary()
            self.win.notebook.set_current_page(5)
            self.win.languages_combobox.set_active(-1)
            self.win.radiobutton_de_foreign_language.set_label("DE -> Foreign language")
            self.win.radiobutton_foreign_language_de.set_label("Foreign language -> DE")
            self.win.radiobutton_dummy.set_active(True)
            self.language_choice = False
            self.direction_of_asking = False
        else:
            self.win.message_preparation.set_label("Choose a language, please")
            self.win.vbox_preparation_of_test.pack_start(self.win.hbox_message_preparation, False, False, 0)
            self.win.vbox_preparation_of_test.show_all()
            self.win.start_test_button.set_sensitive(False)
            self.win.get_to_crud_vocabulary_page_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def get_to_crud_language(self, button_widget):
        """
        change view, preparation page -> administrate language page, show all
        languages to one user
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "get_to_crud_language")
        self.read_all_language()
        self.win.notebook.set_current_page(6)

    def register_clicked(self, button_widget):
        """
        register page, register button
        Create a new user for application.
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """

        def remove_message():
            self.win.message_register.set_label("Dummy")
            self.win.vbox_register.remove(self.win.hbox_message_register)
            self.win.register_button.set_sensitive(True)

        def remove_first_name_error():
            self.win.layout_register.remove(first_name_error_label)

        def remove_last_name_error():
            self.win.layout_register.remove(last_name_error_label)

        def remove_nickname_error():
            self.win.layout_register.remove(nickname_error_label)

        def remove_password_error():
            self.win.layout_register.remove(password_error_label)

        print(button_widget, "register_clicked")
        first_name = self.win.register_first_name_entry.get_text().strip()
        last_name = self.win.register_last_name_entry.get_text().strip()
        nickname = self.win.register_nickname_entry.get_text().strip()
        password = self.win.register_password_entry.get_text().strip()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S{3,}", re.ASCII)
        compiled_pattern_password = re.compile(r"\S{6,}", re.ASCII)

        if not compiled_pattern_name.search(first_name):
            first_name_error_label = Gtk.Label()
            first_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_register.put(first_name_error_label, 506, 180)
            GLib.timeout_add_seconds(2, remove_first_name_error)

        if not compiled_pattern_name.search(last_name):
            last_name_error_label = Gtk.Label()
            last_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_register.put(last_name_error_label, 506, 230)
            GLib.timeout_add_seconds(2, remove_last_name_error)

        if not compiled_pattern_name.search(nickname) or \
                (nickname == "root" and DAO.read_user("root") is not None):
            nickname_error_label = Gtk.Label()
            nickname_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_register.put(nickname_error_label, 506, 280)
            GLib.timeout_add_seconds(2, remove_nickname_error)

        if not compiled_pattern_password.search(password):
            password_error_label = Gtk.Label()
            password_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_register.put(password_error_label, 506, 330)
            GLib.timeout_add_seconds(2, remove_password_error)

        if not compiled_pattern_name.search(first_name) or \
                not compiled_pattern_name.search(last_name) or \
                not compiled_pattern_name.search(nickname) or \
                not compiled_pattern_password.search(password) or \
                (nickname == "root" and DAO.read_user("root") is not None):
            self.win.message_register.set_label(
                "Names must contain at least 3 characters, the password 6.\nnickname can not be root.")
            self.win.vbox_register.pack_start(self.win.hbox_message_register, False, False, 0)
            self.win.vbox_register.show_all()
            self.win.register_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        user = User(first_name, last_name, nickname, password)

        if DAO.create_user(user):
            print(user)
            print("Create user, done !")
            self.win.register_first_name_entry.set_text("")
            self.win.register_last_name_entry.set_text("")
            self.win.register_nickname_entry.set_text("")
            self.win.register_password_entry.set_text("")
            self.win.notebook.next_page()
        else:
            self.win.message_register.set_label(
                "The nickname must be unique. Another user has the nickname.")
            self.win.vbox_register.pack_start(self.win.hbox_message_register, False, False, 0)
            self.win.vbox_register.show_all()
            self.win.register_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def get_to_welcome_page(self, button_widget):
        """
        register page -> welcome page, login page -> welcome page,
        clear entries on register page / login page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "get_to_welcome_page")

        self.win.register_first_name_entry.set_text("")
        self.win.register_last_name_entry.set_text("")
        self.win.register_nickname_entry.set_text("")
        self.win.register_password_entry.set_text("")

        self.win.login_user_entry.set_text("")
        self.win.login_password_entry.set_text("")

        self.win.notebook.set_current_page(0)

    def login_clicked(self, button_widget):
        """
        login button on login page
        Login to use the application.
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """

        def remove_ok_icon():
            self.win.layout_login.remove(self.win.ok_icon)
            self.win.login_button.set_sensitive(True)
            language_list = DAO.read_all_languages_of_one_user(user)
            for language in language_list:
                self.win.store_language_combobox_preparation.append([language.language_id_property,
                                                                     language.name_property,
                                                                     language.user_id_property])
            if user.nickname_property == "root":
                self.win.notebook.set_current_page(7)
            elif language_list:
                self.win.notebook.next_page()
            else:
                self.win.notebook.set_current_page(6)
            self.win.login_user_entry.set_text("")
            self.win.login_password_entry.set_text("")

        def remove_wrong_icon():
            self.win.layout_login.remove(self.win.wrong_icon)
            self.win.login_button.set_sensitive(True)

        print(button_widget, "login_clicked")
        nickname = self.win.login_user_entry.get_text()
        password = self.win.login_password_entry.get_text()

        user = DAO.read_user(nickname)

        if user is not None:
            if md5(bytes(password, "utf-8")).hexdigest() == user.password_property:
                print("Login:", user)
                self.actual_user_nickname = user.nickname_property
                self.win.layout_login.put(self.win.ok_icon, 306, 250)
                self.win.layout_login.show_all()
                self.win.login_button.set_sensitive(False)
                GLib.timeout_add_seconds(2, remove_ok_icon)
            else:
                print("User exists, wrong password.")
                self.win.layout_login.put(self.win.wrong_icon, 306, 250)
                self.win.layout_login.show_all()
                self.win.login_button.set_sensitive(False)
                GLib.timeout_add_seconds(2, remove_wrong_icon)
        else:
            print("User does not exist.")
            self.win.layout_login.put(self.win.wrong_icon, 306, 250)
            self.win.layout_login.show_all()
            self.win.login_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_wrong_icon)

    def language_selected(self, languages_combobox):
        """
        Gtk.ComboBox on preparation page, list of different languages:
        language_id, language_name, user_id.
        The user can select a language for the test.
        @param languages_combobox: selected item
        @type languages_combobox: Gtk.ComboBox
        """
        print("Combobox, language_selected")
        itr = languages_combobox.get_active_iter()

        if itr is not None:
            model = languages_combobox.get_model()
            language_id, language_name, user_id = \
                model.get_value(itr, 0), model.get_value(itr, 1), model.get_value(itr, 2)
            print("language_id: {} language_name: {} user_id: {}".format(language_id,
                                                                         language_name,
                                                                         user_id))
            self.language_instance_combobox = Language(language_name, user_id, language_id)
            self.win.foreign_language_label.set_text(language_name)
            self.win.foreign_language_label_crud_vocabulary.set_text(language_name)
            self.win.column_title_crud_vocabulary.set_title(language_name)
            self.win.radiobutton_de_foreign_language.set_label("DE -> {}".format(language_name))
            self.win.radiobutton_foreign_language_de.set_label("{} -> DE".format(language_name))
        self.language_choice = True

    def direction_selected(self, radiobutton):
        """
        Radiobuttons on preparation page
        Decide, if vocabularies asked in German or foreign language
        @param radiobutton: selected Gtk.RadioButton
        @type radiobutton: Gtk.RadioButton
        """
        # print("direction_selected")
        if radiobutton.get_active():
            label_chosen = radiobutton.get_label()
            l = [x.strip() for x in label_chosen.split("->")]
            self.which_language_first = l[0]
            print("{} is active.".format(radiobutton.get_label()))
            print("Words in '{}' are given.".format(self.which_language_first))
            self.direction_of_asking = True

    def start_training(self, button_widget):
        """
        change view, preparation page -> test page, ask first vocabulary
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """

        def remove_message():
            self.win.message_preparation.set_label("Dummy")
            self.win.vbox_preparation_of_test.remove(self.win.hbox_message_preparation)
            self.win.start_test_button.set_sensitive(True)
            self.win.get_to_crud_vocabulary_page_button.set_sensitive(True)

        if self.language_choice and self.direction_of_asking:
            print(button_widget, "start_training")
            self.vocabulary_list_test = DAO.read_all_vocabularies_to_one_language_id(self.language_instance_combobox)
            self.win.test_info_label. \
                set_markup("<span size='38000' color='green'>{} vocabularies to learn !</span>"
                           .format(len(self.vocabulary_list_test)))
            if self.vocabulary_list_test:
                self.random_index_test = random.randint(0, len(self.vocabulary_list_test) - 1)
                self.actual_vocabulary_test = self.vocabulary_list_test[self.random_index_test]
                if self.which_language_first == "DE":
                    self.win.german_entry_test.set_text(self.actual_vocabulary_test.name_german_property)
                else:
                    self.win.foreign_language_entry_test. \
                        set_text(self.actual_vocabulary_test.name_foreign_language_property)
            else:
                print("Work done !")
            self.win.notebook.next_page()
            self.win.languages_combobox.set_active(-1)
            self.win.radiobutton_de_foreign_language.set_label("DE -> Foreign language")
            self.win.radiobutton_foreign_language_de.set_label("Foreign language -> DE")
            self.win.radiobutton_dummy.set_active(True)
            self.language_choice = False
            self.direction_of_asking = False
        else:
            if not self.language_choice:
                self.win.message_preparation.set_label("Choose a language, please !")
            else:
                self.win.message_preparation.set_label("Select a Radio-Button, please !")
            self.win.vbox_preparation_of_test.pack_start(self.win.hbox_message_preparation, False, False, 0)
            self.win.vbox_preparation_of_test.show_all()
            self.win.start_test_button.set_sensitive(False)
            self.win.get_to_crud_vocabulary_page_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def stop_test(self, button_widget):
        """
        change view, test page -> preparation page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "stop_test")
        self.win.foreign_language_entry_test.set_text("")
        self.win.german_entry_test.set_text("")
        self.win.notebook.set_current_page(3)

    def next_vocabulary_test(self, button_widget):
        """
        next button on test page
        Evaluate user input, ask next vocabulary.
        If answer is correct, the vocabulary will not be asked again.
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "next_vocabulary_test")

        def remove_ok_icon():
            self.win.foreign_language_entry_test.set_text("")
            self.win.german_entry_test.set_text("")
            self.win.layout_test.remove(self.win.ok_icon)
            self.win.next_button_test.set_sensitive(True)
            self.win.stop_button_test.set_sensitive(True)
            new_question()

        def remove_wrong_icon():
            self.win.foreign_language_entry_test.set_text("")
            self.win.german_entry_test.set_text("")
            self.win.layout_test.remove(self.win.wrong_icon)
            self.win.next_button_test.set_sensitive(True)
            self.win.stop_button_test.set_sensitive(True)
            new_question()

        def show_ok_icon():
            self.win.layout_test.put(self.win.ok_icon, 306, 150)
            self.win.layout_test.show_all()
            self.win.next_button_test.set_sensitive(False)
            self.win.stop_button_test.set_sensitive(False)

        def show_wrong_icon():
            self.win.foreign_language_entry_test. \
                set_text(self.actual_vocabulary_test.name_foreign_language_property)
            self.win.german_entry_test. \
                set_text(self.actual_vocabulary_test.name_german_property)
            self.win.layout_test.put(self.win.wrong_icon, 306, 150)
            self.win.layout_test.show_all()
            self.win.next_button_test.set_sensitive(False)
            self.win.stop_button_test.set_sensitive(False)

        def new_question():
            if self.vocabulary_list_test:
                result = random.randint(0, len(self.vocabulary_list_test) - 1)
                while self.random_index_test == result and len(self.vocabulary_list_test) > 1:
                    result = random.randint(0, len(self.vocabulary_list_test) - 1)
                self.random_index_test = result
                self.actual_vocabulary_test = self.vocabulary_list_test[self.random_index_test]
                if self.which_language_first == "DE":
                    self.win.german_entry_test.set_text(self.actual_vocabulary_test.name_german_property)
                else:
                    self.win.foreign_language_entry_test. \
                        set_text(self.actual_vocabulary_test.name_foreign_language_property)
            else:
                print("Work done !")
                self.win.test_info_label. \
                    set_markup("<span size='38000' color='green'>Work done !</span>")
                self.actual_vocabulary_test = None

        if self.actual_vocabulary_test is not None:
            if self.which_language_first == "DE":
                if self.win.foreign_language_entry_test.get_text().strip() == \
                        self.actual_vocabulary_test.name_foreign_language_property:
                    print("removed:", self.vocabulary_list_test.pop(self.random_index_test))
                    self.win.test_info_label. \
                        set_markup("<span size='38000' color='green'>{} vocabularies to learn !</span>"
                                   .format(len(self.vocabulary_list_test)))
                    show_ok_icon()
                    GLib.timeout_add_seconds(2, remove_ok_icon)
                else:
                    show_wrong_icon()
                    GLib.timeout_add_seconds(2, remove_wrong_icon)
            else:
                if self.win.german_entry_test.get_text().strip() == \
                        self.actual_vocabulary_test.name_german_property:
                    print("removed:", self.vocabulary_list_test.pop(self.random_index_test))
                    self.win.test_info_label. \
                        set_markup("<span size='38000' color='green'>{} vocabularies to learn !</span>"
                                   .format(len(self.vocabulary_list_test)))
                    show_ok_icon()
                    GLib.timeout_add_seconds(2, remove_ok_icon)
                else:
                    show_wrong_icon()
                    GLib.timeout_add_seconds(2, remove_wrong_icon)

    def vocabulary_record_selected(self, treeview_widget):
        """
        select data in Gtk.TreeView on administrate vocabulary page
        @param treeview_widget: selected row
        @type treeview_widget: Gtk.TreeView
        """
        print(treeview_widget, "vocabulary_record_selected")
        model, itr = treeview_widget.get_selected()
        if itr is not None:
            print(model[itr][0], model[itr][1], model[itr][2], model[itr][3])
            self.win.vocabulary_id_entry_crud_vocabulary.set_text(str(model[itr][0]))
            self.win.german_entry_crud_vocabulary.set_text(model[itr][1])
            self.win.foreign_language_entry_crud_vocabulary.set_text(model[itr][2])
            self.win.language_id_entry_crud_vocabulary.set_text(str(model[itr][3]))

    def create_vocabulary(self, button_widget):
        """
        create button on administrate vocabulary page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "create_vocabulary")

        def remove_message():
            self.win.message_vocabulary.set_label("Dummy")
            self.win.vbox_administrate_vocabulary.remove(self.win.hbox_message_crud_vocabulary)
            self.win.create_vocabulary_button.set_sensitive(True)
            self.win.update_vocabulary_button.set_sensitive(True)
            self.win.delete_vocabulary_button.set_sensitive(True)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(True)

        def remove_german_name_error():
            self.win.layout_administration_vocabulary.remove(german_name_error_label)

        def remove_foreign_language_name_error():
            self.win.layout_administration_vocabulary.remove(foreign_language_name_error_label)

        german_name = self.win.german_entry_crud_vocabulary.get_text().strip()
        foreign_language_name = self.win.foreign_language_entry_crud_vocabulary.get_text().strip()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S+", re.ASCII)

        if not compiled_pattern_name.search(german_name):
            german_name_error_label = Gtk.Label()
            german_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_vocabulary.put(german_name_error_label, 506, 0)  # 506, 50
            GLib.timeout_add_seconds(2, remove_german_name_error)

        if not compiled_pattern_name.search(foreign_language_name):
            foreign_language_name_error_label = Gtk.Label()
            foreign_language_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_vocabulary.put(foreign_language_name_error_label, 506, 50)  # 506, 100
            GLib.timeout_add_seconds(2, remove_foreign_language_name_error)

        if not compiled_pattern_name.search(german_name) or \
                not compiled_pattern_name.search(foreign_language_name):
            self.win.message_vocabulary.set_label(
                "Vocabularies must contain at least 1 character.")
            self.win.vbox_administrate_vocabulary.pack_start(self.win.hbox_message_crud_vocabulary, False, False, 0)
            self.win.vbox_administrate_vocabulary.show_all()
            self.win.create_vocabulary_button.set_sensitive(False)
            self.win.update_vocabulary_button.set_sensitive(False)
            self.win.delete_vocabulary_button.set_sensitive(False)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        if self.language_instance_combobox is not None:
            vocabulary = Vocabulary(german_name, foreign_language_name,
                                    self.language_instance_combobox.language_id_property)
            DAO.create_vocabulary(self.language_instance_combobox, vocabulary)
            print(self.language_instance_combobox)
            print(vocabulary)
            print("Create vocabulary, done !")
            self.read_all_vocabulary()
        else:
            print("Language is not selected.")

    def read_all_vocabulary(self, button_widget=None):
        """
        read all / clear entries button on administrate vocabulary page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "read_all_vocabulary")
        self.win.store_vocabulary.clear()

        if self.language_instance_combobox is not None:
            vocabulary_list = DAO.read_all_vocabularies_to_one_language_id(self.language_instance_combobox)

            for vocabulary in vocabulary_list:
                self.win.store_vocabulary.append((vocabulary.vocabulary_id_property,
                                                  vocabulary.name_german_property,
                                                  vocabulary.name_foreign_language_property,
                                                  vocabulary.language_id_property))

            self.win.vocabulary_id_entry_crud_vocabulary.set_text("")
            self.win.german_entry_crud_vocabulary.set_text("")
            self.win.foreign_language_entry_crud_vocabulary.set_text("")
            self.win.language_id_entry_crud_vocabulary.set_text("")
            self.win.tree_vocabulary.get_selection().unselect_all()
        else:
            print("Language is not selected.")

    def update_vocabulary(self, button_widget):
        """
        update button on administrate vocabulary page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "update_vocabulary")

        def remove_message():
            self.win.message_vocabulary.set_label("Dummy")
            self.win.vbox_administrate_vocabulary.remove(self.win.hbox_message_crud_vocabulary)
            self.win.create_vocabulary_button.set_sensitive(True)
            self.win.update_vocabulary_button.set_sensitive(True)
            self.win.delete_vocabulary_button.set_sensitive(True)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(True)

        def remove_german_name_error():
            self.win.layout_administration_vocabulary.remove(german_name_error_label)

        def remove_foreign_language_name_error():
            self.win.layout_administration_vocabulary.remove(foreign_language_name_error_label)

        vocabulary_id_string = self.win.vocabulary_id_entry_crud_vocabulary.get_text()
        german_name = self.win.german_entry_crud_vocabulary.get_text().strip()
        foreign_language_name = self.win.foreign_language_entry_crud_vocabulary.get_text().strip()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S+", re.ASCII)

        if not compiled_pattern_name.search(german_name):
            german_name_error_label = Gtk.Label()
            german_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_vocabulary.put(german_name_error_label, 506, 0)  # 506, 50
            GLib.timeout_add_seconds(2, remove_german_name_error)

        if not compiled_pattern_name.search(foreign_language_name):
            foreign_language_name_error_label = Gtk.Label()
            foreign_language_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_vocabulary.put(foreign_language_name_error_label, 506, 50)  # 506, 100
            GLib.timeout_add_seconds(2, remove_foreign_language_name_error)

        if not vocabulary_id_string or not compiled_pattern_name.search(german_name) or \
                not compiled_pattern_name.search(foreign_language_name):
            if not vocabulary_id_string:
                self.win.message_vocabulary.set_label(
                    "Select a data record")
            else:
                self.win.message_vocabulary.set_label(
                    "Incorrect data")
            self.win.vbox_administrate_vocabulary.pack_start(self.win.hbox_message_crud_vocabulary, False, False, 0)
            self.win.vbox_administrate_vocabulary.show_all()
            self.win.create_vocabulary_button.set_sensitive(False)
            self.win.update_vocabulary_button.set_sensitive(False)
            self.win.delete_vocabulary_button.set_sensitive(False)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        if self.language_instance_combobox is not None:
            vocabulary = Vocabulary(german_name, foreign_language_name,
                                    self.language_instance_combobox.language_id_property,
                                    int(vocabulary_id_string))
            DAO.update_vocabulary(vocabulary)
            print(self.language_instance_combobox)
            print(vocabulary)
            print("Update vocabulary, done !")
            self.read_all_vocabulary()
        else:
            print("Language is not selected.")

    def delete_vocabulary(self, button_widget):
        """
        delete button on administrate vocabulary page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "delete_vocabulary")

        def remove_message():
            self.win.message_vocabulary.set_label("Dummy")
            self.win.vbox_administrate_vocabulary.remove(self.win.hbox_message_crud_vocabulary)
            self.win.create_vocabulary_button.set_sensitive(True)
            self.win.update_vocabulary_button.set_sensitive(True)
            self.win.delete_vocabulary_button.set_sensitive(True)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(True)

        vocabulary_id_string = self.win.vocabulary_id_entry_crud_vocabulary.get_text()
        german_name = self.win.german_entry_crud_vocabulary.get_text().strip()
        foreign_language_name = self.win.foreign_language_entry_crud_vocabulary.get_text().strip()

        if vocabulary_id_string:
            if self.language_instance_combobox is not None:
                vocabulary = Vocabulary(german_name, foreign_language_name,
                                        self.language_instance_combobox.language_id_property,
                                        int(vocabulary_id_string))
                DAO.delete_vocabulary(vocabulary)
                print("Delete vocabulary, done !")
                self.read_all_vocabulary()
        else:
            self.win.message_vocabulary.set_label("Choose a data record for delete.")
            self.win.vbox_administrate_vocabulary.pack_start(self.win.hbox_message_crud_vocabulary, False, False, 0)
            self.win.vbox_administrate_vocabulary.show_all()
            self.win.create_vocabulary_button.set_sensitive(False)
            self.win.update_vocabulary_button.set_sensitive(False)
            self.win.delete_vocabulary_button.set_sensitive(False)
            self.win.from_admin_vocabulary_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def language_record_selected(self, treeview_widget):
        """
        select data in Gtk.TreeView on administrate language page
        @param treeview_widget: selected row
        @type treeview_widget: Gtk.TreeView
        """
        print(treeview_widget, "language_record_selected")
        model, itr = treeview_widget.get_selected()
        if itr is not None:
            print(model[itr][0], model[itr][1], model[itr][2])
            self.win.language_id_entry_crud_language.set_text(str(model[itr][0]))
            self.win.language_name_entry_crud_language.set_text(model[itr][1])
            self.win.user_id_entry_crud_language.set_text(str(model[itr][2]))

    def create_language(self, button_widget):
        """
        create button on administrate language page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "create_language")

        def remove_message():
            self.win.message_language.set_label("Dummy")
            self.win.vbox_administrate_language.remove(self.win.hbox_message_crud_language)
            self.win.create_language_button.set_sensitive(True)
            self.win.update_language_button.set_sensitive(True)
            self.win.delete_language_button.set_sensitive(True)
            self.win.from_admin_language_to_preparation_button.set_sensitive(True)

        def remove_language_name_error():
            self.win.layout_administration_language.remove(language_name_error_label)

        language_name = self.win.language_name_entry_crud_language.get_text().strip()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S{3,}", re.ASCII)

        if not compiled_pattern_name.search(language_name):
            language_name_error_label = Gtk.Label()
            language_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_language.put(language_name_error_label, 506, 0)  # 506, 50
            GLib.timeout_add_seconds(2, remove_language_name_error)

            self.win.message_language.set_label(
                "Names must contain at least 3 characters.")
            self.win.vbox_administrate_language.pack_start(self.win.hbox_message_crud_language, False, False, 0)
            self.win.vbox_administrate_language.show_all()
            self.win.create_language_button.set_sensitive(False)
            self.win.update_language_button.set_sensitive(False)
            self.win.delete_language_button.set_sensitive(False)
            self.win.from_admin_language_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        user = DAO.read_user(self.actual_user_nickname)

        if user is not None:
            language = Language(language_name, user.user_id_property)
            DAO.create_language(user, language)
            print(language)
            print(user)
            print("Create language, done !")
            self.read_all_language()

    def read_all_language(self, button_widget=None):
        """
        read all / clear entries button on administrate language page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "read_all_language")
        self.win.store_language.clear()

        user = DAO.read_user(self.actual_user_nickname)

        if user is not None:
            language_list = DAO.read_all_languages_of_one_user(user)
            for language in language_list:
                self.win.store_language.append((language.language_id_property,
                                                language.name_property,
                                                language.user_id_property))

            self.win.language_id_entry_crud_language.set_text("")
            self.win.language_name_entry_crud_language.set_text("")
            self.win.user_id_entry_crud_language.set_text("")
            self.win.tree_language.get_selection().unselect_all()

    def update_language(self, button_widget):
        """
        update button on administrate language page
        @param button_widget: clicked Gtk.Button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "update_language")

        def remove_message():
            self.win.message_language.set_label("Dummy")
            self.win.vbox_administrate_language.remove(self.win.hbox_message_crud_language)
            self.win.create_language_button.set_sensitive(True)
            self.win.update_language_button.set_sensitive(True)
            self.win.delete_language_button.set_sensitive(True)
            self.win.from_admin_language_to_preparation_button.set_sensitive(True)

        def remove_language_name_error():
            self.win.layout_administration_language.remove(language_name_error_label)

        language_id_string = self.win.language_id_entry_crud_language.get_text()
        language_name = self.win.language_name_entry_crud_language.get_text().strip()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S{3,}", re.ASCII)

        if not compiled_pattern_name.search(language_name):
            language_name_error_label = Gtk.Label()
            language_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_language.put(language_name_error_label, 506, 0)  # 506, 50
            GLib.timeout_add_seconds(2, remove_language_name_error)

        if not language_id_string or \
                not compiled_pattern_name.search(language_name):
            if not language_id_string:
                self.win.message_language.set_label(
                    "Select a data record")
            else:
                self.win.message_language.set_label(
                    "Incorrect data")
            self.win.vbox_administrate_language.pack_start(self.win.hbox_message_crud_language, False, False, 0)
            self.win.vbox_administrate_language.show_all()
            self.win.create_language_button.set_sensitive(False)
            self.win.update_language_button.set_sensitive(False)
            self.win.delete_language_button.set_sensitive(False)
            self.win.from_admin_language_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        user = DAO.read_user(self.actual_user_nickname)

        if user is not None:
            language = Language(language_name, user.user_id_property, int(language_id_string))
            DAO.update_language(language)
            print(language)
            print(user)
            print("Update language, done !")
            self.read_all_language()

    def delete_language(self, button_widget):
        """
        delete button on administrate language page
        @param button_widget: delete button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "delete_language")

        def remove_message():
            self.win.message_language.set_label("Dummy")
            self.win.vbox_administrate_language.remove(self.win.hbox_message_crud_language)
            self.win.create_language_button.set_sensitive(True)
            self.win.update_language_button.set_sensitive(True)
            self.win.delete_language_button.set_sensitive(True)
            self.win.from_admin_language_to_preparation_button.set_sensitive(True)

        language_id_string = self.win.language_id_entry_crud_language.get_text()
        language_name = self.win.language_name_entry_crud_language.get_text().strip()

        if language_id_string:

            user = DAO.read_user(self.actual_user_nickname)

            if user is not None:
                language = Language(language_name, user.user_id_property, int(language_id_string))
                print(language)
                print(user)
                DAO.delete_language(language)
                print("Delete language, done !")
                self.read_all_language()

        else:
            self.win.message_language.set_label(
                "Choose a data record for delete.")
            self.win.vbox_administrate_language.pack_start(self.win.hbox_message_crud_language, False, False, 0)
            self.win.vbox_administrate_language.show_all()
            self.win.create_language_button.set_sensitive(False)
            self.win.update_language_button.set_sensitive(False)
            self.win.delete_language_button.set_sensitive(False)
            self.win.from_admin_language_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def user_record_selected(self, treeview_widget):
        """
        select data in Gtk.TreeView on administrate user page for root
        @param treeview_widget: selected row
        @type treeview_widget: Gtk.TreeView
        """
        print(treeview_widget, "user_record_selected")
        model, itr = treeview_widget.get_selected()
        if itr is not None:
            # print(model[itr][0], model[itr][1], model[itr][2], model[itr][3], model[itr][4])
            self.win.user_id_entry_crud_user.set_text(str(model[itr][0]))
            self.win.first_name_entry_crud_user.set_text(model[itr][1])
            self.win.last_name_entry_crud_user.set_text(model[itr][2])
            self.win.nickname_entry_crud_user.set_text(model[itr][3])

    def read_all_user(self, button_widget=None):
        """
        read all / clear entries button on administrate user page
        @param button_widget: clicked button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "read_all_user")
        self.win.store_user.clear()
        user_list = DAO.read_all_users()
        for user in user_list:
            self.win.store_user.append((user.user_id_property,
                                        user.first_name_property,
                                        user.last_name_property,
                                        user.nickname_property,
                                        user.password_property))

        self.win.first_name_entry_crud_user.set_text("")
        self.win.last_name_entry_crud_user.set_text("")
        self.win.nickname_entry_crud_user.set_text("")
        self.win.password_entry_crud_user.set_text("")
        self.win.user_id_entry_crud_user.set_text("")
        self.win.tree_user.get_selection().unselect_all()

    def update_user(self, button_widget):
        """
        update button on administrate user page
        @param button_widget: clicked button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "update_user")

        def remove_message():
            self.win.message_user.set_label("Dummy")
            self.win.vbox_administrate_user.remove(self.win.hbox_message_crud_user)
            self.win.update_user_button.set_sensitive(True)
            self.win.delete_user_button.set_sensitive(True)

        def remove_first_name_error():
            self.win.layout_administration_user.remove(first_name_error_label)

        def remove_last_name_error():
            self.win.layout_administration_user.remove(last_name_error_label)

        def remove_nickname_error():
            self.win.layout_administration_user.remove(nickname_error_label)

        def remove_password_error():
            self.win.layout_administration_user.remove(password_error_label)

        first_name = self.win.first_name_entry_crud_user.get_text().strip()
        last_name = self.win.last_name_entry_crud_user.get_text().strip()
        nickname = self.win.nickname_entry_crud_user.get_text().strip()
        password = self.win.password_entry_crud_user.get_text().strip()
        user_id_string = self.win.user_id_entry_crud_user.get_text()

        # \S Matches a Unicode nonwhitespace, or [^ \t\n\r\f\v] with the re.ASCII flag
        # e{m,} Greedily match at least m occurrences of expression e

        compiled_pattern_name = re.compile(r"\S{3,}", re.ASCII)
        compiled_pattern_password = re.compile(r"\S{6,}", re.ASCII)

        if not compiled_pattern_name.search(first_name):
            first_name_error_label = Gtk.Label()
            first_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_user.put(first_name_error_label, 506, 50)
            GLib.timeout_add_seconds(2, remove_first_name_error)

        if not compiled_pattern_name.search(last_name):
            last_name_error_label = Gtk.Label()
            last_name_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_user.put(last_name_error_label, 506, 100)
            GLib.timeout_add_seconds(2, remove_last_name_error)

        if not compiled_pattern_name.search(nickname):
            nickname_error_label = Gtk.Label()
            nickname_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_user.put(nickname_error_label, 506, 150)
            GLib.timeout_add_seconds(2, remove_nickname_error)

        if not compiled_pattern_password.search(password):
            password_error_label = Gtk.Label()
            password_error_label.set_markup("<span size='15000' color='#b30000'>wrong</span>")
            self.win.layout_administration_user.put(password_error_label, 506, 200)
            GLib.timeout_add_seconds(2, remove_password_error)

        if not user_id_string or \
                not compiled_pattern_name.search(first_name) or \
                not compiled_pattern_name.search(last_name) or \
                not compiled_pattern_name.search(nickname) or \
                not compiled_pattern_password.search(password):
            if not user_id_string:
                self.win.message_user.set_label(
                    "Select a data record")
            else:
                self.win.message_user.set_label(
                    "Incorrect data")
            self.win.vbox_administrate_user.pack_start(self.win.hbox_message_crud_user, False, False, 0)
            self.win.vbox_administrate_user.show_all()
            self.win.update_user_button.set_sensitive(False)
            self.win.delete_user_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
            return

        user = User(first_name, last_name, nickname, password, int(user_id_string))

        if DAO.update_user(user):
            print(user)
            print("Update user, done !")
            self.read_all_user()

        else:
            self.win.message_user.set_label(
                "The nickname must be unique. Another user has the nickname.")
            self.win.vbox_administrate_user.pack_start(self.win.hbox_message_crud_user, False, False, 0)
            self.win.vbox_administrate_user.show_all()
            self.win.update_user_button.set_sensitive(False)
            self.win.delete_user_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def delete_user(self, button_widget):
        """
        delete button on administrate user page
        @param button_widget: clicked button
        @type button_widget: Gtk.Button
        """

        def remove_message():
            self.win.message_user.set_label("Dummy")
            self.win.vbox_administrate_user.remove(self.win.hbox_message_crud_user)
            self.win.update_user_button.set_sensitive(True)
            self.win.delete_user_button.set_sensitive(True)

        print(button_widget, "delete_user")
        user_id_string = self.win.user_id_entry_crud_user.get_text()
        nickname = self.win.nickname_entry_crud_user.get_text().strip()

        if user_id_string:

            user = DAO.read_user(nickname)

            if user is not None:
                DAO.delete_user(user)
                print("Delete user, done !")
                self.read_all_user()
            else:
                self.win.message_user.set_label(
                    "Enter correct nickname.")
                self.win.vbox_administrate_user.pack_start(self.win.hbox_message_crud_user, False, False, 0)
                self.win.vbox_administrate_user.show_all()
                self.win.update_user_button.set_sensitive(False)
                self.win.delete_user_button.set_sensitive(False)
                GLib.timeout_add_seconds(2, remove_message)

        else:
            self.win.message_user.set_label(
                "Choose a data record for delete.")
            self.win.vbox_administrate_user.pack_start(self.win.hbox_message_crud_user, False, False, 0)
            self.win.vbox_administrate_user.show_all()
            self.win.update_user_button.set_sensitive(False)
            self.win.delete_user_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)

    def from_admin_vocabulary_to_preparation(self, button_widget):
        """
        change view with back button on administrate vocabulary page
        @param button_widget: clicked button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "from_admin_vocabulary_to_preparation")
        self.win.notebook.set_current_page(3)

    def from_admin_language_to_preparation(self, button_widget):
        """
        change view with back button on administrate language page
        @param button_widget: back button
        @type button_widget: Gtk.Button
        """
        print(button_widget, "from_admin_language_to_preparation")

        def remove_message():
            self.win.message_language.set_label("Dummy")
            self.win.vbox_administrate_language.remove(self.win.hbox_message_crud_language)
            self.win.create_language_button.set_sensitive(True)
            self.win.update_language_button.set_sensitive(True)
            self.win.delete_language_button.set_sensitive(True)
            self.win.from_admin_language_to_preparation_button.set_sensitive(True)

        self.win.store_language_combobox_preparation.clear()
        user = DAO.read_user(self.actual_user_nickname)

        language_list = []

        if user is not None:
            language_list = DAO.read_all_languages_of_one_user(user)

        if language_list:
            for language in language_list:
                self.win.store_language_combobox_preparation.append([language.language_id_property,
                                                                     language.name_property,
                                                                     language.user_id_property])
            self.win.languages_combobox.set_active(-1)
            self.win.radiobutton_de_foreign_language.set_label("DE -> Foreign language")
            self.win.radiobutton_foreign_language_de.set_label("Foreign language -> DE")
            self.win.radiobutton_dummy.set_active(True)
            self.language_choice = False
            self.direction_of_asking = False
            self.win.notebook.set_current_page(3)
        else:
            self.win.message_language.set_label(
                "Create a language !")
            self.win.vbox_administrate_language.pack_start(self.win.hbox_message_crud_language, False, False, 0)
            self.win.vbox_administrate_language.show_all()
            self.win.create_language_button.set_sensitive(False)
            self.win.update_language_button.set_sensitive(False)
            self.win.delete_language_button.set_sensitive(False)
            self.win.from_admin_language_to_preparation_button.set_sensitive(False)
            GLib.timeout_add_seconds(2, remove_message)
