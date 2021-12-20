from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.firefox.webdriver import WebDriver
# from . import crawl_soup
import crawl_soup
# for debugging
import os
import codecs
# Funktioniert nicht headless
# Nur max 2500 Bilder


base_url = "https://www.flickr.com/search/?text="


def get_image_urls(query: str, image_count, verbose=False, headless=False):
    driver = _connect_to_website(query, headless)
    if verbose:
        print("Connected to website: ", base_url + query)
    
    raw_links = _scroll_and_extract(driver, image_count, verbose)
    # funktioniert nicht
    # raw_links = _scroll_before_extract(driver, image_count, verbose)
    driver.quit()
    if verbose:
        print("Finished crawling " + str(len(raw_links)) + " raw-links. Start extracting image-links!")

    return _get_real_links(raw_links, image_count, verbose)


def _connect_to_website(query: str, headless: bool=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
        #options.add_argument("--start-debugger-server")
        #options.add_argument("--remote-debugging-port=6000")
    driver = webdriver.Firefox(options=options)
    driver.set_window_position(0,0)
    driver.set_window_size(1920, 1080)
    driver.get(base_url + query)
    time.sleep(10)
    driver.save_screenshot("test1.jpg")
    # driver.switch_to.frame(1)
    # driver.switch_to.default_content()
    time.sleep(20)
    # driver.find_element_by_class_name('acceptAll').click()
    driver.save_screenshot("test2.jpg")
    complete_name = os.path.join(os.getcwd(), 'index.html')
    file_object = codecs.open(complete_name, "w", "utf-8")
    html = driver.page_source
    file_object.write(html)
    # driver.close()
    __click_cookies(driver)
    driver.save_screenshot("test2.jpg")
    __click_all_images(driver)
    driver.save_screenshot("test3.jpg")
    __click_better_view(driver)
    driver.save_screenshot("test4.jpg")
    time.sleep(3)
    return driver


def _scroll_and_extract(driver: WebDriver, image_count: int, verbose: bool=False):
    raw_links = []
    step = 1
    no_progress_count = 0       # number of scrolls without extracting new images
    max_no_progress_count = 10  # max. allowed number of scrolls without new images
    # for debugging scroll-ammounts:
    scrolls = 0
    number_useless_scrolls = 0
    while len(raw_links) < image_count:
        last_length = len(raw_links)
        __scroll_down(driver)
        __scrape_urls(driver, raw_links)
        # Delete duplicates
        raw_links = list(dict.fromkeys(raw_links))
        if verbose and len(raw_links) > step * 100:
            step = int(len(raw_links) / 100)
            print("Collected " + str(len(raw_links)) + "/" + str(image_count) + " raw-links")
            if scrolls != 0:
                print("Average number of useless scrolls per extraction: " + str(number_useless_scrolls/scrolls))
                scrolls = scrolls
        __click_view_more(driver)
        if len(raw_links) == last_length:
            no_progress_count += 1
            if no_progress_count >= max_no_progress_count:
                print("End of Page! cannot extract more images from this page!")
                break
        else:
            number_useless_scrolls += no_progress_count
            scrolls += 1
            no_progress_count = 0
    print("Average number of useless scrolls per extraction: " + str(number_useless_scrolls/scrolls))
    return raw_links


# Alternative: scroll and extract later
# Faster, but might lead to less results
def _scroll_before_extract(driver: WebDriver, image_count: int, verbose: bool=False):
    for i in range(0,50):
        __Scroll_to_end(driver)
        __click_view_more(driver)
    raw_links = []
    __scrape_urls(driver, raw_links)
    return raw_links



def _get_real_links(raw_links, image_count, verbose: bool=False):
    real_links = []
    for link in raw_links:
        links_inside = crawl_soup.get_urls_specific(link, 0, 'img', '', 'src', False)
        for l in links_inside:
            if l[-5] != 'n':
                real_links.append("http:" + l)
                break
        if verbose and len(real_links) % 10 == 0:
            print("extracted " + str(len(real_links)) + " links, " + str(len(raw_links)-len(real_links)) +
            " more available. Need " + str(image_count-len(real_links)))
    return real_links


def __scrape_urls(driver: WebDriver, raw_links):
    image_links = driver.find_elements_by_xpath("//a[@href]")
    for image in image_links:
        link = image.get_attribute("href")
        link_split = link.rsplit("/")
        if len(link_split) == 7:
            if link_split[3] == 'photos' and link_split[6] != '#comments':
                raw_links.append(link)


def __scroll_down(driver: WebDriver):
    scroll_count = 500
    driver.execute_script("window.scrollBy(0," + str(scroll_count) + ")")
    time.sleep(2)


def __Scroll_to_end(driver: WebDriver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)


def __click_view_more(driver: WebDriver):
    try:
        driver.find_element_by_class_name('alt').click()
        time.sleep(5)
    except Exception as e:
        pass
        print(e)


def __click_better_view(driver: WebDriver):
    clicked = False
    while not clicked:
        try:
            driver.find_element_by_class_name('thumbs').click()
            clicked = True
        except:
            print("Failed clicking view... try again!")
            time.sleep(2)
    time.sleep(2)



def __click_cookies(driver: WebDriver):
    clicked = False
    #driver.switch_to.frame(1)
    while not clicked:
        try:
            driver.find_element_by_class_name('acceptAll').click()
            time.sleep(2)
            clicked = True
        except Exception as e:
            print(e)
            print("Failed clicking cookies... try again!")
            time.sleep(2)
    driver.switch_to.default_content()
    time.sleep(2)


def __click_all_images(driver: WebDriver):
    clicked = False
    while not clicked:
        try:
            driver.find_element_by_class_name('view-more-link').click()
            time.sleep(2)
            clicked = True
        except:
            print("Failed clicking view-all-images... try again!")
            time.sleep(2)
        
    

if __name__ == '__main__':
    get_image_urls("horse", 6000, verbose=True, headless=True)