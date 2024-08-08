import os
import time
from os.path import join, dirname
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


""" NECESSARY IMPORTS"""
CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")
LOG_FOLDER_NAME = os.environ.get("LOG_FOLDER_NAME")
LOG_FILE_NAME = os.environ.get("LOG_FILE")
TESTING_URL = os.environ.get("TESTING_URL")
TEST_CASES_PATH = os.environ.get("TEST_CASES_PATH")
LOGIN_FILE_NAME = os.environ.get("LOGIN_FILE_NAME")
ADD_STORAGE_FILE_NAME = os.environ.get("ADD_STORAGE_FILE_NAME")

""" NECESSARY SETTINGS"""
ADD_USER = False
SELECTED_DAY = '15'
# SELECTED_TIME = '10'
CONTAINER_TYPE = "pod" # 'container' or 'pod'
PAYMENT_TYPE = "CARD"
PLAN = "POD" # 'Economy-POD' , 'POD' , 'First-Class'
# For now it is HARDCODED later will be autofetched from CSV file
ADD_STORAGE_SETTINGS = {
    "BEDROOM": True,
    "LIVING ROOM":False,
    "KITCHEN":False,
    "Office":False,
    "Garden-Garage":False,
    "OTHER":False,
    "PRESETS":False,

}

# Ensure LOG_FOLDER_NAME and LOG_FILE_NAME are not None
if not LOG_FOLDER_NAME or not LOG_FILE_NAME:
    raise ValueError("LOG_FOLDER_NAME and LOG_FILE_NAME must be set in the .env file")

LOG_DESTINATION = join(dirname(__file__), LOG_FOLDER_NAME)
LOG_PATH = join(LOG_DESTINATION, LOG_FILE_NAME)

"""Test Cases"""
AUTHENTICATION = []
USERS_TO_ADD = 10
ADD_USER_DETAILS = [
    {
        "first_name": "Emily",
        "last_name": "Johnson",
        "email": "emily.johnson@example.com",
        "mobile_number": "7912345678",
        "postal_code": "E1 6AN",
        "city": "London",
        "franchise_id": "F123456"
    },
    {
        "first_name": "James",
        "last_name": "Smith",
        "email": "james.smith@example.com",
        "mobile_number": "7861234567",
        "postal_code": "SW1A 1AA",
        "city": "London",
        "franchise_id": "F654321"
    },
    {
        "first_name": "Olivia",
        "last_name": "Williams",
        "email": "olivia.williams@example.com",
        "mobile_number": "7790123456",
        "postal_code": "W1A 1AA",
        "city": "London",
        "franchise_id": "F789456"
    },
    {
        "first_name": "Liam",
        "last_name": "Brown",
        "email": "liam.brown@example.com",
        "mobile_number": "7700987654",
        "postal_code": "N1 6EU",
        "city": "London",
        "franchise_id": "F321654"
    },
    {
        "first_name": "Sophia",
        "last_name": "Taylor",
        "email": "sophia.taylor@example.com",
        "mobile_number": "7911234567",
        "postal_code": "SE1 9SG",
        "city": "London",
        "franchise_id": "F987123"
    }
]
STORAGE_TYPE ={}


