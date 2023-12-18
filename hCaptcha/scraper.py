import time
from random import randint, random
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless

APIKEY = '24d1ed9554123e9703c246dcd7902949'


def scrape():
    service = Service(ChromeDriverManager().install())
    options = Options()

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless=new')
    options.add_argument('--start-maximized')

    URL = """
    https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp
    """

    CNPJ = '05330384000124'

    driver = Chrome(service=service, options=options)
    driver.get(URL)

    _input = WebDriverWait(driver, 7, ignored_exceptions=ElementNotVisibleException).until(
        EC.visibility_of_element_located((By.ID, 'cnpj'))
    )
    actions = ActionChains(driver)
    actions.move_to_element(_input).click().perform()
    [actions.pause(random()).send_keys(x).perform() for x in CNPJ]

    data_sitekey = driver \
        .find_element(By.CLASS_NAME, 'h-captcha') \
        .get_attribute('data-sitekey')

    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key(APIKEY)
    solver.set_website_url('https://solucoes.receita.fazenda.gov.br/')
    solver.set_website_key(data_sitekey)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        # insere a resposta do desafio hCaptcha
        driver.execute_script(
            f"""
            document.querySelector('textarea[name="h-captcha-response"]').innerHTML = '{g_response}'
            """
        )
        time.sleep(randint(2, 3))  # aguarda 2~3 segundos
        # envia o formulário
        driver.execute_script(
            "document.getElementById('frmConsulta').submit();"
        )
        time.sleep(randint(4, 5))  # aguarda 4~5 segundos
        driver.save_screenshot('pretty_please.png')

    else:
        print("task finished with error", solver.error_code)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    scrape()
