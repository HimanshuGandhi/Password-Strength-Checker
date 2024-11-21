from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import re
import math


COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345",
    "qwerty", "abc123", "111111", "iloveyou", "123123", "welcome",
    "admin", "letmein", "1234", "password1"
]

def is_common_password(password):
    return password in COMMON_PASSWORDS

def calculate_entropy(password):
    charsets = 0
    if any(c.islower() for c in password):
        charsets += 26
    if any(c.isupper() for c in password):
        charsets += 26
    if any(c.isdigit() for c in password):
        charsets += 10
    if any(c in "!@#$%^&*(),.?\":{}|<>" for c in password):
        charsets += len("!@#$%^&*(),.?\":{}|<>")
    entropy = len(password) * math.log2(charsets) if charsets > 0 else 0
    return round(entropy, 2)

def check_password_strength(password):
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password)
    lowercase_criteria = re.search(r'[a-z]', password)
    digit_criteria = re.search(r'[0-9]', password)
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    score = 0
    if length_criteria:
        score += 1
    if uppercase_criteria:
        score += 1
    if lowercase_criteria:
        score += 1
    if digit_criteria:
        score += 1
    if special_char_criteria:
        score += 1

    if score < 3:
        return "Weak Password"
    elif score == 3 or score == 4:
        return "Moderate Password"
    elif score == 5:
        return "Strong Password"

def full_password_analysis(password):
    if is_common_password(password):
        return "Very Weak Password (Commonly used password)"
    strength = check_password_strength(password)
    entropy = calculate_entropy(password)
    return f"{strength} | Entropy: {entropy} bits"


class PasswordApp(App):
    def build(self):
        
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        
        self.input_label = Label(text="Enter Password:", font_size=18, size_hint=(1, 0.2))
        self.layout.add_widget(self.input_label)
        
        self.password_input = TextInput(password=True, multiline=False, font_size=16, size_hint=(1, 0.2))
        self.layout.add_widget(self.password_input)
        
       
        button_layout = GridLayout(cols=2, size_hint=(1, 0.2), spacing=10)
        
        self.check_button = Button(text="Check Strength", font_size=16, background_color=(0, 0.7, 0, 1))
        self.check_button.bind(on_press=self.check_password)
        button_layout.add_widget(self.check_button)
        
        self.clear_button = Button(text="Clear", font_size=16, background_color=(0.7, 0, 0, 1))
        self.clear_button.bind(on_press=self.clear_fields)
        button_layout.add_widget(self.clear_button)
        
        self.layout.add_widget(button_layout)
        
       
        self.result_label = Label(text="Result: ", font_size=18, size_hint=(1, 0.4))
        self.layout.add_widget(self.result_label)
        
        return self.layout

    def check_password(self, instance):
        password = self.password_input.text
        if not password:
            self.result_label.text = "Result: Please enter a password."
        else:
            feedback = full_password_analysis(password)
            self.result_label.text = f"Result: {feedback}"

    def clear_fields(self, instance):
        self.password_input.text = ""
        self.result_label.text = "Result: "

if __name__ == "__main__":
    PasswordApp().run()
