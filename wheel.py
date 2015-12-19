#!/usr/bin/env python
'''Automate spinning of the Bounts reward wheel because
live is too short.'''

import os
import time
from selenium import webdriver

def load_reward_wheel():
    '''Log in and navigate to reward wheel.'''
    browser = webdriver.Chrome()

    browser.get('http://www.bounts.it')
    browser.find_element_by_link_text('My bounts').click()

    username = os.environ['BOUNTS_USR']
    browser.find_element_by_id('login_email') \
           .send_keys(username)

    password = os.environ['BOUNTS_PWD']
    browser.find_element_by_id('login_password') \
           .send_keys(password)

    browser.find_element_by_id('signin_button').click()
    browser.find_element_by_id('reward_wheel').click()
    
    return browser 

def spin_wheel(browser):
    '''Spin the wheel and subsequent messages to return to the 
    ready to spin state.'''
    browser.find_element_by_id('controls').click()

    message = browser.find_element_by_id('rew_title')
    # TODO: replace the hard coded spin waits by detection of
    # browser state.
    while not message.is_displayed():
        time.sleep(15)

    if message.text == 'Sorry!' or message.text == 'Nearly!':
        browser.find_element_by_id('spin_next').click()
    elif message.text == 'Feeling lucky?':
        print browser.find_element_by_id('prod_title').text
        browser.find_element_by_id('showshare').click()
        time.sleep(2)
        browser.find_element_by_link_text('Cancel').click()
        time.sleep(2)
        browser.find_element_by_id('spin_next').click()
    else:
        raise Exception()

def main():
    browser = load_reward_wheel()
    browser.switch_to.frame('rewardwheel_execute')
    time.sleep(5)
    while browser.find_element_by_id('credits').text != '0':
        spin_wheel(browser)

    browser.quit()

if __name__ == '__main__':
    main()
