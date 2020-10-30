import os
from zipfile import ZipFile

import requests

if 'chromedriver' not in os.listdir(os.getcwd()):
    url = 'https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip'
    chromedriver = requests.get(url)
    with open('chromedriver.zip', 'w+b') as file:
        file.write(chromedriver.content)
        with ZipFile(file, 'r') as zipObj:
            zipObj.extractall()
    os.remove(os.path.join(os.getcwd(), 'chromedriver.zip'))
