""" File for crawling images from different Pages using BeautifulSoup

TODOS:
------
    TODO: add Functions to documentation
    TODO: add Enums to Documentation
    TODO: add Support for flickr / ImageNet
    TODO: add Functions for saving into folders or returning arrays
    TODO: add Metric for usefullness of images

Imports:
--------
    requests: Standard Python Library for creating and using HTTP requests
    bs4: BeatifulSoup, Package which is used for html parsing
    os: Standard Python Library for interaction with the os (used for saving images and creating folders)
    enum: Standard Python Library for C-Style Enums

Classes:
--------
    

Functions:
----------
    
"""
import requests
from bs4 import BeautifulSoup
import os
from enum import Enum



class Website(Enum):
    """ Website enum to safely change Websites to crawl from without having to type urls

    Attributes:
    -----------
    GOOGLE: str
        Base-URL to crawl from Google-Images
    """
    GOOGLE = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"



# The User-Agent (needed because google won't show images if we don't have one)
u_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }



def download_images(query: str, image_count: int = 0, website: Website = Website.GOOGLE, folder: str = "", verbose: bool = True):
    """ download Images from a Website and save them to a specified folder

    Args:
    -----
        query: str
            Search-Query for the images (Keyword or more complex Query)
            depends on which website is used

        image_count: int, optional
            How many Images should be downloaded, defaults to 0 which means
            as many as the algorithm can get

        website: Website, optional
            Website from which the images should be downloaded
            Website-Enum from this file
            Defaults to GOOGLE

        folder: str, optional
            Path where downloaded images should be saved
            Defaults to current Directory

        verbose: bool, optional
            Sets if this skript should produce output to the commandline
            Defaults to True

    Returns:
    --------
        Nothing
    """
    if not _change_folder(folder, verbose):
        return

    urls = _get_image_urls(query, website, image_count, verbose)
    _save_images(urls, query, image_count, verbose)



def _change_folder(folder_name: str, verbose: bool) -> bool:
    """
    """
    folder_path = os.path.join(os.getcwd(), folder_name)
    if folder_name != "" and not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)
            if verbose:
                print("Created folder: ", folder_path)
        except:
            print("Error creating folder!")
            return False

    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        if verbose:
            print("Changing folder to: ", folder_path)

    else:
        print("Error changing Folder! Path is no directory!")
        return False

    return True


    
def _get_image_urls(query: str, website: Website, image_count: int, verbose: bool):
    """
    """
    url = website.value + "q=" + query + "&start=700"                                       # Final url with the categroy name for which we want
                                                                                            # to get images for
    r = requests.get(url, headers=u_agent)
    class_name = 'rg_i Q4LuWd'                                                              # Googles name for tags with actual images in it
    soup = BeautifulSoup(r.text, 'html.parser')                                             # Create and filter BeautifulSoup-Object of the website
    results = soup.findAll('img', {'class': class_name})                                    # Filter for all Tags that have images in it
    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count = count + 1
            if (count >= image_count and image_count != 0):                                 # Stop adding images if we have enough (image_count = 0
                break                                                                       # means that we want to get as many images as possible)

        except KeyError:                                                                    # some images do not have a 'data-src' identifier... we skip those
            continue   

    if verbose:
        print("Crawled ", count, " image urls!")   

    return imagelinks



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
        print("Finished downloading images! ", count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)")



if __name__ == "__main__":
    download_images("Pferd", folder="Pferd_Google")