# Set up the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(CHROME_DRIVER_PATH)  # Update with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_test_cases():
    """For importing username and passwords """
    login_credentials = pd.read_csv(join(TEST_CASES_PATH,LOGIN_FILE_NAME),sep=",")
    print(login_credentials)
    usernames = login_credentials["username"]
    passwords = login_credentials["password"]
    for username, password in zip(usernames, passwords):
        if(username and password):
            AUTHENTICATION.append({"username": username, "password":password})
    """For imporing Add Storage options"""
    
    # Load the Excel file with all sheets
    df = pd.read_excel(join(TEST_CASES_PATH,ADD_STORAGE_FILE_NAME), sheet_name=None) 
    # Iterate over the sheets and print their names and content
    for sheet_name, sheet_data in df.items():
        categories=[]
        for type_, quantity in zip(sheet_data["Type"], sheet_data["Quantity"]):
            categories.append({
                "Type":type_,
                "Quantity":quantity
            })
        STORAGE_TYPE[sheet_name]=categories

    
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
    """Click on edit icon beside Contact Details to add user"""
    try:
        for i in ADD_USER_DETAILS:
            # Wait for and interact with the search bar
            search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'controllable-states-demo'))
            )
            search_bar.clear()
            search_bar.send_keys(i["email"])
            print("Search bar value set.")

            # Wait for and interact with the dropdown
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.MuiAutocomplete-popper'))
            )
            print("Dropdown is visible.")
            try:
                first_item = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiAutocomplete-option'))
                )
                print("First item is clickable.")
            except:
                item_not_found = True

            # Check if the mobile number matches
            try:
                print("First item is :",first_item)
                if item_not_found or i["mobile_number"] not in first_item.text :

                    # Click the 'Add User' button
                    add_user_dialog_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='symbol-label pointer']//button[@class='btn btn-link']"))
                    )
                    add_user_dialog_button.click()
                    print("Add user button is clicked")



                    # Fill out user details
                    first_name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "first_name"))
                    )
                    last_name_input = driver.find_element(By.NAME, "last_name")
                    email_input = driver.find_element(By.XPATH, "//div[@class='col-10 form-groupB w-100']//input[@name='email']")
                    mobile_number_input = driver.find_element(By.XPATH, "//input[@type='tel']")
                    postal_code_input = driver.find_element(By.NAME, "postcode")                 
                    
                    # Enter data into each input box
                    first_name_input.clear()
                    first_name_input.send_keys(i["first_name"])
                    last_name_input.clear()
                    last_name_input.send_keys(i["last_name"])
                    email_input.clear()
                    email_input.send_keys(i["email"])
                    mobile_number_input.clear()
                    mobile_number_input.send_keys(i["mobile_number"])
                    postal_code_input.clear()
                    postal_code_input.send_keys(i["postal_code"])

                    # Find and click the 'Save' button
                    all_buttons = driver.find_elements(By.TAG_NAME, "button")
                    save_button = next((btn for btn in all_buttons if btn.text == 'Save'), None)

                    if save_button is None:
                        raise Exception("Save button not found")

                    save_button.click()
                    print("User details saved")

                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.XPATH, "//span[@class='symbol-label pointer']//button[@class='btn btn-link']"))
                    )
                    print("Waited for save button to disappear")
                else:
                    search_bar.clear() 
            except:
                continue
    except Exception as e:
        print(f"An error occurred: {e}")



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

def choose_container():
        
        def find_button(name):
            return driver.find_element(By.XPATH, f"//input[@type='radio' and @value='{name}']")
        
        if CONTAINER_TYPE == 'pod':
            # find the pod option and click it 
            pod_radio_button = find_button('pod')
            time.sleep(5)
            pod_radio_button.click()

            print("Pod option clicked.")

        # still under process
        elif CONTAINER_TYPE == 'container':
            conatiner_radio_button = find_button('container')
            conatiner_radio_button.click()
            choose_button = driver.find_element(By.ID, "mui-component-select-container_id")
            choose_button.click()
            select_option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//li[@data-value='20ft Non-Ele']"))
            )
            select_option.click()
            # 

        # Find proceed button to click
        proceed_button = driver.find_element(By.XPATH, "//div[@class='modal-footer']//button[contains(text(),'Proceed')]")
        proceed_button.click()
        time.sleep(5)


def search_contact():
    """Set the value of the search bar, handle the dropdown, and select an item."""
    try:
        # Locate the search bar using its ID
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'controllable-states-demo'))
        )
        
        # Set the value of the search bar
        search_bar.send_keys('first@last')
        print("Search bar value set.")

        # Wait for the dropdown to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.MuiAutocomplete-popper'))
        )
        print("Dropdown is visible.")

        # Wait for the items in the dropdown
        first_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.MuiAutocomplete-option'))
        )
        print("First item is clickable.")

        # Select the first item from the dropdown
        first_item.click()
        print("First item clicked.")
        time.sleep(5)  # Wait for any possible loading

    except Exception as e:
        print(f"An error occurred: {e}")

def select_plan(PLAN):

    if PLAN == 'Economy-POD':
        print(f"Plan Selected : ${PLAN}")
        button = driver.find_element(By.XPATH, "//input[@value = 'Economy-POD' ]")

    if PLAN == 'POD':
        print(f"Plan Selected : ${PLAN}")
        button = driver.find_element(By.XPATH, "//input[@value = 'POD' ]")

    if PLAN == 'First-Class':
        print(f"Plan Selected : ${PLAN}")
        button = driver.find_element(By.XPATH, "//input[@value = 'First-Class' ]")

    button.click()
    time.sleep(5)





