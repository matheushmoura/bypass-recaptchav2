from selenium import webdriver
from bypass import bypasscaptchaV2
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get('https://www.google.com/recaptcha/api2/demo?invisible=true')
bypasscaptchaV2(driver, "//button[@id='recaptcha-demo-submit']", "[title='o desafio reCAPTCHA expira em dois minutos']")
time.sleep(5)