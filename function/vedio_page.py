import requests
from bs4 import BeautifulSoup

# get the page
request = requests.get("https://www.youtube.com/results?search_query=pitbull")
# call content
content = request.content
# python build-in UML parser : "html.parser" and transfer it to "soup" file
soup = BeautifulSoup(content, "html.parser")
# creat a map between page text(index) and page's link
page = {}

# using find_all to get the page link, the Jason format is like 'tag', {"attribute name" : "value"}
# {"attribute name" : True} means no matter what values is, only take it when the attribute has a value
# <a href="/results?sp=SBTqAwA%253D&amp;q=pitbull" ... what follows the tag name firstly is not an attribute !
for page_value in soup.find_all('a', {"class":True, "data-sessionlink":True, "data-visibility-tracking":True, "aria-label":True}):
    # '' and "" only have difference between, map[key] = value
    page['{}'.format(page_value.text)] = page_value.get('href')
# test the output of the pages map after finishing map building
print(page)