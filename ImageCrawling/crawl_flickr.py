from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.firefox.webdriver import WebDriver
from . import crawl_soup


base_url = "https://www.flickr.com/search/?text="


def _get_real_links(image_links, image_count: int, verbose=False):
    real_links = []
    for link in image_links:
        links_inside = crawl_soup.get_urls_specific(link, 0, 'img', '', 'src', False)
        for l in links_inside:
            if l[-5] != 'n':
                real_links.append("http:" + l)
                break
        if len(real_links) >= image_count and image_count != 0:
            return real_links
        if verbose and len(real_links) % 10 == 0:
            print("Extracted ", len(real_links), "links. ", image_count-len(real_links), " more to process, ",
            len(image_links)-len(real_links), " available!")
    return real_links
    
    
def _scroll_down(driver, scroll_to, scroll_count, verbose=False):
    for i in range(0, scroll_count):
        driver.execute_script("window.scrollTo(0,"  + str(scroll_to) + ");")
        time.sleep(5)
        if i % 5 == 0:
            if verbose:
                print("Scrolling ", i, "/", scroll_count)
            try:
                button = driver.find_element_by_class_name('alt')
                button.click()
                time.sleep(5)
            except:
                # No button to click
                pass
            if i % 10 == 0 and i >= 10:
                scroll_to += 40000


def _click_cookies(driver: WebDriver):
    driver.switch_to.frame(1)
    button = driver.find_element_by_class_name('acceptAll')
    button.click()
    time.sleep(2)
    driver.switch_to.default_content()
    time.sleep(2)


def _click_all_images(driver: WebDriver):
    button = driver.find_element_by_class_name('view-more-link')
    button.click()
    time.sleep(2)


def get_image_urls(query: str, image_count, verbose):
    driver = _connect_to_website(query, headless=False)
    if verbose:
        print("Connected to website: ", base_url + query)

    _prepare_website(driver, image_count)
    if verbose:
        print("Finished preparing Website, starting extraction now!")
    links = _scrape_urls(driver, image_count,verbose=True)
    if verbose:
        print("Scraped: ", len(links), " image-links")
    return links
    


def _scrape_urls(driver: WebDriver, image_count: int, verbose=False):
    images = driver.find_elements_by_xpath("//a[@href]")
    # TODO: A new Thread can be started here!!
    # TODO: when processing many queries the driver can be reused
    image_links = []
    for image in images:
        link = image.get_attribute("href")
        link_s = link.rsplit("/")
        if len(link_s) == 7:
            if link_s[3] == 'photos' and link_s[6] != '#comments':
                image_links.append(link)
    # delete duplicates
    driver.quit()
    image_links = list(dict.fromkeys(image_links))
    return _get_real_links(image_links, image_count, verbose=True)

    


def _connect_to_website(query: str, headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(base_url + query)
    time.sleep(5)
    _click_cookies(driver)
    _click_all_images(driver)
    return driver


def _prepare_website(driver: WebDriver, image_count: int):
    # Click view all
    # Maybe decide how much scrolling needs to be done
    # scroll_count 5 was < 400 links
    scroll_to = 60000
    scroll_count = 5
    _scroll_down(driver, scroll_to, scroll_count, verbose=True)
    if image_count == 0:
        image_count = 10000
    
    # TODO: irgendwann sind nicht mehr alle Bilder geladen! 
    scroll_count = int (image_count / 100)
    _scroll_down(driver, scroll_to, scroll_count, verbose=True)


if __name__ == '__main__':
    get_image_urls("horse", 200, verbose=True)