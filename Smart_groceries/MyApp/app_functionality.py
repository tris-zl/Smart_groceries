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
            SmartApp.email = email
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
        if data.text == "":
            self.new_user = False  # information for kivy
        else:
            # some kind of global variables to access from other screens as well
            SmartApp.first_name = first_name
            SmartApp.last_name = last_name
            SmartApp.email = email
            self.new_user = True  # information for kivy

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

        # filter that only groups that added products can see them
        team_id = SmartApp.group_id
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
    email = ""

    group_id = None
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

    def join_team(self):
        dic = {"email": self.email}  # into dic for request
        user_id = requests.get("http://127.0.0.1:5000/give_user_ids", dic)    # http request

        # into dic for request
        dic_2 = {"group_name": self.group_name, "group_password": self.group_password}
        team_id = requests.get("http://127.0.0.1:5000/give_team_ids", dic_2)    # http request
        self.group_id = team_id

        if team_id.text:   # if team exists
            self.group_exists = True
            dic_3 = {"team_id": team_id, "user_id": user_id}
            requests.get("http://127.0.0.1:5000/join_team", dic_3)    # http request

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
        dic = {"email": self.email}  # into dic for request
        data = requests.get("http://127.0.0.1:5000/give_user_ids", dic)  # http request
        user_id = data.json()

        # into dic for request
        dic_2 = {"user_id": user_id, "group_name": self.group_name, "group_password": self.group_password}
        team_id = requests.get("http://127.0.0.1:5000/new_group", dic_2)  # http request

        if team_id.text:
            self.group_id = team_id
            self.group_exists = True


if __name__ == '__main__':
    SmartApp().run()
