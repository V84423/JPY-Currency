# -*- coding: utf_8 -*-
import sys
import time
import json
import re
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# connection.execute('set max_allowed_packet=67108864')
# connection.connect()
chrome_options = Options()

# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--user-data-dir=tmp')
# chrome_options.add_argument('--enable-logging')
# chrome_options.add_argument('--dump-dom')
# chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--headless')

chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--log-level=OFF')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-application-cache')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--verbose")

chrome_options.add_argument('--disable-browser-side-navigation')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--ignore-certificate-errors-spki-list')
# chrome_options.add_argument('--ignore-ssl-errors')
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

print("please insert start date")
s_dt = input()
print("please insert end date")
e_dt = input()

print("Scraping Date: " + s_dt + " ~ " + e_dt)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = chrome_options)

start = datetime.datetime.strptime(s_dt, "%Y-%m-%d")
end = datetime.datetime.strptime(e_dt, "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(1, (end-start).days+2)]

start_flag = False

for date in date_generated:
    drange = date.strftime("%Y%m%d")

    main_url = "https://info.jfx.co.jp/jfxphpapl/mnavi/mnavi_SwapPoint.php?stdate=P" + drange

    # print(main_url)

    driver.get(main_url)

    iframe = WebDriverWait(driver, 20).until(
	    EC.presence_of_element_located((By.XPATH, "//iframe[@name='SWAPSCREEN']")))
    
    f1 = driver.find_element(By.XPATH, "//td[@class='f1']")
    dt = f1.text

    dt.replace("<","")
    dt.replace(">","")
    dt = dt.strip()
    real_dt = dt
    dt = ''.join([n for n in dt if n.isdigit()])
    # print(dt)

    if start_flag == False and dt != start.strftime("%Y%m%d"):
    	continue

    start_flag = True

    driver.switch_to.frame(iframe)

    # Getting individual cities url
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trs = soup.findAll("tr", {"bgcolor" : "white"})

    print("===================================================================================")
    
    for tr in trs:
    	tds = tr.findAll('td')
    	currency = tds[0].getText()
    	buy = tds[4].getText()
    	sell = tds[5].getText()
    	print(real_dt + "   " + currency + "   " + buy + "   " + sell)
