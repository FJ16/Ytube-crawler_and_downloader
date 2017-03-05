# re package is for using of regular expression extraction
import re

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
#find or find_all('tag', {attributes}), which is Jason format
# return a list of the results
# This for loop basically iterate two soup.find_all Lists
for element in soup.find_all('a', {"rel": "spf-prefetch"}):
    # get the mid link string in i.ytimg.com/vi/{} where {} is, such as /watch?v=5jlI4uzZGjU
    # using split() to separate by "=", /watch?v = separated[0] and 5jlI4uzZGjU = separated[1]
    img_value = element.get('href').split("=")[1]
    # "alt" : True means only condition of the attribute named alt is True, that mean it's OK to crawl when the attribute alt has value
    # It also means the image can be alter, which is not necessary for us to type the concrete the size attributes in find_all function
    all_imgs = soup.find_all('img',{"alt":True,"width":True,"height":True,"onload":True,"data-ytimg":True})
    # Applying regular expression
    # re.findall(A, B) provide a find function to find all content same as format of A from source String B
    # regular expression rule \S to match any characters which is not null, use [ ] to apply the regular expression,
    # + means multiple non-null value, the return type is a LIST
    # str.strip(string) function is used to delete all characters in string,
    # this particular function, we delete the [ ] " ',, which is the string "[\"\']",
    # Because the " and ' have their default mean, we need to add \ to indicate it is a character in that string
    img = str(re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_value),str(all_imgs))).strip("[\"\']")
    # string.replace(string A, string B) is used to replace string A by string B to get the fixed img without the "&amp;"
    vedio_img = img.replace("&amp;","&")
    print(vedio_img)
