from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


class WebDriver:
    def __init__(self):
        self.service = Service(GeckoDriverManager().install())
        self.driver = None

    def create(self):
        self.driver = webdriver.Firefox(service=self.service)


    def scrape(self):
        _url = 'https://www.google.com/'

        self.create()
        print(self.driver)
        self.driver.get(_url)


    def destroy(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None
