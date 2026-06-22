#!/usr/bin/env python3
"""
Modified CCC Edu Mail Generator
- Skips broken Incapsula API bypass
- Uses undetected-chromedriver directly (browser-level anti-bot)
- Tries to navigate to CCCApply, let the browser handle Incapsula
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

bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']
codes = vars(colorama.Fore)
colors_list = [codes[color] for color in codes if color not in bad_colors]

fc = '\033[96m'
fm = '\033[95m'
fg = '\033[92m'
fy = '\033[93m'
fr = '\033[91m'
sb = '\033[1m'
sd = '\033[0m'

def postFix(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def random_phone_num_generator():
    first = str(random.choice(country_codes))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '{}-{}-{}'.format(first, second, last)

def generate_fake_data():
    """Generate fresh fake identity data"""
    ex = fake.name().split(' ')
    firstName = ex[0]
    LastName = ex[1]
    studentAddress = fake.address()
    randomMonth = random.randint(1, 12)
    randomDay = random.randint(1, 27)
    randomYear = random.randint(1996, 1999)
    return {
        'firstName': firstName,
        'LastName': LastName,
        'studentAddress': studentAddress,
        'randomMonth': randomMonth,
        'randomDay': randomDay,
        'randomYear': randomYear,
    }

def start_bot(apply_url, email, college, collegeID):
    """Main bot - uses undetected-chromedriver, no manual Incapsula bypass needed"""
    
    # Generate fake data
    data = generate_fake_data()
    firstName = data['firstName']
    LastName = data['LastName']
    studentAddress = data['studentAddress']
    randomMonth = data['randomMonth']
    randomDay = data['randomDay']
    randomYear = data['randomYear']

    studentPhone = random_phone_num_generator()
    
    # Parse address
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
    
    letters = string.ascii_uppercase
    middleName = random.choice(letters)

    print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Launching Chrome with chromedriver v149...')
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    chromedriver_path = '/home/ubuntu/Edu-Mail-Generator/webdriver/chromedriver-linux64/chromedriver'
    
    try:
        driver = uc.Chrome(
            driver_executable_path=chromedriver_path,
            options=chrome_options,
            headless=False,
            use_subprocess=True,
            version_main=149
        )
    except Exception as e:
        print(fr + 'Chrome launch failed: ' + str(e))

    print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Navigating to CCCApply...')
    driver.get(apply_url)
    
    print(fy + 'Waiting for Incapsula challenge to resolve...')
    print(fy + 'This may take 10-30 seconds. The browser handles it automatically.')
    
    # Wait for the page to load past Incapsula
    # Try to wait for the firstName input or any form element
    try:
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.ID, "inputFirstName"))
        )
        print(fg + 'Incapsula bypassed! Form loaded.')
    except:
        print(fr + 'Timeout waiting for form. Incapsula may have blocked us.')
        print(fy + 'Checking current page state...')
        print(fy + 'Current URL: ' + driver.current_url)
        try:
            body_text = driver.find_element(By.TAG_NAME, 'body').text[:500]
            print(fy + 'Page text: ' + body_text)
        except:
            pass
        driver.close()
        return

    # === STEP 1: Personal Info ===
    print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fy + 'Account Progress - 1/3', end='')
    
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "inputFirstName"))
        ).send_keys(firstName)
        time.sleep(0.7)
        
        driver.find_element(By.ID, "inputMiddleName").send_keys(middleName)
        time.sleep(0.7)
        
        driver.find_element(By.ID, "inputLastName").send_keys(LastName)
        time.sleep(0.7)
        
        driver.find_element(By.XPATH, '//*[@id="hasOtherNameNo"]').click()
        driver.find_element(By.XPATH, '//*[@id="hasPreferredNameNo"]').click()
        time.sleep(0.7)
        
        # Birth date
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateMonth option[value="{randomMonth}"]').click()
        time.sleep(0.7)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateDay option[value="{randomDay}"]').click()
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputBirthDateYear').send_keys(str(randomYear))
        time.sleep(0.7)
        
        # Confirm birth date
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateMonthConfirm option[value="{randomMonth}"]').click()
        time.sleep(0.7)
        driver.find_element(By.CSS_SELECTOR, f'#inputBirthDateDayConfirm option[value="{randomDay}"]').click()
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputBirthDateYearConfirm').send_keys(str(randomYear))
        time.sleep(0.7)
        
        # No SSN
        driver.find_element(By.ID, '-have-ssn-no').click()
        time.sleep(2)
        
        # Scroll to submit
        element = driver.find_element(By.ID, 'accountFormSubmit')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        element.click()
        
        print(fg + ' (Success)')
    except Exception as e:
        print(fr + f' Error at Step 1: {e}')
        driver.close()
        return

    # === STEP 2: Contact Info ===
    print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fy + 'Account Progress - 2/3', end='')
    
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'inputEmail'))
        ).send_keys(email)
        time.sleep(0.7)
        
        driver.find_element(By.ID, 'inputEmailConfirm').send_keys(email)
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputSmsPhone').send_keys(studentPhone)
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputStreetAddress1').send_keys(streetAddress)
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputCity').send_keys(cityAddress)
        time.sleep(0.7)
        driver.find_element(By.CSS_SELECTOR, f'#inputState option[value="{stateAddress}"]').click()
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputPostalCode').send_keys(postalCode)
        time.sleep(1)
        
        driver.find_element(By.ID, 'accountFormSubmit').click()
        time.sleep(3)
        
        # Handle validation errors
        try:
            driver.find_element(By.XPATH, '//*[@id="messageFooterLabel"]').click()
            time.sleep(1)
            
            # Check phone error
            while True:
                chkInputPhone = driver.find_element(By.ID, 'inputSmsPhone')
                chkError = chkInputPhone.get_attribute('class') or ''
                if 'error' in chkError:
                    print(fr + '\nInvalid Number, Retrying...')
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
        
        # Address validation
        try:
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="messageFooterLabel"]').click()
            time.sleep(1)
            driver.find_element(By.ID, 'inputAddressValidationOverride').click()
            time.sleep(1)
            driver.find_element(By.ID, 'accountFormSubmit').click()
        except:
            pass
        
        print(fg + ' (Success)')
    except Exception as e:
        print(fr + f' Error at Step 2: {e}')
        driver.close()
        return

    # === STEP 3: Account Setup ===
    userName = firstName + str(postFix(7))
    pwd = LastName + str(postFix(5))
    pin = postFix(4)
    
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, 'inputUserId'))
        ).send_keys(userName)
        time.sleep(0.7)
        
        driver.find_element(By.ID, 'inputPasswd').send_keys(pwd)
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputPasswdConfirm').send_keys(pwd)
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputPin').send_keys(str(pin))
        time.sleep(0.7)
        driver.find_element(By.ID, 'inputPinConfirm').send_keys(str(pin))
        time.sleep(0.7)
        
        # Security Questions
        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion1 option[value="5"]').click()
        time.sleep(0.5)
        sec_ans1 = LastName + ''.join(random.choices(string.ascii_lowercase, k=4))
        driver.find_element(By.ID, 'inputSecurityAnswer1').send_keys(sec_ans1)
        time.sleep(0.5)
        
        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion2 option[value="6"]').click()
        time.sleep(0.5)
        sec_ans2 = LastName + ''.join(random.choices(string.ascii_lowercase, k=4))
        driver.find_element(By.ID, 'inputSecurityAnswer2').send_keys(sec_ans2)
        time.sleep(0.5)
        
        driver.find_element(By.CSS_SELECTOR, '#inputSecurityQuestion3 option[value="7"]').click()
        time.sleep(0.5)
        sec_ans3 = LastName + ''.join(random.choices(string.ascii_lowercase, k=4))
        driver.find_element(By.ID, 'inputSecurityAnswer3').send_keys(sec_ans3)
        
        print(fr + '\n[!] Captcha needed - solve it in the browser window!')
        print(fy + '[*] Waiting for you to solve the captcha (polling every 2s)...')
        
        # Wait for captcha to be solved
        solved = 0
        for d in range(1, 200):
            try:
                xx = driver.find_element(By.NAME, 'captchaResponse')
                tdt = xx.get_attribute('value')
                if tdt and tdt.strip() != '':
                    print(fg + 'Captcha Solved! Proceeding...')
                    solved = 1
                    break
                else:
                    time.sleep(2)
            except:
                time.sleep(2)
        
        if solved == 1:
            time.sleep(2)
            element = driver.find_element(By.ID, 'accountFormSubmit')
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            element.click()
            
            print(fg + 'Account Progress - 3/3 (Success)')
            
            # Save to file
            fp = open('myccAcc.txt', 'a')
            birthDay = f'{randomMonth}/{randomDay}/{randomYear}'
            fp.write(f'Email - {email} Password - {pwd} UserName - {userName} First Name - {firstName} Middle Name - {middleName} Last Name - {LastName} College - {college} Pin - {pin} Birthday - {birthDay}\n\n')
            fp.close()
            
            print(fg + f'Account Created! Details saved in myccAcc.txt')
            print(fy + f'CCC Username: {userName}')
            print(fy + f'Password: {pwd}')
            print(fy + f'PIN: {pin}')
            
            # Continue with application form
            print(fy + '\nNow filling application form...')
            
            try:
                time.sleep(2)
                # Click continue/next after account creation
                try:
                    btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="registrationSuccess"]/main/div[2]/div/div/button'))
                    )
                    btn.click()
                except:
                    pass
                
                print(fg + 'Account creation completed! Application form should be loading...')
                input(fy + '\nPress Enter to close browser when done...')
                
            except Exception as e:
                print(fr + f'Application form error: {e}')
            
            driver.close()
        else:
            print(fr + 'Timeout waiting for captcha')
            driver.close()
            
    except Exception as e:
        print(fr + f' Error at Step 3: {e}')
        driver.close()

def main():
    # Initialize colorama
    colorama.init()
    
    print(fc + sd + '====== CCC Edu Mail Generator (Modified) ======')
    print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Select a college:\n')
    
    for index, college in enumerate(allColleges):
        color = random.choice(colors_list)
        print(fc + sd + '[' + fm + sb + '*' + fc + sd + '] ' + fy + str(index + 1) + ' - ' + color + college)
    
    # College selection
    while True:
        try:
            print(fc + sd + '\n[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Enter college id (1-5): ', end='')
            userInput = int(input())
            if 1 <= userInput <= len(allColleges):
                userInput = userInput - 1
                break
            else:
                print(fr + 'Wrong ID, try again')
        except:
            print(fr + 'Invalid input')
    
    selectedCollege = allColleges[userInput]
    collegeID = clg_ids[userInput]
    apply_url = start_url + collegeID
    
    print(fc + sd + '\n[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Selected: ' + fy + selectedCollege)
    print(fc + sd + '\n[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Apply URL: ' + fy + apply_url)
    
    # Email input
    print(fc + sd + '\n[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Enter your email (for contact): ', end='')
    userEmail = input().strip()
    
    print(fc + sd + '\n[' + fm + sb + '*' + fc + sd + '] ' + fg + 'Launching browser... (Incapsula will be handled automatically)')
    
    start_bot(apply_url, userEmail, selectedCollege, userInput + 1)

if __name__ == '__main__':
    main()
