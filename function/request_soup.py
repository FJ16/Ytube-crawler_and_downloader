import requests
from bs4 import BeautifulSoup

# get the page
request = requests.get("https://www.youtube.com/results?search_query=pitbull")
# call content
content = request.content
# python build-in UML parser : "html.parser" and transfer it to "soup" file
soup = BeautifulSoup(content, "html.parser")
print(soup)