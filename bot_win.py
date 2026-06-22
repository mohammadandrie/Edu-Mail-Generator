#!/usr/bin/env python3
"""
CCC Edu Mail Generator  - Windows Version
Run this on your Windows PC (home IP bypasses Incapsula)

Requirements:
    pip install -r requirements_win.txt

Usage:
    python bot_win.py
"""

import time
import re
import string
import random
import sys
import colorama
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from faker import Faker
from random import randint

# === Config ===
start_url = 'https://www.opencccapply.net/gateway/apply?cccMisCode='
clg_ids = ['941', '311', '361', '233', '851']
allColleges = ['MSJC College', 'Contra Costa College', 'City College (San Francisco)', 'Sacramento College', 'Mt San Antonio']
country_codes = ['855', '561', '800', '325', '330', '229']
fake = Faker('en_US')

fc = '\033[96m'; fm = '\033[95m'; fg = '\033[92m'; fy = '\033[93m'; fr = '\033[91m'; sb = '\033[1m'; sd = '\033[0m'
bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']
codes = vars(colorama.Fore)
colors_list = [codes[c] for c in codes if c not in bad_colors]

def postFix(n):
    return randint(10**(n-1), (10**n)-1)

def random_phone_num_generator():
    first = str(random.choice(country_codes))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return f'{first}-{second}-{last}'

