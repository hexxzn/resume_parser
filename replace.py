import re

# For element In Document, Replace target_text with replacement_text
def replace(element, target_text, replacement_text):
        inline = element.runs
        for i in range(len(inline)):
            if target_text in inline[i].text:
                text = inline[i].text.replace(target_text, replacement_text)
                inline[i].text = text

# Remove White Space And Line Breaks
def format(string):
    string = re.sub(' +', ' ', string)
    string = re.sub('\n', '', string)
    return string