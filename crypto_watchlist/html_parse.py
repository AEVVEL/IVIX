import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from schemas import Coin

logger = logging.getLogger(__name__)

def parse_coins(driver: webdriver, retry_counter: int = 0):
    if retry_counter >= 5:
        return False

    current_url = driver.current_url
    page_coins_info = []
    try:
        coins = driver.find_elements(By.XPATH,"//tbody/tr")
        for i in range(len(coins)):
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", coins[i])
            WebDriverWait(driver, 5).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            coins = driver.find_elements(By.XPATH,"//tbody/tr")

            page_coins_info.append(Coin(
                rank=coins[i].find_element(By.XPATH,".//p[@class='sc-71024e3e-0 biekbf']").text,
                name=coins[i].find_element(By.XPATH,".//p[@class='sc-65e7f566-0 iPbTJf coin-item-name']").text,
                symbol=coins[i].find_element(By.XPATH,".//p[@class='sc-65e7f566-0 byYAWx coin-item-symbol']").text,
                price=coins[i].find_element(By.XPATH, ".//div[contains(@class, 'sc-142c02c-0 lmjbLF')]").text,
                day_price_change=coins[i].find_element(By.XPATH, "(.//span[contains(@class, 'sc-1e8091e1-0')])[2]").text,
                market_cap=coins[i].find_element(By.XPATH,".//span[@class='sc-11478e5d-1 jfwGHx']").text,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                parse_type="html"
            ))

        return page_coins_info

    except Exception as ex:
        driver.get(current_url)
        logger.warning(f"Error parse_coins: {retry_counter}. Link: {current_url}. Reason: {ex}")
        return parse_coins(driver, retry_counter + 1)


def start_html_parse(pages_to_parse: int):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    try:
        target_url = "https://coinmarketcap.com/"
        driver.get(target_url)

        total_coins_info = []
        for page_index in range(1, pages_to_parse+1):
            target_url = f"https://coinmarketcap.com/?page={page_index}"
            driver.get(target_url)
            WebDriverWait(driver, 5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            page_coins_info = parse_coins(driver=driver)
            if not page_coins_info:
                raise Exception("Failed to parse coins")

            total_coins_info += page_coins_info

        driver.close()
        return total_coins_info

    except Exception as ex:
        driver.close()
