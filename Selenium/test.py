from webdriver import WebDriver


def main():
    webdriver = WebDriver()
    webdriver.create()
    webdriver.scrape()
    webdriver.destroy()


if __name__ == '__main__':
    main()
