import re
import requests
from bs4 import BeautifulSoup
# using youtube_dl template to download mp4 from youtube
import youtube_dl

def find_search_content(search):
    # get the page , need to figure out how to assemble the urll
    request = requests.get("https://www.youtube.com/results?search_query={}".format(search))
    # call content
    content = request.content
    # python build-in UML parser : "html.parser" and transfer it to "soup" file
    soup = BeautifulSoup(content, "html.parser")
    return soup

def find_page_content(search):
    # get the page , need to figure out how to assemble the urll
    request = requests.get("https://www.youtube.com/results?{}".format(search))
    # call content
    content = request.content
    # python build-in UML parser : "html.parser" and transfer it to "soup" file
    soup = BeautifulSoup(content, "html.parser")
    return soup

def find_video(soup, all_item, i = 1):
    # find all html tag like<a .....rel = "spf-prefetch"> ,
    # which is start with <a and end with rel = "spf-prefetch"> ,
    # that is finding content in tag <a> and then the attributes that include rel = "spf-prefetch" ,
    # return a list of the results
    for element in soup.find_all('a', attrs={"rel": "spf-prefetch"}):
        # find attribute name same with 'title', using '' to indicate target attribute name
        video_title = element.get('title')
        video_link = element.get('href')

        # get the mid link string in i.ytimg.com/vi/{} where {} is, such as /watch?v=5jlI4uzZGjU
        # using split() to separate by "=", /watch?v = separated[0] and 5jlI4uzZGjU = separated[1]
        img_value = element.get('href').split("=")[1]

        # "alt" : True means only condition of the attribute named alt is True, that mean it's OK to crawl when the attribute alt has value
        # It also means the image can be alter, which is not necessary for us to type the concrete the size attributes in find_all function
        all_imgs = soup.find_all('img',{"alt": True, "width": True, "height": True, "onload": True, "data-ytimg": True})

        # Applying regular expression
        # re.findall(A, B) provide a find function to find all content same as format of A from source String B
        # regular expression rule \S to match any characters which is not null, use [ ] to apply the regular expression,
        # + means multiple non-null value, the return type is a LIST
        # str.strip(string) function is used to delete all characters in string,
        # this particular function, we delete the [ ] " ',, which is the string "[\"\']",
        # Because the " and ' have their default mean, we need to add \ to indicate it is a character in that string
        img = str(re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_value), str(all_imgs))).strip("[\"\']")

        # string.replace(string A, string B) is used to replace string A by string B to get the fixed img without the "&amp;"
        video_img = img.replace("&amp;", "&")

        # Be prepared to return the items map; using i as indexs which is beginning from 1 and the given value is using Jason Format in { } for future storage
        all_item['{}'.format(i)] = {"title":video_title, "link":"https://www.youtube.com{}".format(video_link),"img":video_img}
        # cause we only use elements in this for loop, so we add a increment of i to build whole the map
        i = i + 1
    return all_item

def video_time(soup, all_item, i = 1):
    for time in soup.find_all('span', {"class": "video-time"}):
        # map.get(key) is to get value from corresponding key
        # the follow [ ] means add new attribute named time and its value into each Jason in{ }
        # basically content in [ ] and the value given by the right side of the = are assembled to a new jason raw in the jason file value of a key
        # using time.text to remove html parts
        all_item.get('{}'.format(i))['time'] = time.text
        i = i + 1
    return all_item

def each_video(soup):
    # using a map to save and find items
    all_item = {}
    find_video(soup, all_item, i=1)
    video_time(soup,all_item, i=1)
    return  all_item

def page_bar(soup):
    # creat a map between page text(index) and page's link
    page = {}

    # using find_all to get the page link, the Jason format is like 'tag', {"attribute name" : "value"}
    # {"attribute name" : True} means no matter what values is, only take it when the attribute has a value
    # <a href="/results?sp=SBTqAwA%253D&amp;q=pitbull" ... what follows the tag name firstly is not an attribute !
    for page_value in soup.find_all('a', {"class": True, "data-sessionlink": True, "data-visibility-tracking": True,
                                          "aria-label": True}):
        # '' and "" only have difference between, map[key] = value
        page['{}'.format(page_value.text)] = page_value.get('href')
    # test the output of the pages map after finishing map building with print(page)
    return page

def dl_mp4(url):
    # The youtube_dl provide an option to change the default download location
    # Using 'outtmpl' : (project main path - this is not displayed) / new folder name /.../ %(title)s.%(ext)s
    # %(title)s means the video original title, .%(ext)s means the video's default format
    ydl_opts = {'format': 'best','outtmpl': '/video/%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def dl_mp3(url):
    # The youtube_dl provide an option to change the default download location
    # Using 'outtmpl' : (project main path - this is not displayed) / new folder name /.../ %(title)s.%(ext)s
    # %(title)s means the video original title, .%(ext)s means the video's default format
    # youtube_dl build-in option to covert mp4 to mp3 file, also use Jason format to set attributes
    # remember to add those (three) .exe files from transfer tool FFprobe software
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '/audio/%(title)s.%(ext)s', 'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])