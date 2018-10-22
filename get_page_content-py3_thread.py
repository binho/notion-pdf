#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
https://duo.com/decipher/driving-headless-chrome-with-python
https://medium.com/@pyzzled/running-headless-chrome-with-selenium-in-python-3f42d1f5ff1d
https://martin-thoma.com/scraping-with-selenium/
https://stackoverflow.com/questions/49642896/automate-print-save-web-page-as-pdf-in-chrome-python-3-6
"""

import time
import os
import browser
import notify_email
from threading import Thread
from queue import Queue
from util import *
from lxml import html
from operator import itemgetter

os.system('pkill -9 chromedriver')
os.system('pkill -9 chromium')

is_dev = 'binho' in os.environ.get('HOME')
max_workers = 3

class BrowserWorker(Thread):
   def __init__(self, queue):
       Thread.__init__(self)
       self.queue = queue

   def run(self):
        while True:
            item = self.queue.get()

            parsed_page = browser.get(item)
            print(parsed_page)

            self.queue.task_done()

queue = Queue()

for i in range(max_workers):
    worker = BrowserWorker(queue)
    worker.daemon = True
    worker.start()

items = ['https://www.notion.so/metalab/Onboarding-0573b66355d24854b67561c2f6b7050e']

for item in items:
    queue.put(item)

queue.join()
