from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the Chrome WebDriver
chrome_options = Options()
 # Run in headless mode for background execution
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('C:\chromedriver-win64\chromedriver.exe')  # Update with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    postal_code = ['SW1A 1AA','EH21 6UU']
    for code in postal_code :
        # Navigate to Google
        with open("log.txt", 'a') as file:
            file.write(str(time.time()))
        driver.get("https://book.easystorage.com/")

        # Find the search box, enter a query, and submit
        input_pin_code_box = driver.find_element(By.TAG_NAME, 'input')
        input_pin_code_box.send_keys(code)
        input_pin_code_box.send_keys(Keys.RETURN)

        # Wait for results to load and fetch the titles of the search results
        driver.implicitly_wait(100)  # Implicit wait to handle dynamic content

        # Find all search result titles
        search_results = driver.find_elements(By.CSS_SELECTOR, "h3")
        for result in search_results:
            print(result.text)

except:
    # Close the browser
    driver.quit()

