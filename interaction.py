import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def do_login(driver):
    load_dotenv()
    # Access the API key and private key from environment variables
    email = os.getenv("EMAIL_ACCOUNT")
    password = os.getenv("PASSWORD_ACCOUNT")
    driver.get("https://www.pararius.nl/inloggen-email")
    # options.add_argument("--headless")  # uncomment if you want no window
    # --- Fill logins
    input_elements = driver.find_elements(By.TAG_NAME, "input")
    input_elements[1].clear()
    input_elements[1].send_keys(email)
    input_elements[2].clear()
    input_elements[2].send_keys(password)

    button_elements = driver.find_elements(By.TAG_NAME, "button")
    # --- Click login button
    button_elements[1].click()

def check_cookies_buttons(driver):
    # Check for cookie acceptance
    cookie_buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in cookie_buttons:
        if "cookies" in button.text.lower():
            button.click()
            return

def click_contact_button(driver):
    link_elements = driver.find_elements(By.TAG_NAME, "a")
    for link in link_elements:
        link_name = link.text.lower()
        if "contact" in link_name and "makelaar" in link_name:
            link.click()
            return

def click_send_button(driver):
    # Second page, we assume information is filled in already
    buttons_second_page = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons_second_page:
        if "versturen" in button.text.lower():
            button.click()
            print("Reaction sent")
            return


def send_reaction(driver):
    url = "https://www.pararius.nl/appartement-te-huur/veenendaal/b3c3a325/julianastraat"
    driver.get(url)
    check_cookies_buttons(driver)
    click_contact_button(driver)
    click_send_button(driver)


driver = webdriver.Firefox()
do_login(driver)
time.sleep(1)
send_reaction(driver)