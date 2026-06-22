#!/usr/bin/env python3
"""
CCC Edu Mail Generator - Windows Edition v3
Dynamic Keycloak form detection for account.cccmypath.org
"""
import time, re, string, random, sys, colorama
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
allColleges = ['MSJC College', 'Contra Costa College', 'City College (SF)', 'Sacramento College', 'Mt San Antonio']
country_codes = ['855', '561', '800', '325', '330', '229']
fake = Faker('en_US')

fc = '\033[96m'; fm = '\033[95m'; fg = '\033[92m'; fy = '\033[93m'; fr = '\033[91m'; sb = '\033[1m'; sd = '\033[0m'
bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']
codes = vars(colorama.Fore); colors_list = [codes[c] for c in codes if c not in bad_colors]

def postFix(n): return randint(10**(n-1), (10**n)-1)

def random_phone():
    first = str(random.choice(country_codes))
    second = str(random.randint(1, 888)).zfill(3)
    last = str(random.randint(1, 9998)).zfill(4)
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = str(random.randint(1, 9998)).zfill(4)
    return f'{first}-{second}-{last}'

def wait_for_page_stable(driver, timeout=60):
    for i in range(timeout):
        try:
            text = driver.find_element(By.TAG_NAME, "body").text[:300]
            if 'Request unsuccessful' in text:
                print(f'{fy}Blocked... retry {i+1}/{timeout}')
                time.sleep(3)
                driver.refresh()
                time.sleep(5)
            elif 'Access denied' in text:
                print(f'{fy}Access denied... retry {i+1}/{timeout}')
                time.sleep(3)
                driver.refresh()
                time.sleep(5)
            else:
                time.sleep(2)
                return True
        except:
            time.sleep(2)
    return False

def get_field(driver, names, by=By.ID, timeout=5):
    """Try multiple field names, return first match or None"""
    el = None
    for name in names:
        try:
            if by == By.ID:
                el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, name)))
            elif by == By.NAME:
                el = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.NAME, name)))
            return el
        except:
            continue
    return None

def try_fill(driver, field_ids, value, by=By.ID):
    """Fill first matching field"""
    el = get_field(driver, field_ids, by)
    if el:
        el.clear()
        el.send_keys(str(value))
        return True
    return False

def try_click(driver, field_ids, by=By.ID):
    el = get_field(driver, field_ids, by)
    if el:
        el.click()
        return True
    return False

def try_select(driver, select_ids, value, by=By.ID):
    """Select option by value in first matching select"""
    el = get_field(driver, select_ids, by)
    if el:
        try:
            Select(el).select_by_value(str(value))
            return True
        except:
            pass
    return False

