from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = True
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://indiaai.gov.in/startup/all')

# Wait for the dynamic content to load
time.sleep(140)

# Scroll down to the bottom of the page to load all startups
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

# Wait for the content to load after scrolling
time.sleep(10)

startup_elements = driver.find_elements(By.CSS_SELECTOR, '.card-footer')
startup_names = [element.text for element in startup_elements]

explore_buttons = driver.find_elements(By.LINK_TEXT, 'Explore')
startup_links = [button.get_attribute('href') for button in explore_buttons]

driver.quit()

with open('startup_links.txt', 'w', encoding='utf-8') as file:
    for link in startup_links:
        file.write(f"{link}\n")

print(f"Updated list of startup links saved to 'startup_links.txt'.")

for link in startup_links:
    print(link)