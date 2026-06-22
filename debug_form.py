#!/usr/bin/env python3
"""Debug script - dump Keycloak CCC registration form fields
Usage: python debug_form.py
Opens browser, navigates to OpenCCC gateway, you click "Create Account",
then it dumps all form fields with their names/IDs."""
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

print("Launching Chrome...")
driver = uc.Chrome(options=uc.ChromeOptions(), version_main=149)

print("Navigating to CCCApply...")
driver.get("https://www.opencccapply.net/gateway/apply?cccMisCode=311")

print("\n=== PLEASE CLICK 'Create an OpenCCC account' in the browser ===")
print("Then press Enter here when you see the registration form...")
input()

print(f"\nCurrent URL: {driver.current_url}")
print(f"Page title: {driver.title}")

print("\n=== INPUT FIELDS ===")
for inp in driver.find_elements(By.TAG_NAME, "input"):
    name = inp.get_attribute("name") or "-"
    id_ = inp.get_attribute("id") or "-"
    type_ = inp.get_attribute("type") or "text"
    placeholder = inp.get_attribute("placeholder") or "-"
    label = inp.get_attribute("aria-label") or placeholder
    print(f"  name={name:30s} id={id_:30s} type={type_:12s} label={label}")

print("\n=== SELECT FIELDS ===")
for sel in driver.find_elements(By.TAG_NAME, "select"):
    name = sel.get_attribute("name") or "-"
    id_ = sel.get_attribute("id") or "-"
    print(f"  name={name:30s} id={id_}")
    for opt in sel.find_elements(By.TAG_NAME, "option"):
        val = opt.get_attribute("value") or "-"
        txt = opt.text[:40]
        print(f"    option: value={val:20s} text={txt}")

print("\n=== BUTTONS ===")
for btn in driver.find_elements(By.TAG_NAME, "button"):
    text = btn.text.strip()
    id_ = btn.get_attribute("id") or "-"
    name = btn.get_attribute("name") or "-"
    if text:
        print(f"  name={name:25s} id={id_:25s} text={text}")

print("\n=== H1/H2 HEADINGS ===")
for h in driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3"):
    print(f"  {h.tag_name}: {h.text}")

print("\nDone! Copy this output.")
input("Press Enter to close browser...")
driver.quit()