def dump_fields(driver):
    """Debug: dump all form fields"""
    print(f'\n{fy}=== Current URL: {driver.current_url} ===')
    for inp in driver.find_elements(By.TAG_NAME, "input"):
        n = inp.get_attribute("name") or "-"
        i = inp.get_attribute("id") or "-"
        t = inp.get_attribute("type") or "text"
        if t not in ('hidden',):
            print(f'{fy}  input: name={n:35s} id={i:35s} type={t}')
    for sel in driver.find_elements(By.TAG_NAME, "select"):
        n = sel.get_attribute("name") or "-"
        i = sel.get_attribute("id") or "-"
        print(f'{fy}  select: name={n:35s} id={i}')

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
    studentPhone = random_phone()
    middleName = random.choice(string.ascii_uppercase)

    ex_split = studentAddress.split("\n")
    streetAddress = ex_split[0]
    try:
        ex_split1 = ex_split[1].split(', ')
        cityAddress = ex_split1[0]
        ex_split2 = ex_split1[1].split(' ')
        stateAddress = ex_split2[0]
        postalCode = ex_split2[1]
    except:
        ex_split3 = ex_split[1].split(' ')
        cityAddress = ex_split3[0]
        stateAddress = ex_split3[1]
        postalCode = ex_split3[2]

    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Launching Chrome...')
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    driver = uc.Chrome(options=chrome_options, version_main=149)

    # === PHASE 1: Navigate to CCCApply gateway ===
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Phase 1: Navigate to CCCApply...')
    driver.get(apply_url)
    wait_for_page_stable(driver)
    print(f'{fg}Gateway loaded. URL: {driver.current_url}')

    # === PHASE 2: Click "Create Account" ===
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Phase 2: Looking for Create Account button...')
    
    # Try auto-clicking
    clicked = False
    create_texts = [
        "Create an OpenCCC account",
        "Create an Account",
        "Create Account",
        "Create New Account",
        "Sign Up",
    ]
    for txt in create_texts:
        try:
            btn = driver.find_element(By.XPATH, f"//*[contains(text(),'{txt}')]")
            btn.click()
            print(f'{fg}Clicked: {txt}')
            clicked = True
            time.sleep(5)
            break
        except:
            continue
    
    if not clicked:
        # Try by link href containing 'registration' or 'signup'
        try:
            for a in driver.find_elements(By.TAG_NAME, "a"):
                href = a.get_attribute("href") or ""
                if 'registration' in href or 'signup' in href or 'create' in href.lower():
                    a.click()
                    print(f'{fg}Clicked registration link: {href}')
                    clicked = True
                    time.sleep(5)
                    break
        except:
            pass

    if not clicked:
        print(f'{fy}Cannot find Create Account button automatically.')
        print(f'{fy}Please click "Create an OpenCCC account" in the browser...')
        input(f'{fy}Press Enter after clicking...')

    # === PHASE 3: Wait for Keycloak form ===
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Phase 3: Waiting for registration form...')
    for _ in range(30):
        cur_url = driver.current_url
        if 'cccmypath.org' in cur_url or 'keycloak' in cur_url.lower() or 'registration' in cur_url:
            print(f'{fg}On registration page: {cur_url[:80]}...')
            break
        if 'login-actions/registration' in cur_url:
            print(f'{fg}On registration page!')
            break
        time.sleep(2)

    dump_fields(driver)
    
    # === PHASE 4: Fill the registration form ===
    print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fg}Phase 4: Filling registration form...')
    
    # NAME FIELDS (try both old CCC IDs and Keycloak standard names)
    print(f'{fy}Filling name fields...')
    try_fill(driver, ['firstName', 'inputFirstName', 'given-name', 'givenName'], firstName)
    time.sleep(0.3)
    try_fill(driver, ['lastName', 'inputLastName', 'family-name', 'familyName'], LastName)
    time.sleep(0.3)
    try_fill(driver, ['middleName', 'inputMiddleName'], middleName)
    time.sleep(0.5)
    
    # BIRTH DATE
    print(f'{fy}Filling birth date...')
    try_select(driver, ['inputBirthDateMonth', 'birthMonth', 'birthdate_month', 'dateOfBirth_month'], randomMonth)
    time.sleep(0.3)
    try_select(driver, ['inputBirthDateDay', 'birthDay', 'birthdate_day', 'dateOfBirth_day'], randomDay)
    time.sleep(0.3)
    try_fill(driver, ['inputBirthDateYear', 'birthYear', 'birthdate_year', 'dateOfBirth_year'], str(randomYear))
    time.sleep(0.5)
    
    # EMAIL
    print(f'{fy}Filling email...')
    try_fill(driver, ['email', 'inputEmail', 'userEmail', 'username'], email)
    time.sleep(0.3)
    try_fill(driver, ['emailConfirm', 'inputEmailConfirm', 'email-confirm'], email)
    time.sleep(0.5)
    
    # PHONE
    print(f'{fy}Filling phone...')
    try_fill(driver, ['inputSmsPhone', 'phone', 'phoneNumber', 'mobile'], studentPhone)
    time.sleep(0.5)
    
    # ADDRESS
    print(f'{fy}Filling address...')
    try_fill(driver, ['inputStreetAddress1', 'streetAddress', 'address', 'street'], streetAddress)
    time.sleep(0.3)
    try_fill(driver, ['inputCity', 'city'], cityAddress)
    time.sleep(0.3)
    try_select(driver, ['inputState', 'state', 'region'], stateAddress)
    time.sleep(0.3)
    try_fill(driver, ['inputPostalCode', 'postalCode', 'zip', 'zipCode'], postalCode)
    time.sleep(0.5)

    # SSN / other radio buttons
    try_click(driver, ['-have-ssn-no', 'hasSSN_no', 'hasSsn_no', 'ssn_no'])
    time.sleep(0.5)

    print(f'{fy}Auto-fill done. Check the browser for remaining fields.')
    print(f'{fy}If there are more fields to fill, type them manually or describe them.')
    
    # Dump fields again to see what's left
    dump_fields(driver)
    
    input(f'\n{fy}=== Press Enter when ready to continue (or Ctrl+C to quit)... ===')
    
    # Try to find and click submit
    submit_btns = ['accountFormSubmit', 'submit', 'kc-register-form', 'register']
    for btn_id in submit_btns:
        try:
            btn = driver.find_element(By.ID, btn_id)
            btn.click()
            print(f'{fg}Clicked submit: {btn_id}')
            break
        except:
            try:
                btn = driver.find_element(By.NAME, btn_id)
                btn.click()
                print(f'{fg}Clicked submit: {btn_id}')
                break
            except:
                continue
    
    print(f'{fy}Waiting... check the browser for result.')
    input(f'{fy}Press Enter to close...')
    driver.quit()

def main():
    colorama.init()
    print(f'''{fc}{sd}
{'='*55}
  CCC Edu Mail Generator v3 - Keycloak Edition  
{'='*55}
{fg}Run on HOME PC (IP rumah lolos Incapsula)''')
    
    for idx, c in enumerate(allColleges):
        print(f'{fc}{sd}[{fm}{sb}*{fc}{sd}] {fy}{idx+1} - {random.choice(colors_list)}{c}')
    
    while True:
        try:
            inp = int(input(f'\n[{fc}{sd}*{fc}{sd}] College ID (1-5): '))
            if 1 <= inp <= len(allColleges): break
        except: pass
    
    idx = inp - 1
    apply_url = start_url + clg_ids[idx]
    print(f'{fg}Selected: {allColleges[idx]}')
    email = input(f'{fc}{sd}[{fc}{sd}*{fc}{sd}] Your email: ').strip()
    start_bot(apply_url, email, allColleges[idx], idx + 1)

if __name__ == '__main__':
    main()
