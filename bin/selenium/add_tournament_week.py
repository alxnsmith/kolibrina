#!/venv/bin python
from driver import Driver


def main():
    driver = Driver()
    driver.sign_in()
    driver.get('https://Nillkizz:Vyjujxtujgjregfntkm@dev.kolibrina.ru/questions/add-tournament-week')

    driver.fill_question_fields('tournament')


if __name__ == '__main__':
    main()