def start_bot(apply_url, email, college, collegeID):
    data = {}
    ex = fake.name().split(' ')
    data['firstName'] = ex[0]
    data['LastName'] = ex[1]
    studentAddress = fake.address()
    data['randomMonth'] = random.randint(1, 12)
    data['randomDay'] = random.randint(1, 27)
    data['randomYear'] = random.randint(1996, 1999)

    firstName = data['firstName']
    LastName = data['LastName']
    randomMonth = data['randomMonth']
    randomDay = data['randomDay']
    randomYear = data['randomYear']
    studentPhone = random_phone_num_generator()
    middleName = random.choice(string.ascii_uppercase)

    ex_split = studentAddress.split("\n")
    streetAddress = ex_split[0]
    if re.compile(',').search(ex_split[1]) is not None:
        ex_split1 = ex_split[1].split(', ')
        cityAddress = ex_split1[0]
        ex_split2 = ex_split1[1].split(' ')
        stateAddress = ex_split2[0]
        postalCode = ex_split2[1]
    else:
        ex_split3 = ex_split[1].split(' ')
        cityAddress = ex_split3[0]
        stateAddress = ex_split3[1]
        postalCode = ex_split3[2]

    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Launching Chrome...')
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    
    driver = uc.Chrome(options=chrome_options, version_main=149)
    
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Navigating to CCCApply...')
    print(f'{fy}Waiting for Incapsula (5-30s)...')
    driver.get(apply_url)

    try:
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.ID, "inputFirstName"))
        )
        print(f'{fg}Form loaded!')
    except:
        print(f'{fr}Incapsula blocked. Page: {driver.current_url}')
        try:
            print(f'{fy}{driver.find_element(By.TAG_NAME, "body").text[:300]}')
        except:
            pass
        driver.close()
        return

    # STEP 1
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Account Progress - 1/3', end='')
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "inputFirstName"))).send_keys(firstName)
        time.sleep(0.5)
        driver.find_element(By.ID, "inputMiddleName").send_keys(middleName)
        time.sleep(0.5)
        driver.find_element(By.ID, "inputLastName").send_keys(LastName)
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="hasOtherNameNo"]').click()
        driver.find_element(By.XPATH, '//*[@id="hasPreferredNameNo"]').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateMonth option[value="{randomMonth}"]').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateDay option[value="{randomDay}"]').click()
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputBirthDateYear').send_keys(str(randomYear))
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateMonthConfirm option[value="{randomMonth}"]').click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateDayConfirm option[value="{randomDay}"]').click()
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputBirthDateYearConfirm').send_keys(str(randomYear))
        time.sleep(0.5)
        driver.find_element(By.ID, '-have-ssn-no').click()
        time.sleep(2)
        element = driver.find_element(By.ID, 'accountFormSubmit')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        element.click()
        print(f'{fg} (Success)')
    except Exception as e:
        print(f'{fr} Step 1 Error: {e}')
        driver.close()
        return

    # STEP 2
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}Account Progress - 2/3', end='')
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'inputEmail'))).send_keys(email)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputEmailConfirm').send_keys(email)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputSmsPhone').send_keys(studentPhone)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputStreetAddress1').send_keys(streetAddress)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputCity').send_keys(cityAddress)
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, f'#inputState option[value="{stateAddress}"]').click()
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputPostalCode').send_keys(postalCode)
        time.sleep(1)
        driver.find_element(By.ID, 'accountFormSubmit').click()
        time.sleep(3)

        try:
            driver.find_element(By.XPATH, '//*[@id="messageFooterLabel"]').click()
            time.sleep(1)
            while True:
                chkInputPhone = driver.find_element(By.ID, 'inputSmsPhone')
                chkError = chkInputPhone.get_attribute('class') or ''
                if 'error' in chkError:
                    print(f'{fr}\nInvalid Number, Retrying...')
                    studentPhone = random_phone_num_generator()
                    chkInputPhone.clear()
                    chkInputPhone.send_keys(studentPhone)
                    time.sleep(0.4)
                    driver.find_element(By.ID, 'inputAlternatePhone_auth_txt').click()
                    time.sleep(2)
                    try:
                        driver.find_element(By.XPATH, '//*[@id="messageFooterLabel"]').click()
                    except:
                        break
                else:
                    break
        except:
            pass

        time.sleep(2)
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="messageFooterLabel"]').click()
            time.sleep(1)
            driver.find_element(By.ID, 'inputAddressValidationOverride').click()
            time.sleep(1)
            driver.find_element(By.ID, 'accountFormSubmit').click()
        except:
            pass
        
        print(f'{fg} (Success)')
    except Exception as e:
        print(f'{fr} Step 2 Error: {e}')
        driver.close()
        return

    # STEP 3
    userName = firstName + str(postFix(7))
    pwd = LastName + str(postFix(5))
    pin = postFix(4)
    
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'inputUserId'))).send_keys(userName)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputPasswd').send_keys(pwd)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputPasswdConfirm').send_keys(pwd)
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputPin').send_keys(str(pin))
        time.sleep(0.5)
        driver.find_element(By.ID, 'inputPinConfirm').send_keys(str(pin))
        time.sleep(0.5)

        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion1 option[value="5"]').click()
        time.sleep(0.3)
        sec_ans1 = LastName + ''.join(random.choices(string.ascii_lowercase, k=4))
        driver.find_element(By.ID, 'inputSecurityAnswer1').send_keys(sec_ans1)
        time.sleep(0.3)

        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion2 option[value="6"]').click()
        time.sleep(0.3)
        driver.find_element(By.ID, 'inputSecurityAnswer2').send_keys(sec_ans1)
        time.sleep(0.3)

        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion3 option[value="7"]').click()
        time.sleep(0.3)
        driver.find_element(By.ID, 'inputSecurityAnswer3').send_keys(sec_ans1)

        print(f'{fr}\n[!] CAPTCHA needed! Solve it in the browser window')
        
        solved = 0
        for _ in range(150):
            try:
                xx = driver.find_element(By.NAME, 'captchaResponse')
                if xx.get_attribute('value') or '':
                    print(f'{fg}Captcha solved! Proceeding...')
                    solved = 1
                    break
                time.sleep(2)
            except:
                time.sleep(2)

        if solved:
            time.sleep(2)
            element = driver.find_element(By.ID, 'accountFormSubmit')
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            element.click()
            print(f'{fg}Account Progress - 3/3 (Success)')
            
            with open('myccAcc.txt', 'a') as fp:
                fp.write(f'Email - {email} Password - {pwd} UserName - {userName} First - {firstName} Last - {LastName} College - {college} Pin - {pin}\n\n')
            
            print(f'\n{fg}✅ ACCOUNT CREATED!')
            print(f'{fy}📧 CCC Username: {userName}')
            print(f'{fy}🔑 Password: {pwd}')
            print(f'{fy}🔢 PIN: {pin}')
            print(f'{fg}Saved to myccAcc.txt')
            
            input(f'{fy}\nPress Enter to close browser...')
            driver.close()
        else:
            print(f'{fr}Timeout waiting for captcha')
            driver.close()
    except Exception as e:
        print(f'{fr} Step 3 Error: {e}')
        driver.close()

def main():
    colorama.init()
    print(f'''{fc}{sd}
{'='*55}
  CCC Edu Mail Generator - Windows Edition  
{'='*55}
{fg}Note: Run this on your HOME PC (IP rumah lolos Incapsula)
{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Select a college:\n''')
    
    for idx, c in enumerate(allColleges):
        print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}{idx+1} - {random.choice(colors_list)}{c}')
    
    while True:
        try:
            inp = int(input(f'\n[{fc}{sd}*{fc}{sd}] College ID (1-5): '))
            if 1 <= inp <= len(allColleges):
                break
        except:
            pass
    
    idx = inp - 1
    apply_url = start_url + clg_ids[idx]
    print(f'{fg}Selected: {allColleges[idx]}')
    
    email = input(f'{fc}{sd}[{fc}{sd}*{fc}{sd}] Your email: ').strip()
    
    print(f'{fg}Launching browser...\n')
    start_bot(apply_url, email, allColleges[idx], idx + 1)

if __name__ == '__main__':
    main()
