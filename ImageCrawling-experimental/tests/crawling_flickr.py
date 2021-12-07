from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
from enum import Enum
import requests
import crawling


def _get_real_link(image_link: str):
    links = crawling.crawl_soup.get_urls_specific(image_links[0], 0, 'img', '', 'src', True)
    for l in links:
        if l[-5] != 'n':
            print("http:" + l)
            break

def _scroll_down(driver, scroll_to, scroll_count):
    for i in range(0, scroll_count):
        driver.execute_script("window.scrollTo(0,"  + str(scroll_to) + ");")
        time.sleep(3)
    # click more images
    # driver.find_element_by_id('yui_3_16_0_1_1638536119574_27178').click()
    buttons = driver.find_element_by_class_name('alt').click()
    time.sleep(3)
    # scroll down again
    for i in range(0, scroll_count):
        driver.execute_script("window.scrollTo(0,"  + str(scroll_to) + ");")
        time.sleep(2)
    ## END OF PAGE

# <button class="alt no-outline" id="yui_3_16_0_1_1638536119574_27178">Load more results</button>

url = "https://www.flickr.com/search/?text=horse"

options = Options()
headless = False
if headless:
    options.add_argument("--headless")
current_pwd = os.getcwd()
driver = webdriver.Firefox(options=options)
# open Website
driver.get(url)

time.sleep(3)
driver.switch_to.frame(1)
button = driver.find_element_by_class_name('acceptAll')
button.click()
time.sleep(2)
driver.switch_to.default_content()



scroll_to = 60000
scroll_count = 5
_scroll_down(driver, scroll_to, scroll_count)



images = driver.find_elements_by_xpath("//a[@href]")


image_links = []
for image in images:
    link = image.get_attribute("href")
    link_s = link.rsplit("/")
    if len(link_s) == 7:
        if link_s[3] == 'photos' and link_s[6] != '#comments':
            image_links.append(link)

#delete duplicates
image_links = list(dict.fromkeys(image_links))
print(len(image_links))
print(image_links[0])
print(image_links[1])

_get_real_link(image_links[0])

driver.quit()
		