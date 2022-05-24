import time

# Log In To Indeed
def login(driver, email, password):
    # Enter Email Address, Click Continue
    driver.find_element_by_id('ifl-InputFormField-3').send_keys(email)
    driver.find_element_by_class_name('css-157vc5a').click()

    # Check For Captcha
    time.sleep(2)
    captcha(driver)

    time.sleep(2)
    # Click Log In With Password
    driver.find_element_by_id('auth-page-google-password-fallback').click()

    time.sleep(2)
    # Enter Password, Click Sign In
    driver.find_element_by_class_name('e1jgz0i3').send_keys(password)
    # driver.find_element_by_class_name('css-157vc5a').click()

    # Check For Captcha
    time.sleep(2)
    captcha(driver)

    # Wait For User To Enter PIN Number, Click Confirm
    time.sleep(2)
    while len(driver.find_element_by_id('verification_input').get_attribute('value')) < 6:
        time.sleep(1)
    driver.find_element_by_class_name('icl-Button').click()
    time.sleep(5)

# Check For Captcha And Wait For User To Complete Captcha Challenge
def captcha(driver):
        if driver.find_elements_by_tag_name('iframe'):
        # Find Captcha Element
            for element in driver.find_elements_by_tag_name('iframe'):
                if element.get_property('title'):
                    if element.get_property('title') == 'widget containing checkbox for hCaptcha security challenge':
                        driver.switch_to.frame(element)
                        captcha = driver.find_element_by_id('checkbox')
                        # Wait For User to Complete Captcha
                        while captcha.get_attribute('aria-checked') == 'false':
                            time.sleep(1)
                        break
            driver.switch_to.default_content()
            driver.find_element_by_class_name('css-157vc5a').click()