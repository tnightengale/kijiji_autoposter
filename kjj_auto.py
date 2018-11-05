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
        self.selling_price = '600.00'
        self.description = open('description.txt','r').read()
    
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
        Returns a random titles for the created
        list of titles.
        '''
        return self.titles[random.randint(0,len(self.titles))]
        
        
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
        title.send_keys(self.random_title())
        
        self.click_by_text(self.kjj.find_elements_by_tag_name,'button','Next')
        
        # click suggested category
        categories = self.kjj.find_elements_by_tag_name('button')
        self.next_click(categories[1])
        
        # enter price
        price = self.kjj.find_element_by_id('PriceAmount')
        price.send_keys(self.selling_price)
        
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
        
        # click submit
        self.click_by_text(self.kjj.find_elements_by_tag_name,'button','Post Your Ad')
        
        print('Ad posted successfully.')
            
    
    def delete_ad(self):
        
        # go to ad page
        self.kjj.get('https://www.kijiji.ca/m-my-ads/active/1')
        
        # go into ad
        self.click_by_text(self.kjj.find_elements_by_tag_name,'a',self.ad_title)
        
        # check for replies
        reply_element = self.kjj.find_element_by_class_name('ad-replies')
        replies = int(reply_element.text)
        if replies > 0:
            print('\nYou have {} replies in your inbox. Ad not deleted.'.format(replies))
            return
        
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

def dt_to_str(date_time_object):
    '''
    Takes in a date time object and outputs
    two strings:
        
        "yyyy/mm/dd"
        "hh:mm.ss"
    '''
    dt = date_time_object
    a = '{}/{}/{}'.format(dt.year,dt.month,dt.day)
    b = '{}:{}.{}'.format(dt.hour,dt.minute,dt.second)
    return a, b

def main():
    while True:
        date_str, time_str = dt_to_str(datetime.datetime.now())
        
        print('The current time is {} on {}.'.format(time_str,date_str))
        
        browser = kijiji()
        
        browser.access_kijiji()
        
        browser.post_ad()
        
        browser.close()
        
        # wait 20hrs
        wait_time = (60*60*20)
        
        sleep_time = time.time() + wait_time
        date_str, time_str = dt_to_str(datetime.datetime.fromtimestamp(sleep_time))
        print('Sleeping loop till {} on {}.'.format(time_str,date_str))
        time.sleep(wait_time)
        
        # delete ad
        print('Deleting ad.')
        browser.access_kijiji()
        
        browser.delete_ad()
        
        browser.close()
        
        # sleep 10 minutes
        time.sleep(60*10)
    
if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
