"""
        Original script (c) Sergey Kolokolov, part of the LinkedIn autoconnect
"""
from pages.login_page import LoginPage


def login(data):
    page = LoginPage(data)
    page.open_url("login_url")
    page.wait_element_displayed("email_field")
    page.wait_element_displayed("pass_field")
    page.wait_element_displayed("submit_button")
    page.enter_text("email_field", data["email"])
    page.enter_text("pass_field", data["password"])
    page.click("submit_button")
    print('Logged In')
    page.wait_element_displayed("avatar")
