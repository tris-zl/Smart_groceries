from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import requests


class StartScreen(Screen):
    pass


class SignIn(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    user_exists = BooleanProperty(None)

    def btn(self):
        # store text of text labels into variables
        email = self.email.text
        password = self.password.text

        # delete text from text labels
        self.ids.email.text = ""
        self.ids.password.text = ""

        dic = {"email": email, "password": password}  # into dictionary for request
        data = requests.get("http://127.0.0.1:5000/check_users", dic)  # http request stored into variable
        if data.text == "":
            self.user_exists = False  # information for kivy
        else:
            names = data.json()
            SmartApp.first_name = names[0]
            SmartApp.last_name = names[1]
            self.user_exists = True  # information for kivy

    def invalid_enter(self):
        print(f'Either your name or password is not correct. ')
        # delete text from text labels
        self.ids.email.text = ""
        self.ids.password.text = ""


class SignUp(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    new_user = BooleanProperty(None)

    def btn(self):
        # store text of text labels into variables
        first_name = self.first_name.text
        last_name = self.last_name.text
        email = self.email.text
        password = self.password.text

        # delete text from text labels
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.check_password.text = ""

        # into dictionary for request
        dic = {"name": first_name, "last_name": last_name, "email": email, "password": password}
        data = requests.get("http://127.0.0.1:5000/add_users", dic)  # http request stored into variable
        if "successfully added" in data.text:
            # some kind of global variables to access from other screens as well
            SmartApp.first_name = first_name
            SmartApp.last_name = last_name
            self.new_user = True  # information for kivy
        else:
            self.new_user = False  # information for kivy

    def invalid_enter(self):
        print("Invalid enter. ")
        # delete text from text labels
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.check_password.text = ""


class JoinCreateGroup(Screen):
    pass


class PJoinGroup(FloatLayout):
    pass


class PCreateGroup(FloatLayout):
    pass


class GroceryList(Screen):
    product_name = ObjectProperty(None)
    quantity = ObjectProperty(None)

    def btn(self):
        # store text of text labels into variables
        product_name = self.product_name.text
        quantity = self.quantity.text

        # into dictionary for request
        dic = {"product_name": product_name,
               "quantity": quantity,
               "first_name": SmartApp.first_name,
               "last_name": SmartApp.last_name}
        requests.get("http://127.0.0.1:5000/add_to_shoppingcart", dic)  # http request


class ShoppingCart(Screen, Widget):
    shoppingcart = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.shoppingcart.clear_widgets()  # remove everything to update it on pre enter
        data = requests.get("http://127.0.0.1:5000/shoppingcart")   # http request stored into variable
        products = data.json()

        # make layout in kivy from py file
        layout = GridLayout(cols=3, size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))

        # add info from database into kivy to users interface
        for product in products:
            all_names = []
            layout.add_widget(Label(text=str(product[0]), size_hint=(1/3, None)))
            layout.add_widget(Label(text=str(product[1]), size_hint=(1/3, None)))
            all_names.append(product[3])
            all_names.append(product[2])
            layout.add_widget(Label(text=', '.join(all_names), size_hint=(1/3, None)))

        # add layout as child to parent ScrollView "shoppingcart"
        self.shoppingcart.add_widget(layout)


class Product(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("the.kv")


class SmartApp(App):
    first_name = ""
    last_name = ""

    group_name = ""
    group_password = ""
    group_exists = False

    def build(self):
        return kv

    @staticmethod
    def show_popup_join():
        show = PJoinGroup()  # make new instance of popup

        # define some attributes
        popup_window = Popup(title="Join group", content=show, size_hint=(None, None), size=(400, 400))

        popup_window.open()

    def check_group_member(self):
        dic = {"group_name": self.group_name, "group_password": self.group_password}  # into dic for request
        data = requests.get("http://127.0.0.1:5000/check_group_member", dic)    # http request

        if data.text:   # if group exists
            self.group_exists = True

    @staticmethod
    def invalid_enter():
        print("Invalid enter. ")

    @staticmethod
    def show_popup_create():
        show = PCreateGroup()  # make new instance of popup

        # define some attributes
        popup_window = Popup(title="Join group", content=show, size_hint=(None, None), size=(400, 400))

        popup_window.open()

    def new_group(self):
        dic = {"group_name": self.group_name, "group_password": self.group_password}  # into dic for request
        requests.get("http://127.0.0.1:5000/new_group", dic)  # http request


if __name__ == '__main__':
    SmartApp().run()
