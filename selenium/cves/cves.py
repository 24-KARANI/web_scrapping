from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from pymongo import MongoClient

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.now().strftime('%Y-%m-%d')
url = f"https://www.cvedetails.com/vulnerability-search.php?f=1&publishdatestart={yesterday}&publishdateend={today}"

driver_option = webdriver.ChromeOptions()
driver_option.add_argument("--incognito")
chromedriver_path = 'C:\\Users\\karan\\Documents\\_dev\\chromedriver-win64\\chromedriver.exe'

def create_webdriver():
    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=driver_option)

browser = create_webdriver()
browser.get(url)

# MongoDB integration
client = MongoClient('mongodb://localhost:27017/')
db = client['cves_db']
collection = db['cves']

# Get all CVE IDs and summaries
try:
    cves = browser.find_elements(By.XPATH, '//div[@class="row" and div[@class="col-md-9"] and div[@class="col-md-3"]]')
    cves_list = {}
    for cve in cves:
        cve_link = cve.find_element(By.XPATH, './/h3/a')
        cve_id = cve_link.text
        cvss = cve.find_element(By.XPATH, './/div[@data-tsvfield="maxCvssBaseScore"]').text
        cve_pd = cve.find_element(By.XPATH, './/div[@data-tsvfield="publishDate"]').text
        cve_summary = cve.find_element(By.XPATH, './/div[@class="cvesummarylong py-0"]').text

        cve_doc = {
            'cve_id': cve_id,
            'cvss': cvss,
            'cve_pd': cve_pd,
            'cve_summary': cve_summary 
        }

        # Insert the CVE document into MongoDB
        if collection.count_documents({"cve_id": cve_doc['cve_id']}) == 0:
            collection.insert_one(cve_doc)
            print(f"Inserted: {cve_doc['cve_id']} to db")
        else:
            print(f"Already exists: {cve_doc['cve_id']} in db")
    """ 
    # Store the CVE details in a dictionary
        cves_list[cve_id] = {
            'cve_id': cve_id,
            'cvss': cvss,
            'cve_pd': cve_pd,
            'cve_summary': cve_summary
        }
    """
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    browser.quit()
    
"""
# Convert the CVE list to a DataFrame and save it as CSV
import pandas as pd

cve_df = pd.DataFrame.from_dict(cves_list, orient='index')
cve_df['cve_id'] = cve_df.index
cve_df.columns = ['cve_id', 'cvss', 'cve_pd', 'cve_summary']
cve_df = cve_df.reset_index(drop=True)
cve_df.to_csv('cve_list.csv', index=False)
"""

