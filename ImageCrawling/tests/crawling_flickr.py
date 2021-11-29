import requests
from bs4 import BeautifulSoup
import os


u_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }

image_count = 0
url = "https://www.flickr.com/search/?text=Pferd"

r = requests.get(url, headers=u_agent)
class_name = 'overlay'
soup = BeautifulSoup(r.content, 'html.parser')      
#print(soup)
                                       
results = soup.findAll('img')
# print(results)
for r in results:
    try:
        print(r['class'])
    except:
        pass


"""count = 0
imagelinks = []
for res in results:
    try:
        link = res['href']
        imagelinks.append(link)
        count = count + 1
        if (count >= image_count and image_count != 0):                                 # Stop adding images if we have enough (image_count = 0
            break                                                                       # means that we want to get as many images as possible)

    except KeyError:                                                                    # some images do not have a 'data-src' identifier... we skip those
        continue   

print(len(imagelinks))
print(imagelinks[0])"""
  

"""
count = 0
    for link in urls:
        with open(name + str(count) + '.jpg', 'wb') as f:
            image = requests.get(link)
            f.write(image.content)

        count = count + 1
        if verbose and count % 10 == 0:
            print("Saving files... ", count, "/", len(urls))

    if verbose:
        print("Finished downloading images! ", count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)") """