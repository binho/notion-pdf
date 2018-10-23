#!/usr/bin/python
# -*- coding: utf-8 -*-
import contextlib
import json
import os
import random
import sys
import time
from contextlib import contextmanager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

user_agents = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
)

def convert_to_pdf(urls, download_path):
    sleep = 6
    max_wait = 60
    width = 1280
    height = 720

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('window-size={},{}'.format(width, height))
    options.add_argument('--user-agent={}'.format(random.choice(list(user_agents))))
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--kiosk-printing')
    options.add_argument('--test-type')
    # options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')

    # Make sure "Save as PDF" is selected on print preview dialog
    # Ref: https://github.com/gingerbeardman/chrome-application-shortcuts/blob/master/Gmail.app/Contents/Profile/Default/Preferences
    appState = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local"
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False
    }

    # Converts ~/Downloads to /Users/<user>/Downloads
    expanded_download_path = os.path.expanduser(download_path)

    prefs = {
        'download.default_directory': os.path.normpath(expanded_download_path),
        'savefile.default_directory': os.path.normpath(expanded_download_path),
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'profile.default_content_settings.popups': 0,
        'plugins.always_open_pdf_externally': True,
        'printing.print_preview_sticky_settings.appState': json.dumps(appState),
        'disk-cache-size': 4096
    }
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',
                               chrome_options=options,
                               service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    browser.set_window_size(width, height)
    browser.set_page_load_timeout(max_wait)
    browser.set_script_timeout(max_wait)

    for url in urls:
        try:
            print('Loading URL: %s' % (url))
            browser.get(url)
        except:
            print('Failed to load URL: %s' % (url))

        try:
            notion_app_element = EC.presence_of_element_located((By.ID, 'notion-app'))
            WebDriverWait(browser, 10).until(notion_app_element)

            # add some extra time for images to finish loading
            time.sleep(5)

            # browser.execute_script("""
            # var head = document.getElementsByTagName('head')[0];
            # var style = '<style type="text/css" media="print">@page { size: A4; }</style>'
            # head.appendChild(style);
            # """)

            # Try to remove the login button from Notion before print
            try:
                login_button_element = browser.find_element_by_xpath("//a[@href='/login']")
                browser.execute_script('arguments[0].remove();', login_button_element)
            except:
                pass

            browser.execute_script('window.print();')
        except TimeoutException:
            print('Timed out waiting for page to load')

    browser.quit()