def add_storage_items():
    def select_tab(tab_name):
        tab = driver.find_element(By.XPATH,f"//a[contains(text(),'{tab_name}')]")
        tab.click()

    def get_item(selection_name):
        """To select living room item """
        try:
            item = driver.find_element(By.XPATH, f"//strong[contains(text(),'{selection_name}')]/ancestor::div[2]")
            actions = ActionChains(driver)
            # Hover over the element
            actions.move_to_element(item).perform()
            element = driver.find_element(By.XPATH, f"//strong[contains(text(),'{selection_name}')]/ancestor::div[contains(@class,'ItemsSelector__FurnitureDescription-sc-1y86vk7-8')]/preceding-sibling::div[1]//div//span[contains(@class, 'ta-add')]")
            return element
        except:
            return None

    def add_items():
        for item_key in ADD_STORAGE_SETTINGS.keys():
            time.sleep(5)
            
            # Check if the key exists in ADD_STORAGE_SETTINGS
            if ADD_STORAGE_SETTINGS.get(item_key) == True:
                select_tab(item_key)
                
                for item in STORAGE_TYPE.get(item_key, []):
                    selected_option = get_item(item["Type"])
                    if(selected_option== None):
                        continue
                    
                    try:
                        quantity = int(item["Quantity"])
                        for _ in range(quantity):
                            selected_option.click()
                    except ValueError:
                        print(f"Invalid quantity value: {item['Quantity']}")


    add_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Add/Edit Storage Items')]")
    add_button.click()
    time.sleep(5)

    try:
        total_tabs= ["BEDROOM" ,"LIVING ROOM" , "KITCHEN" , "Office" ,"Garden / Garage" , "OTHER" , "PRESETS"]
        """ Call add_items() to add items in storage"""
        add_items()
        time.sleep(5)
        calculate_button = driver.find_element(By.XPATH , "//div[contains(text(), 'CALCULATE')]")
        calculate_button.click()
        time.sleep(10)
        book_button = driver.find_element(By.XPATH, "//a[contains(text(),'Book')]")
        book_button.click()
        time.sleep(5)

    except TimeoutException:
        print("Element not found within the given time.")


def select_slot():
    get_slot_button = driver.find_element(By.XPATH,"//div[@class = 'edit-icon']//span//span")
    get_slot_button.click()
    time.sleep(5)
    select_date_button = driver.find_element(By.XPATH, f"//div[contains(text(),'{SELECTED_DAY}')]")
    select_date_button.click()
    time.sleep(2)
    select_time_button = driver.find_element(By.XPATH, "//div[@class='fc-event-title fc-sticky' and contains(text(), '3pm')]")
    select_time_button.click()
    time.sleep(2)
    get_save_button = driver.find_element(By.XPATH, "//div[@class='d-flex']//button[contains(text(),'Save')]")
    get_save_button.click()
    time.sleep(5)

def make_payment():
    try:
        # Wait until the elements are present in the DOM
        get_card_number_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(@class,'CardData')]//input[@id='cardnumber']"))
        )

        get_card_number_input.send_keys('4111111111111111')

        get_expiry_date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'exp-date'))
        )
        get_cvv_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'card-cvv-a5f53132-11c0-4fcf-b8b9-a922effc6a7c'))
        )

        # Input card details
       
        get_expiry_date_input.send_keys('0430')
        get_cvv_input.send_keys('111')

    except Exception as e:
        print(f"An error occurred: {e}")
    


def place_order():
    get_action_button = driver.find_element(By.XPATH,"//button[contains(text(), 'Action')]")
    get_action_button.click()
    get_make_payment_button = driver.find_element(By.XPATH,"//a[contains(text(), 'Make Payment')]")
    get_make_payment_button.click() 
    time.sleep(5)
    make_payment()
    time.sleep(10)
    place_order_button =  driver.find_element(By.XPATH, "//button[contains(text(),'Place Order')]") 
    place_order_button.click()
    time.sleep(10)

try:
    get_test_cases()
    for credentials in AUTHENTICATION:
        print(credentials)
        driver.get(TESTING_URL)
        # Maximize the browser window
        driver.maximize_window()
        login(credentials["username"], credentials["password"])
        # time.sleep(5)  # Consider using WebDriverWait here instead of sleep
        create_order()
        time.sleep(5)
        if(ADD_USER):
            add_user()
        search_contact()
        choose_container()
        select_plan(PLAN)
        add_storage_items()
        select_slot()
        place_order()
        time.sleep(10)  # Consider using WebDriverWait here instead of sleep

except Exception as e:
    log(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
finally:
    # Close the browser
    driver.quit()
