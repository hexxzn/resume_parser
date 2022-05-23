from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# class Candidate:
#     def __init__(self, first, last, location, email, phone, summary, skills, education, experience):
#         self.first = first.contents[0] if first else '<First Name>'
#         self.last = last.contents[0] if last else '<Last Name>'
#         self.location = location.contents[0] if location else '<Location>'
#         self.email = email.contents[0] if email else '<Email Address>'
#         self.phone = phone.contents[0] if phone else '<Phone Number>'
#         self.summary = summary.contents[0] if summary else '<Summary>'
#         self.skills = [skill for skill in skills if skills] if skills else ['<Skills>']

#         # self.education = [item for item in education if education] if education else ['<Education>']
#         # self.experience = [item for item in experience if experience] if experience else ['<Experience>']

# Extract HTML From Web Page
def extract(email, password, url):
    driver = webdriver.Firefox()
    driver.get(url)

    # Enter Email Address, Click Continue
    driver.find_element_by_id('ifl-InputFormField-3').send_keys(email)
    driver.find_element_by_class_name('css-157vc5a').click()

    time.sleep(2)
    # Check For Captcha
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

    time.sleep(2)
    # Click Log In With Password
    driver.find_element_by_id('auth-page-google-password-fallback').click()

    time.sleep(2)
    # Enter Password, Click Sign In
    driver.find_element_by_class_name('e1jgz0i3').send_keys(password)
    driver.find_element_by_class_name('css-157vc5a').click()

    time.sleep(2)
    # Check For Captcha
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

    time.sleep(2)
    while len(driver.find_element_by_id('verification_input').get_attribute('value')) < 6:
        time.sleep(1)
    driver.find_element_by_class_name('icl-Button').click()
    time.sleep(5)






    


    source = driver.page_source
    driver.close()

    # Extract Data From HTML
    soup = BeautifulSoup(source, "html.parser")

    # Extract First Name
    first_name = soup.find('span', {'data-shield-id': 'firstname'})
    first_name = first_name.contents[0] if first_name else 'first_name'

    # Extract Last Name
    last_name = soup.find('span', {'data-shield-id': 'lastname'})
    last_name = last_name.contents[0] if last_name else 'last_name'

    # Extract Location
    location = soup.find('span', {'data-shield-id': 'locality'})
    location = location.contents[0] if location else 'Location'

    # Extract Email Address
    email_address = soup.find('div', {'data-shield-id': 'email'})
    email_address = email_address.contents[0] if email_address else 'Email'

    #Extract Phone Number
    phone_number = soup.find('div', {'data-shield-id': 'phone_number'})
    phone_number = phone_number.contents[0] if phone_number else 'Phone'

    # Extract Summary
    summary = soup.find('div', {'data-shield-id': 'res_summary'})
    summary = summary.contents[0] if summary else 'Summary'

    # Extract Skills
    skills_list = []
    skills = soup.findAll('span', {'data-shield-id': 'skill-text'})
    if skills:
        for skill in skills:
            skills_list.append(skill.contents[0])
    else:
        skills_list.append('Skills')

    # Extract Education
    education_dict = {}
    education = soup.findAll('div', {'data-shield-id': 'education_data_display'})
    if education:
        for item in education:
            degree_title = item.find('h3', {'data-shield-id': 'education_edu_title'})
            degree_title = degree_title.contents[0] if degree_title else 'Degree Title'
            university_name = item.find('span', {'data-shield-id': 'education_edu_school_span'})
            university_name = university_name.contents[0] if university_name else 'University Name'
            university_location = item.find('span', {'data-shield-id': 'education_edu_location_span'})
            university_location = university_location.contents[0] if university_location else 'University Location'
            attendance_date = item.find('div', {'data-shield-id': 'education_edu_dates'})
            attendance_date = attendance_date.contents[0] if attendance_date else 'Attendance Date'
            education_dict[degree_title] = university_name, university_location, attendance_date
    else:
        education_dict['Education'] = 'None'

    # Extract Experience
    experience_dict = {}
    experience = soup.findAll('div', {'data-shield-id': 'workExperience_data_display'})
    if experience:
        for item in experience:
            job_title = item.find('h3', {'data-shield-id': 'workExperience_work_title'})
            job_title = job_title.contents[0] if job_title else 'Job Title'
            company_name = item.find('span', {'data-shield-id': 'workExperience_work_experience_company'})
            company_name = company_name.contents[0] if company_name else 'Company Name'
            company_location = item.find('span', {'data-shield-id': 'workExperience_location_span'})
            company_location = company_location.contents[0] if company_location else 'Company Location'
            attendance_date = item.find('div', {'data-shield-id': 'workExperience_work_dates'})
            attendance_date = attendance_date.contents[0] if attendance_date else 'Attendance Date'
            job_description = item.find('p', {'data-shield-id': 'workExperience_work_description'})
            job_description = job_description.contents[0] if job_description else 'Job Description'
            experience_dict[job_title] = company_name, company_location, attendance_date, job_description
    else:
        experience_dict['Experience'] = 'None'

    return first_name, last_name, phone_number, email_address, location, summary, skills_list, education_dict, experience_dict