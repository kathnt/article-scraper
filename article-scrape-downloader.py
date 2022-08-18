from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import re
import csv
import random
from datetime import date, timedelta
from dateutil.relativedelta import *

from bs4 import BeautifulSoup

import time



from getpass import getpass

# pswd = getpass()

articles_list = ['Süddeutsche Zeitung (inkl. Regionalausgaben)', 'Corriere della Sera', 'Rossiyskaya Gazeta- Federal Issue',
'Mail & Guardian', 'El Pais', 'The Straits Times','Vietnam Plus','Le Figaro']


###########
# username and pass
usr = ''
pswd = ''
##########


# source
src = ''
src_abbr = ''


# keyword
keyword = '\"climate change\"'

keyword_no_quote = 'climate'

add_date = 30

# start
start_month = 8
start_day = 17
start_year = 2021

# end
end_month = 12
end_day = 31
end_year = 2021

path_to_chromedriver = ''
driver = webdriver.Chrome('./chromedriver')
driver.maximize_window()
time.sleep(2)

start_time = time.time()




# Search 

url = ''

# get website (first to login)
driver.get(url)
# time.sleep(2)

# login to database
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,'username'))).send_keys(usr)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,'password'))).send_keys(pswd)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID,'submit'))).click()


def newSearch(driver, keyword, src):
  
  # Open advanced search
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[normalize-space()="Advanced Search"]'))).click()

  time.sleep(random.randint(2,3))

  # Switch to 'News' tab
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[normalize-space()="News"]'))).click()

  # Enter keyword 'covid'
  # driver.find_element_by_class_name('searchterm-input-box').send_keys(keyword)
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,'searchterm-input-box'))).send_keys(keyword) 

  #time.sleep(1)
  time.sleep(random.randint(2,5))

#########################################

  # Choose English
  # WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'//input[@placeholder="Select one or more languages"]'))).send_keys("English")





  #time.sleep(random.randint(2,4))

  # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[normalize-space()="English"]'))).click()



####################################

  time.sleep(random.randint(3,6))

  # Choose source
  WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'//input[@placeholder="Enter one or more sources; then select from the list that appears"]'))).send_keys(src)

  # time.sleep(2)
  time.sleep(random.randint(3,5))

  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[text()="' + src + '"]'))).click()

  time.sleep(random.randint(2,6))

  # click search 
  # driver.find_element_by_xpath('//button[@data-action="search"]').click()
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-action="search"]'))).click()

  time.sleep(random.randint(4,8))
  #time.sleep(1)



  # click on translate option
  # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id=":0.targetLanguage"]/span/a/span[3]'))).click()
  # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[contains(text(), "英語")]'))).click()
  # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id=":1.menuBody"]/table/tbody/tr/td[19]/a[8]/div/span[1]'))).click()



  # Small adjustments to results

########################################################

  # toggle to group duplicates - REMOVED FOR NOW
  # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@data-action="toggleduplicates"]'))).click()

########################################################


  # click on 'Timeline' option
  # time.sleep(5)
  time.sleep(random.randint(5,8))

  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID,'podfiltersbuttondatestr-news'))).click()



# time.sleep(5)

# First search
newSearch(driver, keyword, src)




def changeDate(month, day, year):

  # month 1
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectmonthtimeline"]'))).click()
  time.sleep(random.randint(1,3))

  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datepicker"]/h3/div/ol/li[' + month + ']'))).click()
  # time.sleep(2)
  time.sleep(random.randint(2,4))

  # year
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="selectyeartimeline"]'))).click()
  time.sleep(random.randint(1,2))

  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[text()="' + year + '"]'))).click()
  time.sleep(random.randint(2,4))

  # date
  # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-monthday="' + str(1) + '"]'))).click()
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="datepicker"]/table/tbody/tr/td/button[@data-monthday="' + day + '"]'))).click()
  
  time.sleep(random.randint(3,6))

################################################

start_date = date(start_year, start_month, start_day)
end_date = date(end_year, end_month, end_day)
delta = timedelta(days=1)

month_check = start_month
day_count = 0
art_count = 0







