#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:17:27 2018

@author: tnightengale
"""

from selenium import webdriver
import os
import time
import datetime
import random


class kijiji():
    
    def __init__(self):
        self.current_dir = os.getcwd()
        self.user = os.environ['KIJIJI_EMAIL']
        self.password = os.environ['KIJIJI_PASS']
        self.create_title_list()
        self.create_price_schedule()
        self.description = open('description.txt','r').read()
        print('Titles list is {}'.format(self.titles))
        self.current_ad_title = None
        self.current_ad_price = None
        
    def create_price_schedule(self):
        '''
        Asks for a lower an upper bound and 
        generates a price schedule to cycle through.
        '''
        upper = int(input('Enter your upper price bound: '))
        lower = int(input('Enter your lower price bound: '))
        self.price_schedule = list(range(lower,upper,10))
    
    def schedule_choice(self):
        '''
        Returns decending values from the price_schedule
        attribute until the lower bound is hit and then
        only return the lower bound.
        '''
        if len(self.price_schedule) == 1:
            current_price = self.price_schedule[0]
        else:
            current_price = self.price_schedule.pop()
        
        return current_price
        
    def create_title_list(self):
        '''
        Reads the titles.txt file in the
        folder the script is run in and 
        creates a list of titles and
        assigns it to self.titles.
        '''
        file = open('titles.txt','r')
        self.titles = []
        while True:
            line = file.readline().strip()
            if line == '':
                break
            else:
                self.titles.append(line)
        file.close()
    
    def random_title(self):
        '''
        Returns a random title from the created
        list of titles.
        '''
        return self.titles[random.randint(0,len(self.titles)-1)]
        
        
    def next_url(self,new_url):
        '''
        Waits till new page is loaded.
        '''
        current = self.kjj.current_url
        self.kjj.get(new_url)
        wait = time.time() + 10 # add 10 second time out
        while current == self.kjj.current_url and time.time() < wait:
            time.sleep(1)
            
    def next_click(self,e_to_click):
        '''
        Waits till next click is loaded.
        '''
        current = self.kjj.current_url
        e_to_click.click()
        wait = time.time() + 10 # add 10 second time out
        while current == self.kjj.current_url and time.time() < wait:
            time.sleep(1)
            
            
    def access_kijiji(self):
        '''
        Create driver and go to Kijiji.
        '''
        
        chrome_path = os.path.abspath('chromedriver')
        
        # move to home to access chromedriver
        #os.chdir('/Users/tnightengale')
        self.kjj = webdriver.Chrome(chrome_path)
        #os.chdir(self.current_dir)
    
        # go to kijiji
        self.next_url('https://www.kijiji.ca/')
        
        elements = self.kjj.find_elements_by_tag_name('a')
        text_list = [i.text for i in elements]
        self.next_click(elements[text_list.index('Sign In')])
        
        self.login()
    
    
    def post_ad(self):
        '''
        Post an ad once logged in.
        '''
        self.click_by_text(self.kjj.find_elements_by_tag_name,'a','Post ad')
        
        # randomly choose ad title and send keys
        title = self.kjj.find_element_by_id('AdTitleForm')
        self.current_ad_title = self.random_title()
        title.send_keys(self.current_ad_title)
        
        self.click_by_text(self.kjj.find_elements_by_tag_name,'button','Next')
        
        # click suggested category
        categories = self.kjj.find_elements_by_tag_name('button')
        self.next_click(categories[1])
        
        # choose and enter ad price
        price = self.kjj.find_element_by_id('PriceAmount')
        self.current_ad_price = self.schedule_choice()
        price.send_keys(self.current_ad_price)
        
        # enter description
        desc = self.kjj.find_element_by_tag_name('textarea')
        desc.send_keys(self.description)
        
        # upload images
        os.chdir('/Users/tnightengale/Desktop/Projects/kijiji_auto')
        
        image_list = os.listdir('images')
        
        upload = self.kjj.find_element_by_class_name('imageUploadButtonWrapper')
        upload = upload.find_element_by_tag_name('input')
        
        for pic in image_list:
            upload.send_keys(os.path.abspath('images')+'/'+pic)
        
        # wait for pics to load
        time.sleep(20)
        
        # click submit
        self.click_by_text(self.kjj.find_elements_by_tag_name,'button','Post Your Ad')
        
        print(
                'Ad posted successfully.',
                '\nCurrent title is {}.'.format(self.current_ad_title),
                '\nCurrent price is {}.'.format(self.current_ad_price)
                )
            
    
    def delete_ad(self):
        
        # go to ad page
        self.kjj.get('https://www.kijiji.ca/m-my-ads/active/1')
        
        # go into ad
        self.click_by_text(self.kjj.find_elements_by_tag_name,'a',self.current_ad_title)
        
        # check for replies
        reply_element = self.kjj.find_element_by_class_name('ad-replies')
        replies = int(reply_element.text)
        if replies > 0:
            print('\nYou have {} replies in your inbox. Ad not deleted.'.format(replies))
            print('Press "ctrl + c" to quit the program.')
            input('Press "Enter" to continue the loop and delete the ad: ')
        
        # click delete ad
        self.click_by_text(self.kjj.find_elements_by_tag_name,'a','Delete Ad')
        
        # click "not selling anymore"
        self.click_by_text(self.kjj.find_elements_by_tag_name,'li','Not selling it anymore')
        
        print('Ad deleted.')
        
    def login(self):
        user = self.kjj.find_element_by_id('LoginEmailOrNickname')
        user.send_keys(self.user)
        
        password = self.kjj.find_element_by_id('login-password')
        password.send_keys('j#2kjj999999E')
                           
        self.next_click(self.kjj.find_element_by_id('SignInButton'))
    
    def click_by_text(self, function, search, text):
        '''
        Take in a driver, find elements by
        tag, return element with matching text.
        '''
        elements = function(search)
        text_list = [i.text for i in elements]
        self.next_click(elements[text_list.index(text)])
    
    def close(self):
        self.kjj.close()
        print('Browser closed')

def d_str(date_time_object):
    '''
    Takes in a datetime object and outputs "yyyy/mm/dd hh:mm.ss".
    '''
    dt = date_time_object
    return dt.strftime('%Y/%m/%d %H:%M:%S')

def main():
    browser = kijiji()
    
    while True:
        
        time_stamp = d_str(datetime.datetime.now())
        print('The current time is {}.'.format(time_stamp))
        
        browser.access_kijiji()
        
        browser.post_ad()
        
        browser.close()
        
        # wait 24hrs
        wait_time = datetime.timedelta(days=1)
        
        sleep_time = datetime.datetime.now() + wait_time
        
        sleep_time_stamp = d_str(sleep_time)
        print('Sleeping loop till {}.'.format(sleep_time_stamp))
       
        while datetime.datetime.now() < sleep_time:
            time.sleep(1)
        
        # delete ad
        print('Deleting ad...')
        browser.access_kijiji()
        
        browser.delete_ad()
        
        browser.close()
        
        # sleep 60 seconds
        print('sleeping 60 seconds before reposting...')
        time.sleep(60)
        
        
    
if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
