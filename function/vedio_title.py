import requests
from bs4 import BeautifulSoup

# get the page
request = requests.get("https://www.youtube.com/results?search_query=pitbull")
# call content
content = request.content
# python build-in UML parser : "html.parser" and transfer it to "soup" file
soup = BeautifulSoup(content, "html.parser")

# find all html tag like<a .....rel = "spf-prefetch"> ,
# which is start with <a and end with rel = "spf-prefetch"> ,
# that is finding content in tag <a> and then the attributes that include rel = "spf-prefetch" ,
# return a list of the results
for element in soup.find_all('a', attrs = {"rel": "spf-prefetch"}):
        # find attribute name same with 'title', using '' to indicate target attribute name
        vedio_title = element.get('title')
        print(vedio_title)