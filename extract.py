from bs4 import BeautifulSoup
from selenium import webdriver

def extract(email, password, url):
    # Extract HTML From Web Page
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_id('ifl-InputFormField-3').send_keys(email)
    driver.find_element_by_class_name('css-157vc5a').click()
    driver.find_element_by_id('login-google-button').click()
    source = driver.page_source
    driver.close()

    # Extract Data From HTML
    with open('output.txt', 'w') as output, open('input.html', 'r', encoding='cp850')as source:
        soup = BeautifulSoup(source, "html.parser")

        # Extract First Name
        firstname = soup.find('span', {'data-shield-id': 'firstname'})
        firstname = firstname.contents[0] if firstname else 'FirstName'
        print(firstname)

        # Extract Last Name
        lastname = soup.find('span', {'data-shield-id': 'lastname'})
        lastname = lastname.contents[0] if lastname else 'LastName'

        # Extract Location
        location = soup.find('div', {'data-shield-id': 'headline_location'})
        location = location.contents[0] if location else 'Location'

        # Extract Email Address
        email_address = soup.find('div', {'data-shield-id': 'email_address'})
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

        return firstname, lastname, phone_number, email_address, location, summary, skills_list, education_dict, experience_dict