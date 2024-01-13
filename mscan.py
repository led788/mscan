import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import click


def look_high_bonuses(driver, percent):
    items = driver.find_elements(By.CSS_SELECTOR, 'div.item-block')

    print(f'found {len(items)} items')

    if len(items) > 0:
        for item in items:

            try:
                bonus = item.find_element(By.CLASS_NAME, 'bonus-percent').text
                bonus = int(re.sub(r'\D', '', bonus))

                if bonus > percent:
                    price = item.find_element(By.CLASS_NAME, 'item-price').text
                    price = int(re.sub(r'\D', '', price))
                    title = item.find_element(By.CLASS_NAME, 'ddl_product_link').text
                    link = item.find_element(By.CLASS_NAME, 'ddl_product_link').get_attribute('href')

                    print(f'{title=}')
                    print(f'{link=}')
                    print(f'{price=} {bonus=}')
            except NoSuchElementException:
                continue


@click.command()
@click.option('-n', '--pages', type=click.INT, required=True, help='Start megamarket category URL.')
@click.option('-p', '--percent', type=click.INT, required=True, help="A positive percent number.")
@click.argument('start_url', type=click.STRING, required=True)
def mscan(start_url, percent, pages):
    '''

    :param start_url:
    :param percent:
    :param pages:
    :return:
    '''
    driver = webdriver.Firefox()

    print(f'Start url: {start_url}')
    print(f'*** page 1')
    driver.get(start_url)
    time.sleep(2)
    look_high_bonuses(driver, percent)

    for page_num in range(2, pages + 1):
        print(f'*** page {page_num}')
        driver.get(start_url + 'page-' + str(page_num) + '/')
        time.sleep(2)
        look_high_bonuses(driver, percent)

    driver.close()


if __name__ == '__main__':
    mscan()