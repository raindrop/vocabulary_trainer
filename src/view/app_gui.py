"""
Module with class VocabularyTrainerWindow, which inherits from class Gtk.Window
MVC pattern: It`s the view.
"""

from gi.repository import Gtk, Gdk
from os.path import abspath


class VocabularyTrainerWindow(Gtk.Window):
    """
    @author: s52748
    @contact: s52748@beuth-hochschule.de
    @version: 12.06.2016
    @summary: This class is a Gtk.Window, which contains a Gtk.Notebook for the different
              views of the application. The Notebook Widget is a collection of pages that
              overlap each other, only one page is visible at a time. It`s similar to
              the CardLayout of Java. With method set_show_tabs(False) you can not see
              the tabs of notebook. Every page of view is built in the constructor:
              Welcome, register, login, preparation, test, administrate vocabulary,
              administrate language, administrate user.
    @see: source of brain image: https://pixabay.com/de/gehirn-wachstum-lernen-denkweise-1295128/
          other images from same site
    """

    def __init__(self, get_to_register_page,
                 get_to_login_page,
                 get_to_crud_vocabulary,
                 get_to_crud_language,
                 register_clicked,
                 get_to_welcome_page,
                 login_clicked,
                 language_selected,
                 direction_selected,
                 start_training,
                 stop_test,
                 vocabulary_record_selected,
                 create_vocabulary,
                 read_all_vocabulary,
                 update_vocabulary,
                 delete_vocabulary,
                 language_record_selected,
                 create_language,
                 read_all_language,
                 update_language,
                 delete_language,
                 user_record_selected,
                 read_all_user,
                 update_user,
                 delete_user,
                 from_admin_vocabulary_to_preparation,
                 from_admin_language_to_preparation,
                 next_vocabulary_test):
        """
        constructor of class VocabularyTrainerWindow, description of method parameters:
        Every parameter of constructor expects a callback function.
        The function is defined in class AppController. In class VocabularyTrainerWindow the
        callbacks are used for event handling. They are registered on widgets with
        the connect method.
        @param get_to_register_page: change view, welcome page -> register page
        @param get_to_login_page: change view, welcome page -> login page
        @param get_to_crud_vocabulary: change view, preparation page -> administrate vocabulary page
        @param get_to_crud_language: change view, preparation page -> administrate language page
        @param register_clicked: register page, register button
        @param get_to_welcome_page: register page -> welcome page, login page -> welcome page
        @param login_clicked: login button on login page
        @param language_selected: Gtk.ComboBox on preparation page
        @param direction_selected: Radiobuttons on preparation page
        @param start_training: change view, preparation page -> test page
        @param stop_test: change view, test page -> preparation page
        @param vocabulary_record_selected: select data in Gtk.TreeView on administrate vocabulary page
        @param create_vocabulary: create button on administrate vocabulary page
        @param read_all_vocabulary: read all / clear entries button on administrate vocabulary page
        @param update_vocabulary: update button on administrate vocabulary page
        @param delete_vocabulary: delete button on administrate vocabulary page
        @param language_record_selected: select data in Gtk.TreeView on administrate language page
        @param create_language: create button on administrate language page
        @param read_all_language: read all / clear entries button on administrate language page
        @param update_language: update button on administrate language page
        @param delete_language: delete button on administrate language page
        @param user_record_selected: select data in Gtk.TreeView on administrate user page for root
        @param read_all_user: read all / clear entries button on administrate user page
        @param update_user: update button on administrate user page
        @param delete_user: delete button on administrate user page
        @param from_admin_vocabulary_to_preparation: change view with back button on administrate vocabulary page
        @param from_admin_language_to_preparation: change view with back button on administrate language page
        @param next_vocabulary_test: next button on test page
        """
        super().__init__(title="Vocabulary Trainer")
        self.set_size_request(700, 750)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        self.add(self.notebook)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(abspath("src/static/css/base.css"))

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.ok_icon = Gtk.Image()
        self.ok_icon.set_from_file(abspath("src/static/images/correct.png"))

        self.wrong_icon = Gtk.Image()
        self.wrong_icon.set_from_file(abspath("src/static/images/incorrect.png"))

        ################################################################################################################
        # Welcome page                                                                                                 #
        ################################################################################################################

        hbox_welcome = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_welcome.set_halign(Gtk.Align.CENTER)
        welcome_label = Gtk.Label()
        welcome_label.set_name("welcome_label")
        welcome_label.set_markup("<span size='38000' color='green'>Welcome !</span>")
        hbox_welcome.add(welcome_label)

        vbox_welcome = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox_welcome.pack_start(hbox_welcome, False, False, 50)

        image_welcome = Gtk.Image()
        image_welcome.set_from_file(abspath("src/static/images/brain.png"))
        vbox_welcome.add(image_welcome)

        hbox_welcome_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_welcome_buttons.set_halign(Gtk.Align.CENTER)
        get_to_register_page_button = Gtk.Button(label="Register page")
        get_to_register_page_button.connect("clicked", get_to_register_page)
        get_to_login_page_button = Gtk.Button(label="Login page")
        get_to_login_page_button.connect("clicked", get_to_login_page)
        hbox_welcome_buttons.add(get_to_register_page_button)
        hbox_welcome_buttons.add(get_to_login_page_button)
        vbox_welcome.pack_start(hbox_welcome_buttons, False, False, 50)

        self.notebook.append_page(vbox_welcome, Gtk.Label("Welcome"))

        ################################################################################################################
        # Register page                                                                                                #
        ################################################################################################################

        self.vbox_register = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(self.vbox_register, Gtk.Label("Register"))

        register_first_name_label = Gtk.Label("First name:")
        register_last_name_label = Gtk.Label("Last name:")
        register_nickname_label = Gtk.Label("Nickname:")
        register_password_label = Gtk.Label("Password:")
        self.register_first_name_entry = Gtk.Entry()
        self.register_first_name_entry.set_placeholder_text("first name")
        self.register_first_name_entry.set_max_length(20)
        self.register_last_name_entry = Gtk.Entry()
        self.register_last_name_entry.set_placeholder_text("last name")
        self.register_last_name_entry.set_max_length(20)
        self.register_nickname_entry = Gtk.Entry()
        self.register_nickname_entry.set_placeholder_text("nickname")
        self.register_nickname_entry.set_max_length(20)
        self.register_password_entry = Gtk.Entry()
        self.register_password_entry.set_placeholder_text("password")
        self.register_password_entry.set_max_length(20)
        self.register_password_entry.set_visibility(False)
        self.register_button = Gtk.Button(label="Register")
        self.register_button.connect("clicked", register_clicked)
        self.from_register_to_welcome_button = Gtk.Button("Welcome page")
        self.from_register_to_welcome_button.connect("clicked", get_to_welcome_page)

        self.layout_register = Gtk.Fixed()
        self.layout_register.put(register_first_name_label, 206, 180)
        self.layout_register.put(register_last_name_label, 206, 230)
        self.layout_register.put(register_nickname_label, 206, 280)
        self.layout_register.put(register_password_label, 206, 330)
        self.layout_register.put(self.register_first_name_entry, 306, 180)
        self.layout_register.put(self.register_last_name_entry, 306, 230)
        self.layout_register.put(self.register_nickname_entry, 306, 280)
        self.layout_register.put(self.register_password_entry, 306, 330)
        self.layout_register.put(self.register_button, 306, 380)
        self.layout_register.put(self.from_register_to_welcome_button, 375, 380)

        self.hbox_message_register = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox_message_register.set_halign(Gtk.Align.CENTER)
        self.message_register = Gtk.Label("Dummy")
        self.message_register.set_name("message_register")
        self.hbox_message_register.add(self.message_register)

        self.vbox_register.pack_start(self.layout_register, False, False, 50)

        ################################################################################################################
        # Login page                                                                                                   #
        ################################################################################################################

        vbox_login = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(vbox_login, Gtk.Label("Login"))

        login_user_label = Gtk.Label("Nickname:")
        login_password_label = Gtk.Label("Password:")
        self.login_user_entry = Gtk.Entry()
        self.login_user_entry.set_placeholder_text("nickname")
        self.login_user_entry.set_max_length(20)
        self.login_password_entry = Gtk.Entry()
        self.login_password_entry.set_placeholder_text("password")
        self.login_password_entry.set_max_length(20)
        self.login_password_entry.set_visibility(False)
        self.login_button = Gtk.Button(label="Login")
        self.login_button.connect("clicked", login_clicked)
        self.from_login_to_welcome_button = Gtk.Button("Welcome page")
        self.from_login_to_welcome_button.connect("clicked", get_to_welcome_page)

        self.layout_login = Gtk.Fixed()
        self.layout_login.put(login_user_label, 206, 100)
        self.layout_login.put(login_password_label, 206, 150)
        self.layout_login.put(self.login_user_entry, 306, 100)
        self.layout_login.put(self.login_password_entry, 306, 150)
        self.layout_login.put(self.login_button, 306, 200)
        self.layout_login.put(self.from_login_to_welcome_button, 360, 200)

        vbox_login.pack_start(self.layout_login, False, False, 180)

        ################################################################################################################
        # Preparation of vocabulary test or go to administration                                                       #
        ################################################################################################################

        self.vbox_preparation_of_test = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(self.vbox_preparation_of_test, Gtk.Label("Preparation"))

        combobox_label = Gtk.Label("Choose a language:")
        layout_preparation_of_test = Gtk.Fixed()
        layout_preparation_of_test.put(combobox_label, 283, 0)

        # Model
        self.store_language_combobox_preparation = Gtk.ListStore(int, str, int)

        # View
        self.languages_combobox = Gtk.ComboBox.new_with_model(self.store_language_combobox_preparation)
        renderer = Gtk.CellRendererText()
        self.languages_combobox.connect("changed", language_selected)
        self.languages_combobox.pack_start(renderer, True)
        self.languages_combobox.add_attribute(renderer, "text", 1)
        layout_preparation_of_test.put(self.languages_combobox, 283, 30)

        hbox_direction_of_asking = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_direction_of_asking.set_halign(Gtk.Align.CENTER)
        self.radiobutton_dummy = Gtk.RadioButton(label="dummy")
        self.radiobutton_de_foreign_language = Gtk.RadioButton(label="DE -> Foreign language")
        self.radiobutton_de_foreign_language.connect("toggled", direction_selected)
        self.radiobutton_foreign_language_de = Gtk.RadioButton(label="Foreign language -> DE")
        self.radiobutton_foreign_language_de.connect("toggled", direction_selected)
        self.radiobutton_de_foreign_language.join_group(self.radiobutton_dummy)
        self.radiobutton_foreign_language_de.join_group(self.radiobutton_dummy)

        hbox_direction_of_asking.add(self.radiobutton_de_foreign_language)
        hbox_direction_of_asking.add(self.radiobutton_foreign_language_de)

        self.start_test_button = Gtk.Button(label="Start training")
        self.start_test_button.connect("clicked", start_training)
        self.get_to_crud_vocabulary_page_button = Gtk.Button(label="Administrate vocabulary")
        self.get_to_crud_vocabulary_page_button.connect("clicked", get_to_crud_vocabulary)
        get_to_crud_language_page_button = Gtk.Button(label="Administrate language")
        get_to_crud_language_page_button.connect("clicked", get_to_crud_language)

        hbox_buttons_on_preparation_page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_buttons_on_preparation_page.set_halign(Gtk.Align.CENTER)
        hbox_buttons_on_preparation_page.add(self.start_test_button)
        hbox_buttons_on_preparation_page.add(self.get_to_crud_vocabulary_page_button)
        hbox_buttons_on_preparation_page.add(get_to_crud_language_page_button)

        self.hbox_message_preparation = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox_message_preparation.set_halign(Gtk.Align.CENTER)
        self.message_preparation = Gtk.Label("Dummy")
        self.message_preparation.set_name("message_preparation")
        self.hbox_message_preparation.add(self.message_preparation)

        self.vbox_preparation_of_test.pack_start(layout_preparation_of_test, False, False, 100)
        self.vbox_preparation_of_test.pack_start(hbox_direction_of_asking, False, False, 0)
        self.vbox_preparation_of_test.pack_start(hbox_buttons_on_preparation_page, False, False, 100)

        ################################################################################################################
        # Vocabulary Test                                                                                              #
        ################################################################################################################

        vbox_test = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(vbox_test, Gtk.Label("Test"))

        hbox_test_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_test_info.set_halign(Gtk.Align.CENTER)
        self.test_info_label = Gtk.Label("Dummy")
        hbox_test_info.add(self.test_info_label)
        vbox_test.pack_start(hbox_test_info, False, False, 120)

        german_label = Gtk.Label("German")
        self.foreign_language_label = Gtk.Label("Language")
        self.german_entry_test = Gtk.Entry()
        self.german_entry_test.set_placeholder_text("fill in")
        self.foreign_language_entry_test = Gtk.Entry()
        self.foreign_language_entry_test.set_placeholder_text("fill in")
        self.stop_button_test = Gtk.Button(label="Stop")
        self.next_button_test = Gtk.Button(label="Next")
        self.stop_button_test.connect("clicked", stop_test)
        self.next_button_test.connect("clicked", next_vocabulary_test)

        self.layout_test = Gtk.Fixed()
        self.layout_test.put(german_label, 206, 0)
        self.layout_test.put(self.foreign_language_label, 206, 50)
        self.layout_test.put(self.german_entry_test, 306, 0)
        self.layout_test.put(self.foreign_language_entry_test, 306, 50)
        self.layout_test.put(self.stop_button_test, 306, 100)
        self.layout_test.put(self.next_button_test, 355, 100)

        vbox_test.pack_start(self.layout_test, False, False, 0)

        ################################################################################################################
        # Administration CRUD Vocabulary for user                                                                      #
        ################################################################################################################

        self.vbox_administrate_vocabulary = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(self.vbox_administrate_vocabulary, Gtk.Label("Administrate vocabulary"))

        # vocabulary_id_label_crud_vocabulary = Gtk.Label("Vocabulary ID:")
        german_label_crud_vocabulary = Gtk.Label("German")
        self.foreign_language_label_crud_vocabulary = Gtk.Label("Language")
        # language_id_label_crud_vocabulary = Gtk.Label("Language ID:")
        self.vocabulary_id_entry_crud_vocabulary = Gtk.Entry()
        self.vocabulary_id_entry_crud_vocabulary.set_placeholder_text("vocabulary id")
        self.vocabulary_id_entry_crud_vocabulary.set_sensitive(False)
        self.german_entry_crud_vocabulary = Gtk.Entry()
        self.german_entry_crud_vocabulary.set_placeholder_text("fill in")
        self.foreign_language_entry_crud_vocabulary = Gtk.Entry()
        self.foreign_language_entry_crud_vocabulary.set_placeholder_text("fill in")
        self.language_id_entry_crud_vocabulary = Gtk.Entry()
        self.language_id_entry_crud_vocabulary.set_placeholder_text("language id")
        self.language_id_entry_crud_vocabulary.set_sensitive(False)

        # Model
        self.store_vocabulary = Gtk.ListStore(int, str, str, int)

        # View
        self.tree_vocabulary = Gtk.TreeView(self.store_vocabulary)
        column = Gtk.TreeViewColumn("vocabulary id", renderer, text=0)
        column.set_sort_column_id(0)
        # self.tree_vocabulary.append_column(column)
        column = Gtk.TreeViewColumn("German", renderer, text=1)
        column.set_sort_column_id(1)
        self.tree_vocabulary.append_column(column)
        self.column_title_crud_vocabulary = Gtk.TreeViewColumn("Foreign language", renderer, text=2)
        self.column_title_crud_vocabulary.set_sort_column_id(2)
        self.tree_vocabulary.append_column(self.column_title_crud_vocabulary)
        column = Gtk.TreeViewColumn("language id", renderer, text=3)
        column.set_sort_column_id(3)
        # self.tree_vocabulary.append_column(column)

        scrolled_window_vocabulary = Gtk.ScrolledWindow()
        scrolled_window_vocabulary.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window_vocabulary.add(self.tree_vocabulary)
        scrolled_window_vocabulary.set_min_content_height(100)

        select_vocabulary = self.tree_vocabulary.get_selection()
        select_vocabulary.connect("changed", vocabulary_record_selected)

        self.create_vocabulary_button = Gtk.Button(label="Create")
        read_all_vocabulary_button = Gtk.Button(label="Read all / Clear entries")
        self.update_vocabulary_button = Gtk.Button(label="Update")
        self.delete_vocabulary_button = Gtk.Button(label="Delete")
        self.from_admin_vocabulary_to_preparation_button = Gtk.Button(label="Back")
        self.create_vocabulary_button.connect("clicked", create_vocabulary)
        read_all_vocabulary_button.connect("clicked", read_all_vocabulary)
        self.update_vocabulary_button.connect("clicked", update_vocabulary)
        self.delete_vocabulary_button.connect("clicked", delete_vocabulary)
        self.from_admin_vocabulary_to_preparation_button.connect("clicked", from_admin_vocabulary_to_preparation)

        hbox_treeview_vocabulary = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_treeview_vocabulary.set_halign(Gtk.Align.CENTER)
        hbox_treeview_vocabulary.add(scrolled_window_vocabulary)

        self.layout_administration_vocabulary = Gtk.Fixed()
        # self.layout_administration_vocabulary.put(vocabulary_id_label_crud_vocabulary, 206, 0)
        # self.layout_administration_vocabulary.put(self.vocabulary_id_entry_crud_vocabulary, 306, 0)
        self.layout_administration_vocabulary.put(german_label_crud_vocabulary, 206, 0)  # 206, 50
        self.layout_administration_vocabulary.put(self.foreign_language_label_crud_vocabulary, 206, 50)  # 206, 100
        self.layout_administration_vocabulary.put(self.german_entry_crud_vocabulary, 306, 0)  # 306, 50
        self.layout_administration_vocabulary.put(self.foreign_language_entry_crud_vocabulary, 306, 50)  # 306, 100
        # self.layout_administration_vocabulary.put(language_id_label_crud_vocabulary, 206, 150)
        # self.layout_administration_vocabulary.put(self.language_id_entry_crud_vocabulary, 306, 150)

        hbox_crud_buttons_vocabulary = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_crud_buttons_vocabulary.set_halign(Gtk.Align.CENTER)

        hbox_crud_buttons_vocabulary.add(self.create_vocabulary_button)
        hbox_crud_buttons_vocabulary.add(read_all_vocabulary_button)
        hbox_crud_buttons_vocabulary.add(self.update_vocabulary_button)
        hbox_crud_buttons_vocabulary.add(self.delete_vocabulary_button)
        hbox_crud_buttons_vocabulary.add(self.from_admin_vocabulary_to_preparation_button)

        self.hbox_message_crud_vocabulary = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox_message_crud_vocabulary.set_halign(Gtk.Align.CENTER)
        self.message_vocabulary = Gtk.Label("Dummy")
        self.message_vocabulary.set_name("message_vocabulary")
        self.hbox_message_crud_vocabulary.add(self.message_vocabulary)

        self.vbox_administrate_vocabulary.pack_start(hbox_treeview_vocabulary, False, False, 85)
        self.vbox_administrate_vocabulary.pack_start(self.layout_administration_vocabulary, False, False, 0)
        self.vbox_administrate_vocabulary.pack_start(hbox_crud_buttons_vocabulary, False, False, 85)

        ################################################################################################################
        # Administration CRUD Language for user                                                                        #
        ################################################################################################################

        self.vbox_administrate_language = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(self.vbox_administrate_language, Gtk.Label("Administrate language"))

        # language_id_label_crud_language = Gtk.Label("Language ID:")
        language_name_label_crud_language = Gtk.Label("Language name:")
        # user_id_label_crud_language = Gtk.Label("User ID:")
        self.language_id_entry_crud_language = Gtk.Entry()
        self.language_id_entry_crud_language.set_placeholder_text("language id")
        self.language_id_entry_crud_language.set_sensitive(False)
        self.language_name_entry_crud_language = Gtk.Entry()
        self.language_name_entry_crud_language.set_placeholder_text("fill in")
        self.language_name_entry_crud_language.set_max_length(20)
        self.user_id_entry_crud_language = Gtk.Entry()
        self.user_id_entry_crud_language.set_placeholder_text("user id")
        self.user_id_entry_crud_language.set_sensitive(False)

        # Model
        self.store_language = Gtk.ListStore(int, str, int)

        # View
        self.tree_language = Gtk.TreeView(self.store_language)
        column = Gtk.TreeViewColumn("language id", renderer, text=0)
        column.set_sort_column_id(0)
        # self.tree_language.append_column(column)
        column = Gtk.TreeViewColumn("name of language", renderer, text=1)
        column.set_sort_column_id(1)
        self.tree_language.append_column(column)
        column = Gtk.TreeViewColumn("user id", renderer, text=2)
        column.set_sort_column_id(2)
        # self.tree_language.append_column(column)

        scrolled_window_language = Gtk.ScrolledWindow()
        scrolled_window_language.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window_language.add(self.tree_language)
        scrolled_window_language.set_min_content_height(100)

        select_language = self.tree_language.get_selection()
        select_language.connect("changed", language_record_selected)

        self.create_language_button = Gtk.Button(label="Create")
        read_all_language_button = Gtk.Button(label="Read all / Clear entries")
        self.update_language_button = Gtk.Button(label="Update")
        self.delete_language_button = Gtk.Button(label="Delete")
        self.from_admin_language_to_preparation_button = Gtk.Button(label="Back")
        self.create_language_button.connect("clicked", create_language)
        read_all_language_button.connect("clicked", read_all_language)
        self.update_language_button.connect("clicked", update_language)
        self.delete_language_button.connect("clicked", delete_language)
        self.from_admin_language_to_preparation_button.connect("clicked", from_admin_language_to_preparation)

        hbox_treeview_language = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_treeview_language.set_halign(Gtk.Align.CENTER)
        hbox_treeview_language.add(scrolled_window_language)

        self.layout_administration_language = Gtk.Fixed()
        # self.layout_administration_language.put(language_id_label_crud_language, 206, 0)
        # self.layout_administration_language.put(self.language_id_entry_crud_language, 306, 0)
        self.layout_administration_language.put(language_name_label_crud_language, 206, 0)  # 206, 50
        self.layout_administration_language.put(self.language_name_entry_crud_language, 306, 0)  # 306, 50
        # self.layout_administration_language.put(user_id_label_crud_language, 206, 100)
        # self.layout_administration_language.put(self.user_id_entry_crud_language, 306, 100)

        hbox_crud_buttons_language = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_crud_buttons_language.set_halign(Gtk.Align.CENTER)

        hbox_crud_buttons_language.add(self.create_language_button)
        hbox_crud_buttons_language.add(read_all_language_button)
        hbox_crud_buttons_language.add(self.update_language_button)
        hbox_crud_buttons_language.add(self.delete_language_button)
        hbox_crud_buttons_language.add(self.from_admin_language_to_preparation_button)

        self.hbox_message_crud_language = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox_message_crud_language.set_halign(Gtk.Align.CENTER)
        self.message_language = Gtk.Label("Dummy")
        self.message_language.set_name("message_language")
        self.hbox_message_crud_language.add(self.message_language)

        self.vbox_administrate_language.pack_start(hbox_treeview_language, False, False, 85)
        self.vbox_administrate_language.pack_start(self.layout_administration_language, False, False, 0)
        self.vbox_administrate_language.pack_start(hbox_crud_buttons_language, False, False, 85)

        ################################################################################################################
        # Administration CRUD User for root                                                                            #
        # Create operation is not necessary, because you can register.                                                 #
        ################################################################################################################

        self.vbox_administrate_user = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.notebook.append_page(self.vbox_administrate_user, Gtk.Label("Administrate user"))

        user_id_label_crud_user = Gtk.Label("User ID:")
        first_name_label_crud_user = Gtk.Label("First name:")
        last_name_label_crud_user = Gtk.Label("Last name:")
        nickname_label_crud_user = Gtk.Label("Nickname:")
        password_label_crud_user = Gtk.Label("Password:")
        self.user_id_entry_crud_user = Gtk.Entry()
        self.user_id_entry_crud_user.set_placeholder_text("user id")
        self.user_id_entry_crud_user.set_sensitive(False)
        self.first_name_entry_crud_user = Gtk.Entry()
        self.first_name_entry_crud_user.set_placeholder_text("first name")
        self.first_name_entry_crud_user.set_max_length(20)
        self.last_name_entry_crud_user = Gtk.Entry()
        self.last_name_entry_crud_user.set_placeholder_text("last name")
        self.last_name_entry_crud_user.set_max_length(20)
        self.nickname_entry_crud_user = Gtk.Entry()
        self.nickname_entry_crud_user.set_placeholder_text("nickname")
        self.nickname_entry_crud_user.set_max_length(20)
        self.password_entry_crud_user = Gtk.Entry()
        self.password_entry_crud_user.set_placeholder_text("password")
        self.password_entry_crud_user.set_max_length(20)
        self.password_entry_crud_user.set_visibility(False)

        # Model
        self.store_user = Gtk.ListStore(int, str, str, str, str)

        # View
        self.tree_user = Gtk.TreeView(self.store_user)
        column = Gtk.TreeViewColumn("user id", renderer, text=0)
        column.set_sort_column_id(0)
        self.tree_user.append_column(column)
        column = Gtk.TreeViewColumn("first name", renderer, text=1)
        column.set_sort_column_id(1)
        self.tree_user.append_column(column)
        column = Gtk.TreeViewColumn("last name", renderer, text=2)
        column.set_sort_column_id(2)
        self.tree_user.append_column(column)
        column = Gtk.TreeViewColumn("nickname", renderer, text=3)
        column.set_sort_column_id(3)
        self.tree_user.append_column(column)
        column = Gtk.TreeViewColumn("password", renderer, text=4)
        column.set_fixed_width(230)
        column.set_sort_column_id(4)
        self.tree_user.append_column(column)

        scrolled_window_user = Gtk.ScrolledWindow()
        scrolled_window_user.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window_user.add(self.tree_user)
        scrolled_window_user.set_min_content_height(100)

        select_user = self.tree_user.get_selection()
        select_user.connect("changed", user_record_selected)

        read_all_user_button = Gtk.Button(label="Read all / Clear entries")
        self.update_user_button = Gtk.Button(label="Update")
        self.delete_user_button = Gtk.Button(label="Delete")
        read_all_user_button.connect("clicked", read_all_user)
        self.update_user_button.connect("clicked", update_user)
        self.delete_user_button.connect("clicked", delete_user)

        hbox_treeview_user = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox_treeview_user.set_halign(Gtk.Align.CENTER)
        hbox_treeview_user.add(scrolled_window_user)

        self.layout_administration_user = Gtk.Fixed()
        self.layout_administration_user.put(user_id_label_crud_user, 206, 0)
        self.layout_administration_user.put(first_name_label_crud_user, 206, 50)
        self.layout_administration_user.put(last_name_label_crud_user, 206, 100)
        self.layout_administration_user.put(nickname_label_crud_user, 206, 150)
        self.layout_administration_user.put(password_label_crud_user, 206, 200)
        self.layout_administration_user.put(self.user_id_entry_crud_user, 306, 0)
        self.layout_administration_user.put(self.first_name_entry_crud_user, 306, 50)
        self.layout_administration_user.put(self.last_name_entry_crud_user, 306, 100)
        self.layout_administration_user.put(self.nickname_entry_crud_user, 306, 150)
        self.layout_administration_user.put(self.password_entry_crud_user, 306, 200)

        hbox_crud_buttons_user = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox_crud_buttons_user.set_halign(Gtk.Align.CENTER)

        hbox_crud_buttons_user.add(read_all_user_button)
        hbox_crud_buttons_user.add(self.update_user_button)
        hbox_crud_buttons_user.add(self.delete_user_button)

        self.hbox_message_crud_user = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.hbox_message_crud_user.set_halign(Gtk.Align.CENTER)
        self.message_user = Gtk.Label("Dummy")
        self.message_user.set_name("message_user")
        self.hbox_message_crud_user.add(self.message_user)

        self.vbox_administrate_user.pack_start(hbox_treeview_user, False, False, 60)
        self.vbox_administrate_user.pack_start(self.layout_administration_user, False, False, 0)
        self.vbox_administrate_user.pack_start(hbox_crud_buttons_user, False, False, 60)
