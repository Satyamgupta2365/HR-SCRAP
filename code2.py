from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()

chrome_path = !which chromium-browser  

if chrome_path:
    options.binary_location = chrome_path[0]
else:
    raise Exception("Chrome/Chromium executable not found. Please install it.")

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/login")
input("🔹 Log in to LinkedIn manually & press Enter to continue...")

company_name = "Google"  
search_query = f"https://www.linkedin.com/search/results/people/?keywords=HR%20Manager%20{company_name}"
driver.get(search_query)
time.sleep(5)

for _ in range(5):  
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

profiles = driver.find_elements(By.CLASS_NAME, "entity-result__title-text a")
data = []
for profile in profiles:
    try:
        name = profile.text.strip()
        link = profile.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({"Name": name, "Profile Link": link})
    except:
        continue

df = pd.DataFrame(data)
df.to_csv("linkedin_hr_profiles.csv", index=False)
print("✅ Data saved successfully!")

driver.quit()
