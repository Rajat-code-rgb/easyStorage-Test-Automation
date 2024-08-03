from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOG_FILE = "vaultstaging.txt"
TESTING_URL = "https://vaultstagingstripe.easystorage.com/auth/login"
AUTHENTICATION = [{"username": "paul@yopmail.com", "password": "Dots@123"}]

# Set up the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service("C:\\chromedriver-win64\\chromedriver.exe")  # Update with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def log(msg):
    """Append a log message with timestamp to the log file."""
    with open(LOG_FILE, 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{timestamp} - {msg}\n")

def login(username, password):
    """Log in to the application with provided username and password."""
    try:
        # Wait for the username input box to be present and interact with it
        username_input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        password_input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'kt_login_signin_submit'))
        )
        
        username_input_box.send_keys(username)
        password_input_box.send_keys(password)
        login_button.click()

        # Wait for the URL to change to confirm successful login
        WebDriverWait(driver, 10).until(
            EC.url_changes(TESTING_URL)
        )
        
        log("Login successful and page loaded")
    
    except Exception as e:
        log(f"Login or page load failed: {e}")
        print(f"Login or page load failed: {e}")

def create_order():
    """Click the 'Create Order' button to create a new order."""
    try:
        # Wait for the Create Order button to be clickable and then click it
        create_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='topbar']//button[contains(text(), 'Create Order')]"))
        )
        create_order_button.click()
        log("Create Order button clicked")
    except Exception as e:
        log(f"Create Order button interaction failed: {e}")
        print(f"Create Order button interaction failed: {e}")

try:
    driver.get(TESTING_URL)
    login(AUTHENTICATION[0]["username"], AUTHENTICATION[0]["password"])
    time.sleep(10)  # Consider using WebDriverWait here instead of sleep
    create_order()
    time.sleep(10)  # Consider using WebDriverWait here instead of sleep
except Exception as e:
    log(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
