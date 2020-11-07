from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('headless')


class UrlAssembly:
    url = ''

    def __init__(self, *args, protocol, host, page='', net_lock='', query=''):
        def justify(elem):
            return str(elem).strip().strip('/').strip('\\').strip(':')

        self.url = f"{justify(protocol)}://{f'{justify(net_lock)}@' if net_lock else ''}{justify(host)}/"
        if page:
            self.url += f"{justify(page)}/"
        if query:
            self.url += f"?{query}"


class Driver(webdriver.Chrome):
    url = ''

    pages = {
        'login': 'auth/login/',
        'add_question': 'questions/add-question',
        'add_tournament_week': 'questions/add-tournament-week',
        'add_marafon_week': 'questions/add-theme-blocks-marafon-week'
    }

    class Url:
        def __init__(self, https, dev):
            self.protocol = 'https' if https else 'http'
            # self.host = 'dev.kolibrina.ru' if dev else 'kolibrina.ru'
            self.host = 'dev.kolibrina.ru'
            self.net_lock = 'Nillkizz:Vyjujxtujgjregfntkm'

    def __init__(self):
        super(Driver, self).__init__(chrome_options=chrome_options)

    def get(self, page):
        self.url = UrlAssembly(protocol=self.Url.protocol,
                               net_lock=self.Url.net_lock,
                               host=self.Url.host,
                               page=self.pages[page]).url
        super(Driver, self).get(self.url)

    def login(self, *args, dev=True, https=True):
        self.Url = self.Url(https, dev)
        self.get('login')
        self.find_element_by_id('id_username').send_keys('admin')
        self.find_element_by_id('password').send_keys('admin')
        self.find_element_by_id('sign_in').click()
        self.Url.net_lock = ''
