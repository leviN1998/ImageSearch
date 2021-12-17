""" File with functions to crawl image-urls from Google or any other webiste 
    with img-Tags in its html

Imports:
--------
    requests needed to get the html of a website
    BeatufilSoup html parser to get img urls out of the html

Constants:
----------
    base_url: base url string to search for Images on Google
    u_agent: user agent, needed that Google does not block search query

Functions:
----------

get_image_urls(query, image_count, verbose): str, int, bool -> [str]
    crawls image-Urls from Google with a specific query or keyword

get_urls_specific(url, image_count, tag_name, class_name, content_name, verbose): str, int, str, str, str, bool -> [str]
    crawls image-Urls from any Website (needs to knwo which tag, class and content it should crawl)
    example: <img class="image" href="http://bla"> ==> tag_name = "img", class_name = "image", content_name = "href"

_get_urls_form_url(url, image_count, verbose): str, int, bool -> [str]
    helper function to crawl from Google. inserts class, tag and content name into _get_tags so that it works for Google

_get_tags(tag_name, class_name, content_name, website_content, image_count, verbose): str, str, str, str, int, bool -> [str]
    Function that extracts the image urls from a Website using information of the functions above
    should not be called from another file since get_urls_specific or _get_image_urls are better options


TODOS:
------
    see __init__.py
"""
import requests
from bs4 import BeautifulSoup


base_url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"


u_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }


def _get_urls_from_url(url: str, image_count: int, verbose: bool):
    """ Helper Function, inserts Values needed to crawl images from Google

    Parameters:
    -----------
    url: str
        url with query already inserted

    image_count: int
        how many images are crawled (0 means all)

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    [str]: list of urls which represent an image
    """
    r = requests.get(url, headers=u_agent)
    class_name = 'rg_i Q4LuWd'                                                              # Googles name for tags with actual images in it
    return _get_tags('img', class_name, 'data-src', r.text, image_count, verbose)


def get_urls_specific(url: str, image_count: int, tag_name: str, class_name: str, content_name: str, verbose: bool=False):
    """ Function to extract image-urls from any Website
        Needs to know how images are represented in the websites html
        Example: <img class="image" href="http://bla"> 
        ==> tag_name = "img", class_name = "image", content_name = "href"

    Parameters:
    -----------
    url: str
        url to the website which has the images in it

    image_count: int
        how many images are crawled (0 means all)

    tag_name: str
        how the tag containing the image is called in the html
        Examples: <img> -> "img", <a> -> "a"

    class_name: str
        how the class of the image tag is called 
        Examples <img class="Image"> -> "image", <img class="Test"> -> "Test"

    content_name: str
        name of the attribute that contains the link to the image
        Examples: <img href="http://bla"> -> "href", <img src="http://bla"> -> "src"

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    [str]: List of urls to images
    """
    r = requests.get(url, headers=u_agent)
    return _get_tags(tag_name, class_name, content_name, r.text, image_count, verbose)


def _get_tags(tag_name: str, class_name: str, content_name: str, website_content: str, image_count: int, verbose: bool):
    """ Function that does the real extraction work
        extarcts required attribute with BeautifulSoup
        Is only called by other functions in this File
        Do not call this from other files, since get_urls_specific would be the better option

    Parameters:
    -----------
    url: str
        url to the website which has the images in it

    tag_name: str
        how the tag containing the image is called in the html
        Examples: <img> -> "img", <a> -> "a"

    class_name: str
        how the class of the image tag is called 
        Examples <img class="Image"> -> "image", <img class="Test"> -> "Test"

    content_name: str
        name of the attribute that contains the link to the image
        Examples: <img href="http://bla"> -> "href", <img src="http://bla"> -> "src"

    website_content: str
        Raw html content of the webiste

    image_count: int
        how many images are crawled (0 means all)

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    [str]: List of urls to images
    """
    soup = BeautifulSoup(website_content, 'html.parser')
    if class_name == '':
        results = soup.findAll(tag_name)
    else:
        results = soup.findAll(tag_name, {'class': class_name})
    count = 0
    image_links = []
    for res in results:
        try:
            link = res[content_name]
            image_links.append(link)
            count = count + 1
            if (count >= image_count and image_count != 0):                                 # Stop adding images if we have enough (image_count = 0
                break                                                                       # means that we want to get as many images as possible)

        except KeyError:                                                                    # some images do not have a 'data-src' identifier... we skip those
            continue   

    if verbose:
        print("Crawled ", count, " image urls!")   

    return image_links



def get_image_urls(query: str, image_count: int, verbose: bool):
    """ Function called by __init__.py to get urls from a Keyword
        compines base_url and qurey to get the full url to a result page on Google
        Calls _get_urls_from_url to insert required information about the html construction of the website

    Parameters
    ----------
    query: str
        Keyword or query to find images for

    image_count: int
        how many images are crawled (0 means all)

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    [str]: List of urls to images
    """
    url = base_url + "q=" + query                                     # Final url with the categroy name for which we want
    return _get_urls_from_url(url, image_count, verbose)                                                                                            # to get images for
    