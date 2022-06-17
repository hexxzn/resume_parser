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
            index = 0
            for item in experience:
                experience_dict[index] = {'job_title': 'none', 'company_name': 'none', 'company_location': 'none', 'attendance_date': 'none', 'job_description': 'none'}
                job_title = item.find('h3', {'data-shield-id': 'workExperience_work_title'})
                experience_dict[index]['job_title'] = job_title.contents[0] if job_title else 'Job Title'
                company_name = item.find('span', {'data-shield-id': 'workExperience_work_experience_company'})
                experience_dict[index]['company_name'] = company_name.contents[0] if company_name else 'Company Name'
                company_location = item.find('span', {'data-shield-id': 'workExperience_location_span'})
                experience_dict[index]['company_location'] = company_location.contents[0] if company_location else 'Company Location'
                attendance_date = item.find('div', {'data-shield-id': 'workExperience_work_dates'})
                experience_dict[index]['attendance_date'] = attendance_date.contents[0] if attendance_date else 'Attendance Date'
                job_description = item.find('p', {'data-shield-id': 'workExperience_work_description'})
                if job_description:
                    experience_dict[index]['job_description'] = ''
                    for item in job_description.contents:
                        if isinstance(item, str):
                            experience_dict[index]['job_description'] += item
                        else:
                            experience_dict[index]['job_description'] += '\n'
                else:
                    experience_dict[index]['job_description'] = 'Job Description'
                index += 1
        else:
            experience_dict['Experience'] = 'None'

        self.experience = ''
        for key in experience_dict:
            key = int(key)
            self.experience += experience_dict[key]['job_title'] + '\n'
            self.experience += experience_dict[key]['company_name'] + '\n'
            self.experience += experience_dict[key]['company_location'] + '\n'
            self.experience += experience_dict[key]['attendance_date'] + '\n'
            self.experience += format_string(experience_dict[int(key)]['job_description']) + '\n\n'
        self.experience = self.experience[:-2]

# Remove excess white space and line breaks from string.
def format_string(string):
    string = re.sub('•', '', string)
    string = re.sub(' +', ' ', string)
    string = re.sub('\n ', '\n', string)
    if string[0] == ' ':
        string = string[1:]
    return string