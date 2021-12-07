from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import time
from enum import Enum


class ImageSource:

    src: str
    description: str
    search_tag: str

    def __init__(self, src, description, search_tag) -> None:
        if src == None:
            self.src = "None"
        else:
            self.src = src
        
        if description == None:
            self.description = "None"
        else:
            self.description = description
        
        if search_tag == None:
            self.search_tag = "None"
        else:
            self.search_tag = search_tag

    def print_info(self):
        print("Image for query: " + self.search_tag + "  description: " + self.description + " link: " + self.src)


class Website(Enum):
    """ Website enum to safely change Websites to crawl from without having to type urls

    Attributes:
    -----------
    GOOGLE: str
        Base-URL to crawl from Google-Images
    """
    GOOGLE = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990"
    FLICKR = "https://www.flickr.com/search/?text=horse"

class Response:

    query: str
    total_images: int
    data_images: int
    none_images: int
    image_count: int
    images = []
    website: str

    def __init__(self, query: str, images, image_count: int, website: Website) -> None:
        self.query = query
        self.images = images
        self.image_count = image_count
        self.website = website.name

    def print_info(self):
        print("Query: " + self.query + ", total: " + str(self.total_images) + ", usefull: " + str(self.image_count) + ", from: " + self.website)



def get_image_urls(query: str, website: Website, image_count: int, verbose: bool, scrolling: bool=True, headless: bool=True):
    scroll_to = 60000
    scroll_count = 5

    if verbose:
        print("Connecting to website: " + website.name)

    driver = connect_to_website(website, query, headless)
    if verbose:
        print("Scrolling down to load more images")

    if scrolling:
        _scroll_down(driver, scroll_to, scroll_count)
    if verbose:
        print("Donwloading links to all available Images")

    # res = _getContent(driver, 'img', 'src', 'alt', query, website, image_count)
    res = _getContent(driver, 'yui_3_16_0_1_1638483673356_7311', 'href', 'aria-label', query, website, image_count)
    for image in res.images:
        image.print_info()
    driver.quit()
    return res    




def connect_to_website(website: Website, query: str, headless: bool=True):
    options = Options()
    if headless:
        options.add_argument("--headless")

    current_pwd = os.getcwd()
    driver_path = current_pwd + "geckodriver.exe"
    driver = webdriver.Firefox(options=options)

    # open Website
    driver.get(website.value)

    time.sleep(1)

    if (website == Website.GOOGLE):
        # click cookies
        driver.find_element_by_id('L2AGLb').click()
        time.sleep(1)

    if (website == Website.FLICKR):
        time.sleep(5)
        print("clicking Cookies")
        driver.find_element_by_xpath("/html/body/div[8]/div[1]/div/div[6]/a[3]").click()

    # insert query
    # aktion = driver.find_element_by_name('text')
    # aktion.send_keys(query)
    # aktion.submit()


    time.sleep(2)
    return driver


def _scroll_down(driver, scroll_to, scroll_count):
    for i in range(0, scroll_count):
        driver.execute_script("window.scrollTo(0,"  + str(scroll_to) + ");")
        time.sleep(2)
    # click more images
    driver.find_element_by_class_name('mye4qd').click()
    time.sleep(3)
    # scroll down again
    for i in range(0, scroll_count):
        driver.execute_script("window.scrollTo(0,"  + str(scroll_to) + ");")
        time.sleep(2)
    ## END OF PAGE


def _getContent(driver, tag_name: str, link_tag: str, alt_tag: str, query: str, website: Website, image_count: int):
    if website == Website.GOOGLE:
        images = driver.find_elements_by_tag_name(tag_name)
    elif website == Website.FLICKR:
        images = driver.find_elements_by_id(tag_name)

    total = len(images)
    data = 0
    src_none = 0
    usefull_images = []
    print(len(images))
    for image in images:
        if image_count != 0 and len(usefull_images) >= image_count:
            break

        src = image.get_attribute(link_tag)
        alt = image.get_attribute(alt_tag)
        if src == None:
            src_none += 1
        elif src[0] == 'd':
            data += 1
        else:
            usefull_images.append(ImageSource(src, alt, query))

    res = Response(query, usefull_images, len(usefull_images), website)
    res.total_images = total
    res.data_images = data
    res.none_images = src_none
    return res



if __name__ == '__main__':
    get_image_urls("horse", Website.FLICKR, 0, True, scrolling=False, headless=False).print_info()