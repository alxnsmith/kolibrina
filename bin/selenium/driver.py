from random import random
from time import sleep
from selenium import webdriver


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(chrome_options=options)

    def sign_in(self):
        self.driver.get('http://dev.kolibrina.ru/auth/login/')
        self.driver.find_element_by_id('id_username').send_keys('admin')
        self.driver.find_element_by_id('password').send_keys('admin')
        self.driver.find_element_by_id('sign_in').click()

    def get(self, url: str):
        self.driver.get(url)

    def select_category_and_theme(self, instance: str):
        def set_random():
            self.driver.find_elements_by_css_selector('#category_id option')[round(random() + 1)].click()
            sleep(0.5)
            themes = self.driver.find_elements_by_css_selector('#theme_id option')
            x = round(random() * (len(themes) - 2) + 1)
            themes[x].click()

        if instance == 'tournament':
            set_random()
        elif instance == 'marafon':
            for i in range(4):
                set_random()
                self.driver.find_element_by_id('add_theme_to_table_button').click()

    def fill_question_fields(self, instance: str):
        if instance == 'marafon':
            self.select_category_and_theme(instance)
            self.driver.find_element_by_id('add_theme_to_table_button').click()
            sleep(2)
        nums = self.driver.find_elements_by_class_name('circle_btn')
        for i in nums:
            if instance == 'tournament':
                if i.text != '01':
                    i.click()
                self.select_category_and_theme(instance)
            elif instance == 'marafon':
                i.click()
            self.driver.find_element_by_id('question_text').send_keys(f'{i.text} - question')
            self.driver.find_element_by_id('correct_answer').send_keys('+')
            self.driver.find_element_by_id('answer2').send_keys('answer2')
            self.driver.find_element_by_id('answer3').send_keys('answer3')
            self.driver.find_element_by_id('answer4').send_keys('answer4')
