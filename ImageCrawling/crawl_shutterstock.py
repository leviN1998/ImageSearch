from os import link
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import math
import threading


base_url = "https://www.shutterstock.com/de/search/"
base_url_2 = "?image_type=photo&page="


def crawl_links(query: str, image_count: int, thread_count: int=5):
    print("[Info]      Keyword: " + query + " is crawling now")
    available_images = get_image_count(query)
    if  available_images < image_count:
        print("[Warning]   Only " + str(available_images) + " images available")
        print("[Critical]  Keyword: " + query + " will not be crawled")
        # handle case
        return []
    
    pages_to_crawl = math.ceil(image_count / 100)
    pages_per_thread = math.ceil(pages_to_crawl / thread_count)
    links = []
    threads = list()
    for i in range(0, thread_count):
        t = threading.Thread(target=__start_thread, args=(query, (i * pages_per_thread) + 1, ((i+1) * pages_per_thread) + 1, i, links, ))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    # remove None-links
    __remove_empty_links(links)

    # handle case that list isnt long enough
    current_page = pages_to_crawl +2
    while len(links) < image_count:
        pages_remaining = math.ceil((image_count - len(links)) / 100)
        __start_thread(query, current_page, current_page + pages_remaining, 0, links)
        current_page += pages_remaining + 1

        # remove None-links
        __remove_empty_links(links)

    links = links[0:image_count]
    return links


def __start_thread(query: str, page: int, to:int, thread_id: int, links):
    '''
    '''
    print("[Thread-" + str(thread_id) +"]  Started new Thread, crawling from: " + str(page) + " to: " + str(to))
    driver = _create_driver()
    array = []
    for i in range(page, to):
        array += __crawl_page(driver, query, i)
    driver.quit()
    for l in array:
        links.append(l)
    print("[Thread-" + str(thread_id) +"]  Thread finished")



def get_image_count(query: str, headless: bool=True):
    '''
    '''
    driver = _create_driver(headless)
    _connect(driver, base_url + query + base_url_2 + '1')
    text = driver.find_element_by_class_name('MuiTypography-colorTextSecondary')
    numbers = text.text.split()[0].split(".")
    driver.quit()
    number_str = ""
    for n in numbers:
        number_str += n
    return int(number_str)


def crawl_page(query: str, page: int, headless: bool=True):
    '''
    '''
    driver = _create_driver(headless)
    return __crawl_page(driver, query, page)




def __crawl_page(driver: webdriver, query: str, page: int):
    '''
    '''
    _connect(driver, base_url + query + base_url_2 + str(page))
    image_links = driver.find_elements_by_tag_name('img')
    links = []
    for l in image_links:
        link = l.get_attribute("src")
        links.append(link)
    return links




def _connect(driver: webdriver, url: str):
    '''
    '''
    driver.get(url)
    time.sleep(5)


def _create_driver(headless: bool=True):
    '''
    '''
    options = Options()
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)
    return driver


def __remove_empty_links(links):
    i = 0
    while i < len(links):
        if links[i] == None:
            links.pop(i)
            i = 0
        else:
            temp = links[i].split(".")
            if temp[-1] == "jpg":
                i += 1
            else:
                links.pop(i)
                i = 0