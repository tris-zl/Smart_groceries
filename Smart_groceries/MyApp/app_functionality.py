from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import requests


class StartScreen(Screen):
    pass


class SignIn(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    user_exists = BooleanProperty(None)

    def btn(self):
        email = self.email.text
        password = self.password.text

        dic = {"email": email, "password": password}
        self.ids.email.text = ""
        self.ids.password.text = ""
        data = requests.get("http://127.0.0.1:5000/check_users", dic)
        if data.text == "":
            self.user_exists = False
        else:
            names = data.json()
            SmartApp.first_name = names[0]
            SmartApp.last_name = names[1]
            self.user_exists = True

    def invalid_enter(self):
        print(f'Either your name or password is not correct. ')
        self.ids.email.text = ""
        self.ids.password.text = ""


class SignUp(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    new_user = BooleanProperty(None)

    def btn(self):
        first_name = self.first_name.text
        last_name = self.last_name.text
        email = self.email.text
        password = self.password.text

        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.check_password.text = ""

        dic = {"name": first_name, "last_name": last_name, "email": email, "password": password}
        data = requests.get("http://127.0.0.1:5000/add_users", dic)
        if "successfully added" in data.text:
            SmartApp.first_name = first_name
            SmartApp.last_name = last_name
            self.new_user = True
        else:
            self.new_user = False

    def invalid_enter(self):
        print("Invalid enter. ")
        self.ids.first_name.text = ""
        self.ids.last_name.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""
        self.ids.check_password.text = ""


class JoinGroup(Screen):
    pass


class GroceryList(Screen):
    product_name = ObjectProperty(None)
    quantity = ObjectProperty(None)

    def btn(self):
        product_name = self.product_name.text
        quantity = self.quantity.text
        dic = {"product_name": product_name,
               "quantity": quantity,
               "first_name": SmartApp.first_name,
               "last_name": SmartApp.last_name}
        requests.get("http://127.0.0.1:5000/add_to_shoppingcart", dic)


class ShoppingCart(Screen, Widget):
    shoppingcart = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.shoppingcart.remove_widget(self.shoppingcart)
        data = requests.get("http://127.0.0.1:5000/shoppingcart")
        products = data.json()
        layout = GridLayout(cols=3, size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        for product in products:
            all_names = []
            layout.add_widget(Label(text=product[0], size_hint=(1/3, None)))
            layout.add_widget(Label(text=product[1], size_hint=(1/3, None)))
            all_names.append(product[3])
            all_names.append(product[2])
            layout.add_widget(Label(text=', '.join(all_names), size_hint=(1/3, None)))
        self.shoppingcart.add_widget(layout)


class Product(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("the.kv")


class SmartApp(App):
    first_name = ""
    last_name = ""

    def build(self):
        return kv


if __name__ == '__main__':
    SmartApp().run()
