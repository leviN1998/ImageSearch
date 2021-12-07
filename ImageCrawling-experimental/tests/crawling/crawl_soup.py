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
    r = requests.get(url, headers=u_agent)
    class_name = 'rg_i Q4LuWd'                                                              # Googles name for tags with actual images in it
    return _get_tags('img', class_name, 'data-src', r.text, image_count, verbose)


def get_urls_specific(url: str, image_count: int, tag_name: str, class_name: str, content_name: str, verbose: bool=False):
    r = requests.get(url, headers=u_agent)
    return _get_tags(tag_name, class_name, content_name, r.text, image_count, verbose)


def _get_tags(tag_name: str, class_name: str, content_name: str, website_content: str, image_count: int, verbose: bool):
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



def _get_image_urls(query: str, image_count: int, verbose: bool):
    """
    """
    url = base_url + "q=" + query                                     # Final url with the categroy name for which we want
    return _get_urls_from_url(url, image_count, verbose)                                                                                            # to get images for
    