from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# Log In To Indeed
def login(driver, email, password):
    # Enter Email Address, Click Continue
    wait(driver, '#ifl-InputFormField-3')
    driver.find_element_by_css_selector('#ifl-InputFormField-3').send_keys(email)
    driver.find_element_by_css_selector('.css-157vc5a').click()

    # Check For Captcha
    captcha(driver)

    # Enter Email Address Again If Necessary, Click Continue
    if driver.find_element_by_css_selector('#ifl-InputFormField-3').get_attribute('value') == '':
        driver.find_element_by_css_selector('#ifl-InputFormField-3').send_keys(email)
    driver.find_element_by_css_selector('.css-157vc5a').click()

    # Click Log In With Password
    wait(driver, '#auth-page-google-password-fallback')
    driver.find_element_by_css_selector('#auth-page-google-password-fallback').click()

    # Enter Password, Click Sign In
    wait(driver, '.e1jgz0i3')
    driver.find_element_by_css_selector('.e1jgz0i3').send_keys(password)
    driver.find_element_by_css_selector('.css-157vc5a').click()

    # Check For Captcha
    captcha(driver)

    # Enter Password Again If Necessary, Click Continue
    if driver.find_element_by_css_selector('.e1jgz0i3').get_attribute('value') == '':
        driver.find_element_by_css_selector('.e1jgz0i3').send_keys(email)
    driver.find_element_by_css_selector('.css-157vc5a').click()

    # Wait For User To Enter PIN Number, Click Confirm
    wait(driver, '#verification_input')
    while len(driver.find_element_by_css_selector('#verification_input').get_attribute('value')) < 6:
        time.sleep(1)
    driver.find_element_by_css_selector('.icl-Button').click()

    # Wait For Resume To Load
    wait(driver, '.rdp-resume-container')

# Check For Captcha And Wait For User To Complete Captcha Challenge
def captcha(driver):
        time.sleep(2)
        if driver.find_elements_by_tag_name('iframe'):
        # Find Captcha Element
            for element in driver.find_elements_by_tag_name('iframe'):
                if element.get_property('title'):
                    if element.get_property('title') == 'widget containing checkbox for hCaptcha security challenge':
                        driver.switch_to.frame(element)
                        captcha = driver.find_element_by_css_selector('#checkbox')
                        # Wait For User to Complete Captcha
                        while captcha.get_attribute('aria-checked') == 'false':
                            time.sleep(2)
                        break
            driver.switch_to.default_content()

def wait(driver, element_class):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_class)))