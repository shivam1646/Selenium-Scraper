import os
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Linkedin():

    def __init__(self):
        self.url = 'https://in.linkedin.com'
        # Chrome driver path
        self.driver_path = os.path.join(os.getcwd(), 'chromedriver')
        self.driver = webdriver.Chrome(self.driver_path)

    def page_load(self):
        self.driver.get(self.url)

    def sign_in(self):
        # goto sign in page
        self.driver.find_element_by_xpath("//*[contains(text(),'Sign in')]").click()

        # Enter Credentials
        self.driver.find_element_by_id('username').send_keys('ENTER_USERNAME')
        self.driver.find_element_by_id('password').send_keys('ENTER_PASSWORD')

        # Sign in
        self.driver.find_element_by_xpath("//*[@type='submit']").click()

    def search(self):
        # goto jobs
        nav_bar_elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'global-nav__primary-item')))
        nav_bar_elements[2].click()

        # close message popup
        msg_popup_items = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'msg-overlay-bubble-header__control--new-convo-btn artdeco-button artdeco-button--circle artdeco-button--muted')]")))
        msg_popup_items[1].click()

        # Enter search params
        keyword_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'jobs-search-box-keyword-id-ember')]")))
        keyword_field.send_keys('full stack')
        location_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'jobs-search-box-location-id-ember')]")))
        location_field.send_keys('Pune')

        # Search jobs
        search_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Search']")))
        search_btn.click()

        time.sleep(10)
        # Here we fetched driver page source from driver.
        page_html = self.driver.page_source
        self.soup = BeautifulSoup(page_html, 'html.parser')

    def create_csv_file(self):
        row_headers = ["Position", "Company Name", "Posted"]
        self.csv_file = open('linkedin_jobs.csv', 'w', newline='', encoding='utf-8')
        self.linkedin_jobs = csv.DictWriter(self.csv_file, fieldnames=row_headers)
        # writeheader is pre-defined function to write header
        self.linkedin_jobs.writeheader()

    def save_data_in_file(self):
        # fetch job containers
        job_containers = (self.soup.find_all('div', class_='job-card-container'))
        for container in job_containers:
            position = container.find('a', class_='job-card-list__title').text            
            try:
                company_name = container.find('a', class_='job-card-container__company-name').text
            except:
                company_name = 'Data not available'
            posted = container.find('time').text
            print(position, company_name, posted, type(company_name))
            # TODO: data does not get written in file. Need to fox.
            self.linkedin_jobs.writerow({"Position": str(position), "Company Name": str(company_name), "Posted": str(posted)})

    def end_scraper(self):
        self.driver.quit()
        self.csv_file.close()

if __name__ == "__main__":

    linkedin = Linkedin()
    linkedin.page_load()
    linkedin.sign_in()
    linkedin.search()
    linkedin.create_csv_file()
    linkedin.save_data_in_file()
    linkedin.end_scraper()