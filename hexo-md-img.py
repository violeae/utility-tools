import re

def markdown_to_html_img(text):
    # Regex pattern: ![alt text](url)
    # Group 1 = alt text, Group 2 = image URL
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # HTML replacement with no-referrer policy
    replacement = r'<img src="\2" alt="\1" referrerpolicy="no-referrer">'
    
    return re.sub(pattern, replacement, text)
while(1):
    markdown_data = input()
    html_result = markdown_to_html_img(markdown_data)
    print(html_result)
