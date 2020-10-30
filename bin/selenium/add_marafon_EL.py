from random import choice
from time import sleep

from modules.driver import Driver


def add_random_theme():
    def themes():
        return driver.find_elements_by_css_selector('#theme_id > option')[1:]

    categories = driver.find_elements_by_css_selector('#category_id > option')[1:]
    choice(categories).click()

    while True:
        if len(themes()) > 0:
            break
    sleep(0.1)
    choice(themes()).click()


if __name__ == '__main__':
    driver = Driver()
    driver.login()
    driver.get('add_marafon_week')

    for i in range(4):
        add_random_theme()
        driver.find_element_by_id('add_theme_to_table_button').click()
    driver.find_element_by_id('add_theme_to_table_button').click()

    circle_btns = driver.find_elements_by_css_selector('.circle_btn')
    sleep(1)
    for btn in circle_btns:
        btn.click()
        driver.find_element_by_id('question_text').send_keys(
            f'num: {btn.text}, difficulty: {btn.get_attribute("data-difficulty")}')
        driver.find_element_by_id('correct_answer').send_keys('Correct')
        driver.find_element_by_id('answer2').send_keys('answer2')
        driver.find_element_by_id('answer3').send_keys('answer3')
        driver.find_element_by_id('answer4').send_keys('answer4')
