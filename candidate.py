import re

class Candidate:
    def __init__(self, first, last, location, email, phone, summary, skills, education, experience):
        # Candidate identity
        self.first = first.contents[0] if first else 'First Name'
        self.last = last.contents[0] if last else 'Last Name'
        self.location = location.contents[0] if location else 'Location'
        self.email = email.contents[0] if email else 'Email Address'
        self.phone = phone.contents[0] if phone else 'Phone Number'
        self.summary = summary.contents[0] if summary else 'Summary'

        # Candidate skills
        self.skills = '' if skills else 'Skills'
        for skill in skills:
            self.skills += format_string(skill.contents[0]) + '\n'
        self.skills = self.skills[:-1]

        # Candidate education
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

        self.education = '' if education_dict else 'Education'
        for key in education_dict:
            self.education += format_string(key) + '\n'
            for value in education_dict[key]:
                self.education += format_string(value) + '\n'
            self.education += '\n'
        self.education = self.education[:-2]

        # Candidate experience
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
            self.experience += format_string(key) + '\n'
            for value in experience_dict[key]:
                self.experience += format_string(value) + '\n'
            self.experience += '\n'
        self.experience = self.experience[:-2]

# Remove excess white space and line breaks from string.
def format_string(string):
    string = re.sub(' +', ' ', string)
    string = re.sub('\n', '', string)
    return string