while start_date <= end_date:

  time_for_day = time.time() 

  current_year = start_date.strftime('%Y')
  current_month = start_date.strftime('%m')
  current_day = start_date.strftime('%d')
 
  date_str = start_date.strftime("%Y-%m-%d")
  
  # print("date changed!")

  title_list = []
  dates_list = []

  day_count += 1

  # Since retrieving data separately for each day, just make a list of same date
  # if gathering over multiple days, comment out below
  # for i in range(len(title_list)):
    # dates_list.append(date_str)
  
  # since '0' is attached in front for single digit months and days
  # remove '0' to match the content of button in calendar
  if current_month[0] == '0':
    current_month = current_month[1]
  if current_day[0] == '0':
    current_day = current_day[1] 

  date_str = start_date.strftime("%Y-%m-%d")
  print('----------') 
  print('start:\t' + date_str)

  # make new query every 90 days
  if day_count > 90:
    driver.get("url")
    print('new query...')
    time.sleep(random.randint(5,8))
    newSearch(driver, keyword, src)
    # month_check = current_month
    day_count = 0


  time.sleep(random.randint(2,5))

  # choose start date
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Pick Minimum Date"]'))).click()
  changeDate(current_month, current_day, current_year)

  # start_date += relativedelta(months=+4)    # move to last day of next month here
  #start_date += relativedelta(day=31)
  
  # start_date += timedelta(days=1)

  # current_year = start_date.strftime('%Y')
  # current_month = start_date.strftime('%m')
  # current_day = start_date.strftime('%d')
  
 




  ########################################    take data per 2 months

  start_date += timedelta(days=add_date)

  current_year = start_date.strftime('%Y')
  current_month = start_date.strftime('%m')
  current_day = start_date.strftime('%d')
 
  print('end:\t' + start_date.strftime("%Y-%m-%d"))
  
  # since '0' is attached in front for single digit months and days
  # remove '0' to match the content of button in calendar
  if current_month[0] == '0':
    current_month = current_month[1]
  if current_day[0] == '0':
    current_day = current_day[1] 

  
#########################################

  # choose end date
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Pick Maximum Date"]'))).click()
  changeDate(current_month, current_day, current_year)

  # click OK to save dates
  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="date-form"]/button[@class="save btn secondary"]'))).click()

  time.sleep(random.randint(10,15))
  
  # print("date changed!")
  

  # time.sleep(5) 
  news_res = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/header/h2/span'))).text

  num_news = ""

  for c in news_res:
   if c.isdigit():
     num_news = num_news + c

  while int(num_news) > 9999:
    time.sleep(3)
    news_res = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="content"]/header/h2/span'))).text

    num_news = ""

    for c in news_res:
      if c.isdigit():
        num_news = num_news + c

  print('number of articles: ' + num_news)
  
  # w_file.write(date_str + ':\t' + num_news + '\n')

  # check that articles exist in date range
  if int(num_news) > 0:

    num_art = '1-' + num_news
    if num_news == '1':
      num_art = '1'
     

    # database used doesn't allow 1 article to be downloaded, need to download manually ******

    art_count += int(num_news)


  

    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Download"]'))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="results-list-toolbar-gvs"]/ul[1]/li[4]/ul/li[3]/button'))).click()

    time.sleep(random.randint(2,5))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID,'ResultsListOnly'))).click()
 
    time.sleep(random.randint(1,3))

    # choose xlsx option
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="XLSX"]'))).click()

    time.sleep(random.randint(2,4))

    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//input[@id="SelectedRange"]'))).click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/aside/form/div[4]/div[2]/div[1]/section/fieldset[1]/div[3]/div[1]/div/input'))).send_keys(num_art)


    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="XLSX"]'))).click()

    file_name = date_str + '-' + src_abbr + '-' + keyword_no_quote
  
    time.sleep(random.randint(3,6))

    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="FileName"]'))).clear() 
    time.sleep(random.randint(2,4))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="FileName"]'))).send_keys(file_name)
  
    time.sleep(random.randint(4,7))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//button[@data-action="download"]'))).click()


  start_date += delta

  print("time for " + date_str + ": %s seconds" % (time.time() - time_for_day))

  print('day count: ' + str(day_count))      # print day_count
  print('article count: ' + str(art_count))      # print art_count

  print('switching date...')
  time.sleep(random.randint(10,15))

  # click 'x' to change date 
  title_name = 'Timeline: ' + start_date.strftime("%b %d, %Y") + ' to ' + start_date.strftime("%b %d, %Y")

  WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-id="00000000-0000-0000-0000-000000000000"]'))).click()
  time.sleep(random.randint(8,12))

# print(len(title_list))
# print(len(dates_list))

# w_file.close()

print(src)


end_time = time.time()
print("--- %s seconds ---" % (end_time - start_time))
# print(day_count)


# driver.close()
