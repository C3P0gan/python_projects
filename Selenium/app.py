from flask import Flask
from webdriver import WebDriver

app = Flask(__name__)


@app.route('/')
def scrape():
    webdriver = None
    try:
        webdriver = WebDriver()
        webdriver.scrape()
    except Exception as e:
        print(f'An error has occurred: {str(e)}')
    finally:
        if webdriver:
            webdriver.destroy()
