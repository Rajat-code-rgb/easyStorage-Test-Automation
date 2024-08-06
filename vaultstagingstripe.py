import os
import time
from os.path import join, dirname
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import pandas as pd

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


""" NECESSARY IMPORTS"""
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
LOG_FOLDER_NAME = os.environ.get("LOG_FOLDER_NAME")
LOG_FILE_NAME = os.environ.get("LOG_FILE")
TESTING_URL = os.environ.get("TESTING_URL")
TEST_CASES_PATH = os.environ.get("TEST_CASES_PATH")
LOGIN_FILE_NAME = os.environ.get("LOGIN_FILE_NAME")


# Ensure LOG_FOLDER_NAME and LOG_FILE_NAME are not None
if not LOG_FOLDER_NAME or not LOG_FILE_NAME:
    raise ValueError("LOG_FOLDER_NAME and LOG_FILE_NAME must be set in the .env file")

LOG_DESTINATION = join(dirname(__file__), LOG_FOLDER_NAME)
LOG_PATH = join(LOG_DESTINATION, LOG_FILE_NAME)
AUTHENTICATION = []

# Set up the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(CHROME_DRIVER_PATH)  # Update with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_test_cases():
    """For importing username and passwords """
    login_credentials = pd.read_csv(join(TEST_CASES_PATH,LOGIN_FILE_NAME),sep="\t")
    usernames = login_credentials["username"]
    passwords = login_credentials["password"]
    for username, password in zip(usernames, passwords):
        if(username and password):
            AUTHENTICATION.append({"username": username, "password":password})
    print(AUTHENTICATION)
    
def log(msg):
    """Check if the logs folder exists if not create one"""
    try:
        if not os.path.exists(LOG_DESTINATION):
            os.makedirs(LOG_DESTINATION)
        """Append a log message with timestamp to the log file."""
        with open(LOG_PATH, "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            file.write(f"{timestamp} - {msg}\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}")


def login(username, password):
    
    """Log in to the application with provided username and password."""
    try:
        # Wait for the username input box to be present and interact with it
        username_input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "kt_login_signin_submit"))
        )

        username_input_box.send_keys(username)
        password_input_box.send_keys(password)
        login_button.click()

        # Wait for the URL to change to confirm successful login
        WebDriverWait(driver, 10).until(EC.url_changes(TESTING_URL))

        log("Login successful and page loaded")

    except Exception as e:
        log(f"Login or page load failed: {e}")
        print(f"Login or page load failed: {e}")


def add_user():
    """Click on edit icon besides Contact Details to add user"""
    add_user_dialog_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class = 'symbol-label']//button[@class = 'btn ']"))
    )
    add_user_dialog_button.click()
    

def create_order():
    """Click the 'Create Order' button to create a new order."""
    try:
        # Wait for the Create Order button to be clickable and then click it
        create_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='topbar']//button[contains(text(), 'Create Order')]",
                )
            )
        )
        create_order_button.click()
        log("Create Order button clicked")
    except Exception as e:
        log(f"Create Order button interaction failed: {e}")
        print(f"Create Order button interaction failed: {e}")


try:
    get_test_cases()
    for credentials in AUTHENTICATION:
        print(credentials)
        driver.get(TESTING_URL)
        # Maximize the browser window
        driver.maximize_window()
        login(credentials["username"], credentials["password"])
        time.sleep(5)  # Consider using WebDriverWait here instead of sleep
        
        create_order()
        add_user()
        time.sleep(5)  # Consider using WebDriverWait here instead of sleep
except Exception as e:
    log(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
