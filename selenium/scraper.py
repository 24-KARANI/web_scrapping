import pandas as pd
from selenium import webdriver 
from selenium .webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incongnito")
chromedriver_path = 'C:\\Users\\karan\\Documents\\_dev\\chromedriver-win64\\chromedriver.exe'  

def create_webdriver():
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_option)

browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

# Get all project titles and URLs
projects = browser.find_elements(By.XPATH, "//h1[@class='h3 lh-condensed']")
project_list = {}
for proj in projects:
    proj_name =proj.text
    proj_url = proj.find_elements(By.XPATH, "a")[0].get_attribute('href')
    project_list[proj_name] = proj_url

browser.quit()
# Convert the project list to a DataFrame and save it as CSV
project_df = pd.DataFrame.from_dict(project_list, orient = 'index')
project_df['project_name'] = project_df.index
project_df.columns = ['project_url', 'project_name']
project_df = project_df.reset_index(drop=True)
project_df.to_csv('project_list.csv')

#print(project_df)

# for parallelization
"""

def scrape_url(url):
    new_browser = create_webdriver()
    new_browser.get(url)

# Extract required data
# ...

new_browser.quit()

return data

with ProcessPoolExecutor(max_workers=4) as exercutor:
    furture_results = {executor.submit(scrape_url, url) for url in urlarray}

results = []
for furture in concurrent.futures.as_completed(furture_results):
    results.append(furture.result())

    """