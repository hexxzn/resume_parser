<h2>Indeed Resume Extractor</h2>

![Interface Image](/resources/interface.png?raw=true) <br>

<h4>What it does...</h4>

1. Navigates to resume url with selenium webdriver
2. Automatically logs in by adding cookies from previous successful login
3. Extracts resume candidate data with beautifulsoup
4. Inserts candidate data into custom template.docx with python-docx
5. Saves the modified template as a new MS Word document named after the candidate

<h4>What it needs...</h4>

1. Some testing for more detailed/informative error handling.
2. A proper installer to set up geckodriver and firefox on user end if necessary.
