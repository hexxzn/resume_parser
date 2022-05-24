from selenium import webdriver
from bs4 import BeautifulSoup
from docx import Document

from replace import replace
from login import login

class Candidate:
    def __init__(self, first, last, location, email, phone, summary, skills, education, experience):
        # Candidate Identity
        self.first = first.contents[0] if first else '<First Name>'
        self.last = last.contents[0] if last else '<Last Name>'
        self.location = location.contents[0] if location else '<Location>'
        self.email = email.contents[0] if email else '<Email Address>'
        self.phone = phone.contents[0] if phone else '<Phone Number>'
        self.summary = summary.contents[0] if summary else '<Summary>'
        
        # Candidate Skills
        self.skills = '' if skills else '<Skills>'
        for skill in skills:
            self.skills += format(skill.contents[0]) + '\n'

        # Candidate Education
        education_dict = {}
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

        self.education = '' if education_dict else '<Education>'
        for key in education_dict:
            self.education += format(key) + '\n'
            for value in education_dict[key]:
                self.education += format(value) + '\n'
            self.education += '\n'

        # Candidate Experience
        experience_dict = {}
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

        self.experience = ''
        for key in experience_dict:
            self.experience += format(key) + '\n'
            for value in experience_dict[key]:
                self.experience += format(value) + '\n'
            self.experience += '\n'

# Extract HTML From URL With Indeed Account Credentials
def extract(email, password, url):
    driver = webdriver.Firefox()
    driver.get(url)
    login(driver, email, password)
    source = driver.page_source
    driver.close()

    soup = BeautifulSoup(source, "html.parser")

    candidate = Candidate(
        soup.find('span', {'data-shield-id': 'firstname'}),
        soup.find('span', {'data-shield-id': 'lastname'}),
        soup.find('span', {'data-shield-id': 'locality'}),
        soup.find('div', {'data-shield-id': 'email'}),
        soup.find('div', {'data-shield-id': 'phone_number'}),
        soup.find('div', {'data-shield-id': 'res_summary'}),
        soup.findAll('span', {'data-shield-id': 'skill-text'}),
        soup.findAll('div', {'data-shield-id': 'education_data_display'}),
        soup.findAll('div', {'data-shield-id': 'workExperience_data_display'})
        )

    return candidate

# Insert Data Into Word Document
def insert(email, password, url, document_name='template.docx', ):
    document = Document(document_name)
    candidate = extract(email, password, url)

    # Replace Text In Paragraphs
    for paragraph in document.paragraphs:
        replace(paragraph, 'FirstName', candidate.first.upper())
        replace(paragraph, 'LastName', candidate.last.upper())

    # Replace Text In Tables
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace(paragraph, 'PhoneNumber', candidate.phone)
                    replace(paragraph, 'EmailAddress', candidate.email)
                    replace(paragraph, 'Location', candidate.location)
                    replace(paragraph, 'Summary', candidate.summary)
                    replace(paragraph, 'SkillsList', candidate.skills)
                    replace(paragraph, 'EducationList', candidate.education)
                    replace(paragraph, 'ExperienceList', candidate.experience)

    document.save('resume.docx')