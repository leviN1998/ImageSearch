from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
from enum import Enum
import requests


def _save_images(urls, name: str, image_count: int, verbose: bool):
    """
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
        print("Finished downloading images for keyword: ", name, " " , count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)")

url = "https://www.flickr.com/search/?text=horse"

options = Options()
headless = False
if headless:
    options.add_argument("--headless")
current_pwd = os.getcwd()
driver_path = current_pwd + "geckodriver.exe"
driver = webdriver.Firefox(options=options)
# open Website
driver.get(url)
time.sleep(1)
print("Trying to click")


images = driver.find_elements_by_xpath("//a[@href]")
print(len(images))


image_links = []
for image in images:
    link = image.get_attribute("href")
    link_s = link.rsplit("/")
    if len(link_s) == 7:
        if link_s[3] == 'photos' and link_s[6] != '#comments':
            image_links.append(link)

#delete duplicates
image_links = list(dict.fromkeys(image_links))

driver.quit()

_save_images(image_links, "pferd", 0, True)
# <a class="overlay no-outline" href="/photos/parismadrid/5412377622/" tabindex="0" role="heading" aria-level="3" aria-label="horses von Danny VB" id="yui_3_16_0_1_1638480851150_7605"></a>
# <div class="view photo-list-photo-view awake" id="yui_3_16_0_1_1638480851150_1032" style="transform: translate(548px, 219px); width: 258px; height: 180px; background-image: url(&quot;//live.staticflickr.com/5173/5412377622_2f5cb4156d_n.jpg&quot;);"><div class="interaction-view" id="yui_3_16_0_1_1638480851150_1898"><div class="photo-list-photo-interaction" id="yui_3_16_0_1_1638480851150_7601">

		