import requests
from bs4 import BeautifulSoup

url = "https://mmf.bsu.by/en/about-faculty/"
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Remove script and style tags
for script in soup(["script", "style"]):
    script.extract()

# Extract the text content from the webpage
text_content = soup.get_text()

# Remove leading and trailing whitespace
text_content = text_content.strip()
text_content = "\n".join(
    line for line in text_content.split("\n") if line.strip())


# Save text content to a file
filename = "context.txt"
with open(filename, "w") as file:
    file.write(text_content)

print("Text content saved to", filename)
