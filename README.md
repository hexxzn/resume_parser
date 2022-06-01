![Interface Image](/resources/interface.png?raw=true) <br>

When given a valid resume URL the extractor will...

1. Navigate to resume url with selenium webdriver
2. Automatically log in by adding cookies from previous successful login
3. Extract resume candidate data with beautifulsoup
4. Insert candidate data into custom template.docx with python-docx
5. Save the modified template as a new MS Word document named after the candidate

Made for Indeed employers.