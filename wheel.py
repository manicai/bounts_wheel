#!/usr/bin/env python
'''Automate spinning of the Bounts reward wheel because
live is too short.'''

import os
import time
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_until_clickable(browser, element_id, max_wait=60):
    wait = WebDriverWait(browser, max_wait)
    element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
    return element

def load_reward_wheel():
    '''Log in and navigate to reward wheel.'''
    browser = webdriver.Chrome()

    browser.get('http://www.bounts.it')
    browser.find_element_by_link_text('My bounts').click()

    wait_until_clickable(browser, 'signin_button')
    username = os.environ['BOUNTS_USR']
    browser.find_element_by_id('login_email') \
           .send_keys(username)

    password = os.environ['BOUNTS_PWD']
    browser.find_element_by_id('login_password') \
           .send_keys(password)

    browser.find_element_by_id('signin_button').click()

    wait_until_clickable(browser, 'reward_wheel')
    browser.find_element_by_id('reward_wheel').click()
    
    return browser 

def next_spin(browser):
    attempts =  0
    while attempts < 10:
        try:
            wait_until_clickable(browser, 'spin_next')
            browser.find_element_by_id('spin_next').click()
            return
        except selenium.common.exceptions.WebDriverException:
            attempts += 1
            time.sleep(5)

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
        next_spin(browser)
    elif message.text == 'Feeling lucky?':
        print browser.find_element_by_id('prod_title').text
        wait_until_clickable(browser, 'showshare')
        browser.find_element_by_id('showshare').click()
        time.sleep(2)
        browser.find_element_by_link_text('Cancel').click()
        time.sleep(2)
        next_spin(browser)
    else:
        raise Exception()

def main():
    browser = load_reward_wheel()
    browser.switch_to.frame('rewardwheel_execute')
    time.sleep(5)
    raw_input("Press any return to start spinning ...")
    while browser.find_element_by_id('credits').text != '0':
        spin_wheel(browser)

    browser.quit()

if __name__ == '__main__':
    main()
