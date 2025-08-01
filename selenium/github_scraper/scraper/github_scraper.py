from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def launch_browser():
    """Initialize webdriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chromedriver_path = 'C:\\Users\\karan\\Documents\\_dev\\chromedriver-win64\\chromedriver.exe'

    def create_webdriver():
        service = Service(executable_path=chromedriver_path)
        return webdriver.Chrome(service=service, options=options)
    
    browser = create_webdriver()
    return browser
    
def search_github(browser, query):
    """Search Github with search term"""
    search_url = f"https://github.com/search?q={query}&type=code&p=1"
    browser.get(search_url)

    #browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/main/react-app/div/div/div[1]/div/div/div[2]/div/div/div/div[4]/div/div')
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="prc-PageLayout-Content--F7-I"]')))
    print("Search results found.")

    #results = main_container.find_elements(By.XPATH, './/div[@class="Box-sc-g0xbh4-0 hmwxFk"]')
    #print("results found:", len(results))
    return True
    


#def extract_results(browser):
    """Extract search results from Github"""

if __name__ == "__main__":
    browser = launch_browser()
    query = "AWS_SECRET_ACCESS_KEY"

    test_search = search_github(browser, query)
    print(f"Search test result: {test_search}")
    