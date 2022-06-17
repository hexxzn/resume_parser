from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from docx import Document
import os.path
import pickle

from candidate import Candidate

# Extract candidate data from HTML.
def resume_extractor(url, manual_login):
    driver = webdriver.Firefox() # Create driver.
    indeed_login(driver, url, manual_login) # Log in to Indeed.
    source = driver.page_source # Get page source.
    driver.close() # Close driver.
    candidate = create_candidate(source) # Create candidate.
    parse_document_text(candidate) # Create resume from template.

    # with open('source.html', 'w') as sourcefile: # Save page source to file for debug.
    #     for line in source:
    #         sourcefile.write(line)

# Log in to Indeed.
def indeed_login(driver, url, manual_login):
    # Log in manually if manual login is true or if cookies.pkl doesn't exist.
    if not os.path.exists('resources\cookies.pkl') or manual_login:
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rdp-resume-container'))) # Wait for resume to fully load.
        if EC.presence_of_element_located((By.CSS_SELECTOR, '.rdp-resume-container')): # If resume loads then login was successful.
            pickle.dump(driver.get_cookies(), open('resources/cookies.pkl', 'wb')) # Save successful login cookies.
    # Log in with saved cookies.
    else:
        driver.get(url)
        cookies = pickle.load(open('resources/cookies.pkl', 'rb'))
        for cookie in cookies:
            if cookie['domain'] == '.indeed.com':
                driver.add_cookie(cookie) # Add cookies to skip login process.
        driver.get(url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rdp-resume-container'))) # Wait for resume to fully load.

# Create candidate instance.
def create_candidate(source):
    soup = BeautifulSoup(source, "html.parser")
    candidate = Candidate(
        soup.find('span', {'data-shield-id': 'firstname'}), # First name
        soup.find('span', {'data-shield-id': 'lastname'}), # Last name
        soup.find('span', {'data-shield-id': 'locality'}), # Location
        soup.find('div', {'data-shield-id': 'email'}), # Email address
        soup.find('div', {'data-shield-id': 'phone_number'}), # Phone number
        soup.find('div', {'data-shield-id': 'res_summary'}), # Summary
        soup.findAll('span', {'data-shield-id': 'skill-text'}), # Skills
        soup.findAll('div', {'data-shield-id': 'education_data_display'}), # Education
        soup.findAll('div', {'data-shield-id': 'workExperience_data_display'}) # Work experience
        )

    return candidate

# Iterate through text elements in document.
def parse_document_text(candidate, document='resumes/template.docx'):
    document = Document(document)

    # Replace text in paragraphs.
    for paragraph in document.paragraphs:
        replace_document_text(paragraph, candidate)

    # Replace text in tables.
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_document_text(paragraph, candidate)

    # Save resume as new word document.
    filename = candidate.first + candidate.last
    document.save('resumes/' + filename + '.docx')

# Find and replace text in word document.
def replace_document_text(element, candidate):
    # replacements[x] == [string to remove, string to insert]
    replacements = [
        ['CandidateFirst', candidate.first.upper()],
        ['CandidateLast', candidate.last.upper()],
        ['CandidatePhone', candidate.phone],
        ['CandidateEmail', candidate.email],
        ['CandidateLocation', candidate.location],
        ['CandidateSummary', candidate.summary],
        ['CandidateSkills', candidate.skills],
        ['CandidateEducation', candidate.education],
        ['CandidateExperience', candidate.experience],
        ]

    # Find text to replace
    inline = element.runs
    for i in range(len(inline)):
        for item in replacements:
            if item[0] in inline[i].text:
                item.append(i)

    # Replace text found
    for replacement in replacements:
        if len(replacement) == 3: # If target text was found, its location becomes the 3rd element in replacement list
            index = replacement[2] # Inline location of text to replace
            target_text = replacement[0] # Text to remove/replace
            replacement_text = replacement[1] # Text to add/insert
            inline[index].text = inline[index].text.replace(target_text, replacement_text)