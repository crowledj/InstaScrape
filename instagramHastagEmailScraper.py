  
#from scraper_api import ScraperAPIClient
import datetime
import itertools
## turn down level of v verbose by dwfauklt selenium webdriver logging , lol
import logging
import os
import pprint
import random
import re
import smtplib
import subprocess
import sys
import time
#strtime_file = time.time()
import timeit
from collections import defaultdict
from datetime import date
from smtplib import SMTPException

import requests
import selenium

import unidecode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (InvalidSessionIdException,
                                        NoSuchElementException,
                                        StaleElementReferenceException,
                                        NoSuchAttributeException,
                                        ElementClickInterceptedException, TimeoutException,
                                        ElementNotInteractableException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys

import csv #pandas as pd
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
req_proxy = RequestProxy(log_level=logging.ERROR) #you may get different number of proxy when  you run this at each time

 
#from googletrans import Translator
# init the Google API translator
#translator = Translator()

LOGGER.setLevel(logging.WARNING)

local_ch_link  =  'https://www.instagram.com'

#/explore/tags/crafts/

## TODO : must generalize this and add file to code bundle
DRIVER_PATH = r'chromedriver' #the path where you have "chromedriver" file.

all_categoies_list = ['Café', 'Restaurant',
'Médecins','Coiffure','Garage','Bureau d’architecture',
'Menuiserie','Entreprise de peinture','Agence immobilière',
'Pompes funèbres','Caves, encuvage',
'Institut de beauté','Installations sanitaires',
'Opticien','Fenêtres',
'Demenagements','Veterinaire','Maçonnerie','Fitness Center Institut de beauté',
'Construction métallique','Agencement de cuisines',
'Aménagement d’intérieurs','Location de véhicules','Parquet','Horlogerie Bijouterie',
'Boulangerie et pâtisserie ',
'Therapie naturelle','Association','Médecine traditionnelle chinoise',
'Clinique Ophtalmologique ','Minibus Taxi','Agence de voyages','Paysagistes ','Droguerie',
'Etablissement medico-social','Entreprise de construction',
'Atelier mécanique','Fruits et legumes','Magasin de sport','Ecole de danse',
'Location de tentes',
'Nutrition','Marbrerie','Pharmacie','Revêtements et sols','Auto-école',
'Massage de santé et de sport',
'Stores','Vitrerie','Personal training',
'Électroménager','Reparations','Reflexologie',
'Boucherie Charcuterie','Traiteur','Ferblanterie couverture','Vélos cycles',
'Electriciens installateurs','Ergotherapie ','Entreprise de nettoyage','Relooking']


options = Options()
options.headless = False#True
#options.LogLevel = False
#
# options.add_argument("--window-size=1920,1200")
#options.add_argument("--LogLevel=0")
#options.add_argument("user-agent= 'Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41' ")
options.add_argument("user-agent= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.698.0 Safari/534.24'")
driver_ = webdriver.Chrome(options=options, executable_path=DRIVER_PATH ) #, service_args=["--verbose", "--log-path=D:\\qc1.log"])
    

csvfile = open('intsaPeepsDeets.csv','w', newline='')
header = ('Name', 'Category', 'Website', 'Phone no.')
obj=csv.writer(csvfile)
obj.writerow(header)

csvfile.close()
#obj.close()

def write_2_csv(username='some_shit_company', num_followers ='1k', email='joeBloggs@hgmail.com'):

    global csvfile, obj
    csvfile = open('intsaPeepsDeets.csv','a', newline='')
    obj=csv.writer(csvfile)
    print('writing to file ... !!! s')
    try:
        obj.writerow( (username, num_followers, unidecode.unidecode(str(email[-1]))) )
    except UnicodeEncodeError as err:
        print('issue with writing to csv here -- now  -- eroor is ' + str(err) +  ' ...')
        pass     

    csvfile.close()

    return True


def scrapeLaad(driver):

    num_valais_businesses = 4402
    num_businesses_per_page = 11

    driver.get(local_ch_link)
    business_counter = 0
    errors_caught = 0
    page_counter = 1

    driver_inner = webdriver.Chrome(options=options, executable_path=DRIVER_PATH ) #, service_args=["--verbose", "--log-path=D:\\qc1.log"])

   # Login in girst gimp ..!

    #tar
    # get username
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    #enter username and password
    username.clear()
    username.send_keys("godlikester1")
    password.clear()
    password.send_keys("Keano_16")

    #target the login button and click it
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    #handle NOT NOW
    not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

    import time

    #target the search input field
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()

    #search for the hashtag cat
    keywords = ["#crafts",'#pets','#cork']
    #crafts
 
    tot_email_counter = 5000

    for keyword in keywords:

        valid_email_counter = 0
        
        try:
            searchbox.send_keys(keyword)
            
            # Wait for 5 seconds
            time.sleep(2)
            searchbox.send_keys(Keys.ENTER)
            time.sleep(2)
            searchbox.send_keys(Keys.ENTER)

        except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException, ElementClickInterceptedException, ElementNotInteractableException) as err:
            print('issue with first block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
            continue               
         
        time.sleep(3)

        main_pg_url = driver.current_url

        jump = 600
        new_start = 0
        new_end = jump
        
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        loopCount = 0
        emails = []
        last_final_index = 0
        while( valid_email_counter < tot_email_counter ):
                                                                #'//*[@id="react-root"]/div/div/section/main/article'
            # centra_page_elements = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/article/div')

            # if not centra_page_elements:
            #     #while not centra_page_elements:
            #     print('main page body web element non existant ! :( ')
            #         # common_link = pagination_link.split('page=')[0] + 'page=' + str(page_counter +1) + '&rid=833G'  
            #     return False
            #         # print('in infinite while until pagelements found -- page_counter = ' + str(page_counter) + ' -- trying newlyformed common link...')

            #         # # driver.close()
            #         # # driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH ) 

            #         # #strtcloseopenDriverTimer = time.time()
            #         # driver.get(common_link)
            #         # time.sleep(1)
            #         # centra_page_elements = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[1]/div')

            # else:

            #scroll down to scrape more images

    # TEST : replacing scrolling code with code from online - for infinite scrolling soc. media sites

            # driver.execute_script("window.scrollTo( " + str(new_start) + " , " + str(new_end) + " );")
            # new_start += jump
            # new_end = new_start + jump

            # time.sleep(5)
            

            if loopCount > 0:
                driver.get(main_pg_url)
                # Scroll down to bottom
            if loopCount >= 0:
                time.sleep(1.5)    
                driver.execute_script("window.scrollTo(  " + str(loopCount) +  ", "  + str(loopCount + 2) + "*document.body.scrollHeight);")

                # Wait to load page
                time.sleep(6*SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                time.sleep(2*SCROLL_PAUSE_TIME)
                if new_height == last_height and loopCount != 0:
                    break
                last_height = new_height

            loopCount += 1

            print('loop value = ' + str(loopCount) + ' ...')
            stuck_in_first_block = 0
            #driver.get(main_pg_url)
            if (loopCount % 1) == 0:
                time.sleep(2.25)    
                #target all images on the page
                images = driver.find_elements_by_tag_name('a')
                #links = [image.get_attribute('href') for image in images]

                start_indx = last_final_index
                print('going into the for loop of images again : start_indx = ' + str(start_indx) + ' -- len(images) = ' + str(len(images)) + ' -- len(images)-23 = ' + str(len(images)) + ' ...')
                for index  in range(start_indx,len(images)):
                    #driver.navigate.refresh()
                    # if index > 0:
                    #     driver.get(main_pg_url)

                    if stuck_in_first_block > 3:
                        driver.back()
                        time.sleep(2.25)
                        stuck_in_first_block = 0
                        #continue

                    try:

                        time.sleep(1.5)    
                        driver.execute_script("window.scrollTo(  " + str(loopCount) +  ", "  + str(loopCount + 2) + "*document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(6*SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        time.sleep(2*SCROLL_PAUSE_TIME)
                        
                        time.sleep(1.25)
                        images_in_loop = driver.find_elements_by_tag_name('a')
                        num_images = len(images_in_loop)
                        if index < len(images):
                            time.sleep(2.75)
                            outer_clikableElment = images_in_loop[index].find_element_by_xpath('./..')
                        else:
                            break

                        #if type(outer_clikableElment) == WebEl
                            
                        #outer_clikableElment.click()
                        time.sleep(3.25)
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div")))

                        outer_clikableElment.click()
                            
                    except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException, ElementClickInterceptedException, ElementNotInteractableException) as err:
                        print('issue with first block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                        stuck_in_first_block += 1
                        continue    

                    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, './.'))).click()
                    #time.sleep(0.5)

            ## 1).  Check this popups text content for an emil ....        
                    try:
                        elm = driver.find_element_by_tag_name('body')
                        texts = elm.text
                    except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException) as err:
                        print('issue with second block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                        continue   

                    mail_address= ''
                    # if '@' in texts and '.' in texts:
                    #     # pattern = "\S+@*\n" #this wild card doesnt appear to work?
                    #     mail_address = re.findall('\S+@\S+', texts)

                    # if mail_address != '' an5d len(mail_address) == 0:
                    #     print(mail_address )
                    #     write_2_csv(Username, num_Follwers, mail_address)    

                    time.sleep(1.5)    

                    try:
            ## 2).  Go to actual page of poster to check text for email
                        head = elm.find_elements_by_tag_name('header')
                        time.sleep(1.5)
                        if len(head) >= 1:
                            a_lnks = head[-1].find_elements_by_tag_name('a')
                        else:
                            continue    

                    except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException) as err:
                        print('issue with third block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                        parent = driver.back()
                        granparent = driver.back()
                        continue                           
                    #poster_pg_linbk = a_lnks[1].get_attribute('href') 

                    if len(a_lnks) >= 2:
                        Username = str(a_lnks[1].text)
                        try:
                            a_lnks[1].click()
                        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException) as err:
                            parent = driver.back()
                            granparent = driver.back()
                            print('issue with fourth block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                            continue                              

                    try:                                        
                        #follower_elm = elm.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')
                                                                                                          # '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'  
                                                                                                          # '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'    
                        #time.sleep(2.5)                                                                                    
                        follower_elm = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')))
                        check = -1
                        time.sleep(2.5)
                        num_Follwers = follower_elm.get_attribute('title')

                    except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException, TimeoutException) as err:
                        #parent = driver.back()
                        #granparent = driver.back()
                        granparent = driver.back()
                        num_Follwers = 'N/A'
                        print('issue with fifth block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                        pass                          

                    try:        
                        elm_inner = driver.find_element_by_tag_name('body')
                        inner_texts = elm_inner.text
                    except (StaleElementReferenceException, NoSuchElementException, NoSuchAttributeException) as err:
                        print('issue with sixth block after scrolls, skipping this post for now  -- eroor is ' + str(err) +  ' ...')
                        parent = driver.back()
                        granparent = driver.back()
                        continue      

                    split_inner_texts = inner_texts.split('\nJobs\nHelp\nAPI\nPrivacy\nTerms')
                    if len(split_inner_texts) >= 1:
                        relvant_inner_texts =  split_inner_texts[0]

                    #inner_texts_pieces = relvant_inner_texts.split('\n')
                    print(' Done processing post no. ' + str(index) + ' ....')
                    
                    if '@' in split_inner_texts[0]:
                        #pattern_iner = "\S+@*\n" #this wild card doesnt appear to work?
                        #compiled_iner = re.compile(pattern)
                        #soln = compiled_iner.search(inner_texts)
                        mail_address = re.findall('\S+@\S+', split_inner_texts[0])
                        
                    if  len(mail_address) != 0:
                        if mail_address[-1] != '' :
                            print(mail_address )
                            valid_email_counter += 1
                            write_2_csv(Username, num_Follwers, mail_address)

                    #grand_parent_elm = elm_inner.find_element_by_xpath('./..')
                    time.sleep(1.5)
                    ## then use another driver to go to this link ..., or click it ( a_lnks.click() ...?? )

                    parent = driver.back()
                    granparent = driver.back()
                #images = images[:-2]
  
            last_final_index = index
            #print('Number of scraped images: ', len(images))
            print('Counter of scraped images: ', loopCount)

            

                #for index, block in enumerate(centra_page_elements[1:]):

                    # #//*[@id="react-root"]/div/div/section/main/article/div[1]/div/div
                    # panels = driver.find_elements_by_xpath('.//div/div')
                    # for rows in panels:
                    
                    #     row = rows.find_elements_by_xpath('.//div')
                    #     for pic in row:
                    
                    #         btn_click_retVal = pic.click()
                    #         check = 1   


                # the text in link where a given pic takes u to..
                # //*[@id="react-root"]/section/main/div/div[1]/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span                      

    return True

        #print('shop no. = ' + str(index))
        #index = len(centra_page_elements) - 1
        # 
        # 
        # 



    #     if index == 0 and len(centra_page_elements) == 1:

    #         # common_link = pagination_link.split('page=')[0] + 'page=' + str(page_counter) + '&rid=833G'  
    #         # driver.get(common_link)

    #         # page_counter += 1

    #         break
    #         #continue

    #     elif index == 0 and len(centra_page_elements) != 1:
    #         continue
        
    #     elif index == len(centra_page_elements) - 1:
    #         try:

    #             #strtFinalBlockTimer = time.time()
                
    #             #pagination_display_num = (page_counter + 1) % 4
    #             pagination_display_num = page_counter
    #             # print('pagination_display_num  = ' + str(pagination_display_num))
    #             # #xpath_find_str = './/div/ul/li[' + str(pagination_display_num) + ']/a'
    #             xpath_find_str = './/div/ul/li[2]/a'
    #             pagination_link = shop.find_element_by_xpath(xpath_find_str).get_attribute('href')

    #             # if business_counter < 25:0  
    #             #     orig_pagination_link = pagination_link
                    
    #             # if not pagination_link:
    #             #     pagination_link = orig_pagination_link

    #             if page_counter == 4:
    #                   page_counter = 4

    #             common_link = pagination_link.split('page=')[0] + 'page=' + str(page_counter) + '&rid=833G'  

    #             # driver.close()
    #             # driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH ) 

    #             #strtcloseopenDriverTimer = time.time()
    #             driver.get(common_link)

    #             #endcloseopenDriverTimer = time.time()
    #             #print('Time in get Driver call = ', str(endcloseopenDriverTimer - strtcloseopenDriverTimer))                 

    #             #print(' pagination_link = ' + str(common_link))
    #             #time.sleep(1)
    #             #driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[1]/div')                      
    #             page_counter += 1
    #             #time.sleep(1) 
    #             #endFinalBlockTimer = time.time()
    #             #print('Time in main FinalBlock = ', str(endFinalBlockTimer - strtFinalBlockTimer))    

    #             if page_counter == 23 or page_counter == 24:
    #                 check = 1


    #         except (NoSuchAttributeException, KeyError, IndexError, StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException) :
    #             print("Error caught in the final elif block   :( .....")
    #             business_counter += 11
    #             errors_caught += 1
    #             continue
    #     else:

    #         #strTimer = time.time()
    #         company_name_address_etc_info = shop.text.split('\n')  
            
    #     ## NB !!    ## NOte : this a - element list's final element should have the company's website in it's href !! 

    #         try:
    #             if len(company_name_address_etc_info) >= 3:
    #                 company_name   = company_name_address_etc_info[0]
    #                 category = company_name_address_etc_info[2] 
    #             elif len(company_name_address_etc_info) < 3:    
    #                 company_name   = company_name_address_etc_info[0]
    #                 category = 'N/A'
    #             else:    
    #                 company_name   = 'N/A'
    #                 category = 'N/A'
    #         except (NoSuchAttributeException, KeyError, IndexError, StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException)  :
    #                 print("Error caught in attempt to grab or go to pagination link  0 :( .....")
    #                 business_counter += 1
    #                 errors_caught += 1
    #                 write_2_csv(company_name, category, company_tel_no, website_name)
    #                 continue                   
    #         if 'www' in shop.text.lower():
    #             try:
    #                 company_tel_no = company_name_address_etc_info[-1].split('www.')[0]
    #                 website_name = company_name_address_etc_info[-1].split('www.')[1]
    #             except:
    #                 print("Error caught in attempt to grab or go to pagination link  1 :( .....")
    #                 business_counter += 1
    #                 errors_caught += 1
    #                 write_2_csv(company_name, category, company_tel_no, website_name)
    #                 continue                        

    #         elif 'site internet' in shop.text.lower():
    #             try:
    #                 company_phone_email_etc_info_list = shop.find_elements_by_xpath('.//div/div[2]/div[2]/a')
    #                 if len(company_phone_email_etc_info_list) >= 3:
                        
    #                     company_tel_no = company_phone_email_etc_info_list[2].get_attribute('href') 
    #                     try:
    #                         website_name   = company_phone_email_etc_info_list[-1].get_attribute('href')
    #                     except (NoSuchAttributeException, KeyError, IndexError, StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException)  :
    #                         print("Error caught in attempt to grab website name in 'site internet' block  in the 'pagination link2' block( .....")
    #                         business_counter += 1
    #                         errors_caught += 1
    #                         website_name = 'N/A'
    #                         write_2_csv(company_name, category, company_tel_no, website_name) 
    #                         continue                             

    #                 elif len(company_phone_email_etc_info_list) == 1 or  len(company_phone_email_etc_info_list) == 2 :
    #                     website_name = company_phone_email_etc_info_list[-1].get_attribute('href') 
    #                     company_tel_no   = 'N/A'
    #                 else:
    #                     company_tel_no = 'N/A'
    #                     website_name = 'N/A'                           
    #             except (NoSuchAttributeException, KeyError, IndexError, StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException) :
    #                 print("Error caught in attempt to grab or go to pagination link  2 :( .....")
    #                 business_counter += 1
    #                 errors_caught += 1
    #                 write_2_csv(company_name, category, company_tel_no, website_name)
    #                 continue                        

    #         else:
    #             try:
    #                 if len(company_name_address_etc_info) >= 2:
    #                     company_tel_no = company_name_address_etc_info[-2]
    #                 elif len(company_name_address_etc_info) == 1:
    #                     company_tel_no = company_name_address_etc_info[-1]
    #                 else:
    #                     company_tel_no = 'N/A'    
    #             except (NoSuchAttributeException, KeyError, IndexError, StaleElementReferenceException, NoSuchElementException, InvalidSessionIdException) :
    #                 print("Error caught in attempt to grab or go to pagination link  3 :( .....")
    #                 business_counter += 1
    #                 errors_caught += 1
    #                 write_2_csv(company_name, category, company_tel_no, website_name)
    #                 continue 

    #         #endTimer = time.time()
    #         #print('Time in main else loop of scraping n pagination stuff = ', str(endTimer - strTimer))    

    #         #company_phone_email_etc_info = shop.find_element_by_xpath('.//div/div[2]/div[2]/a')  

    #         #company_website = company_phone_email_etc_info[-1].get_attribute('href')

    #         contcat_info_links = []
    #         # for a_sub_elements in company_phone_email_etc_info:
    #         #     contact_datas = a_sub_elements.get_attribute('href')
    #         #     contcat_info_links.append(contact_datas)

    #         #print('writing to .csv file --  business_counter = ' + str(business_counter) + ' -- errors_caught = ' + str(errors_caught))
    #         #strtimerCsvWriting = time.time()
    #         write_2_csv(company_name, category, company_tel_no, website_name)

    #         #endTimerCsvWriting = time.time()
    #         #print('Time in csv writing.. = ', str(endTimerCsvWriting - strtimerCsvWriting)) 

    # business_counter += num_businesses_per_page
    print('Done with page ' + str(page_counter) + ' -- writeen 11 lines  to .csv file --  business_counter = ' + str(business_counter) + ' -- errors_caught = ' + str(errors_caught))
print('finished file !! ')
#csvfile.close()
   

if __name__ == '__main__':


    PROXY_COUNTER = 0
    proxies = req_proxy.get_proxy_list()


    if PROXY_COUNTER == len(proxies) - 1:
        proxies = req_proxy.get_proxy_list()

    PROXY = proxies[PROXY_COUNTER].get_address()
    driver_ = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

    webdriver.DesiredCapabilities.CHROME['proxy']={
        "httpProxy":PROXY,
        "ftpProxy":PROXY,
        "sslProxy":PROXY,
        "proxyType":"MANUAL",
    }

    PROXY_COUNTER += 1
    # waitr a delay time to refresh sites parsings....
    #if  (not justParsed) :

    if scrapeLaad(driver_): #all_srpaed_sites_data):
        pass

    blaj = -1
