import os

from django.contrib import messages
from django.shortcuts import render
import time
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path

from website.models import Website


def spider(request, url):
    options = Options()
    '''options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(executable_path=binary_path, chrome_options=options)'''

    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')), chrome_options=options)

    try:
        driver.get(url)
        messages.success(request, 'Search was successful!')
    except InvalidArgumentException:
        messages.error(request, 'Invalid url...')

    time.sleep(10)
    text = driver.title

    driver.close()

    return text


def search(request):
    result = ''

    if request.method == 'POST':
        website = Website()
        url = request.POST['search']
        result = spider(request, url)

        website.title = result
        website.save()

    return render(request, 'search.html', {'result': result})
