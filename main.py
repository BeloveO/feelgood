from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import json, glob
from pathlib import Path
from hoverable import HoverBehavior
import random
from datetime import datetime
import time

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "signup_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users= json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.transition.direction = 'left'
            self.manager.current = "loginscreen_success"
        else:
            self.ids.login_wrong.text = "Incorrect Username or Password"
    def forgotp(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "forgot_password_screen"

class SignUpScreen(Screen):
    def logins(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    def add_user(self, uname, pword, otp):
        with open("users.json") as file:
            users= json.load(file)
        users[uname]= {'username': uname, 'password':pword, 'otp': otp,
        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.transition.direction = 'left'
        self.manager.current = "signup_screen_success"

class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    
    def get_quote(self, feel):
        feel= feel.lower()
        available_feelings= glob.glob("quotes/*txt")
        available_feelings= [Path(filename).stem for 
                            filename in available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quote = file.readlines()
            self.ids.quote.text = random.choice(quote)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
     pass

class ForgotPasswordScreen(Screen):
    def logins(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    def forgot(self, uname, otp):
        if len(uname) and len(otp) != 0:
            with open("users.json") as file:
                users= json.load(file)
            if uname in users and users[uname]['otp']== otp:
                self.manager.transition.direction = 'left'
                self.manager.current = "newpassword_screen"
            else:
                self.ids.userfound.text= "User not found or wrong secret number"
        else:
            self.ids.userfound.text= "Username or Password box cannot be empty"

class NewPasswordScreen(Screen):
    def forgotpa(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "forgot_password_screen"
    def newpassword(self, user, newp, newpt):
        if len(user) and len(newp) and len(newpt) != 0:
            with open("users.json") as file:
                users= json.load(file)
            if newp == newpt and user in users:
                users[user]['password'] = newp
                with open("users.json", 'w') as file:
                    json.dump(users, file)
                self.ids.password_match.text= "Password Updated"
            else:
                self.ids.password_match.text= "Passwords do not match"
        else:
            self.ids.password_match.text= "Password or Username cannot be left empty"
    def to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"        


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
