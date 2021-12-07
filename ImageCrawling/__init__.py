""" Module for crawling images from different Websites using
	a set of Keywords
	At the Moment only Google with BeautifulSoup is supported,
	which leads to ~80 Images per Keyword

Imports:
--------
    crawl_soup file with the BeautifulSoup-Image Crawler. Implements _get_image_urls to get urls of the images from google
    crawling_base provides functions for creating folders and saving images locally
    os is needed to get the current working directory's path

Functions:
----------
download_images(query, image_count, folder, verbose): str, int, str, bool -> None
	downloads images to a Keyword (query) into a specific folder (folder)
	path is relative to working directory

download_images_batch(): -> None
	optimized version of download_images to support using more than one Keyword

TODOS:
------
    TODO: implemet download_images_batch()
    TODO: add support for Selenium
    TODO: add Crawler for Google with Selenium
    TODO: add Crawler for Flickr with Selenium
    TODO: change Filestructure of Image-Databases
    TODO: add functionality to save images into Database (binary vs. path ??)
    TODO: add support for Feature Extraction
    TODO: add functionality of using 5 example images to measure how good results are

INFORMATION:
------------
	Every scraper needs to have a function _get_image_urls(query, image_count, verbose)
	That collects all image urls on that website

"""
from .crawl_soup import *
from .crawling_base import *
import os



def download_images(query: str, image_count: int = 0, folder: str = "", verbose: bool = True):
	""" downloads Images for a given Keyword into a given Folder

    Parameters:
    -----------
    query: str
    	Keyword String to enter into website for searching the images

    image_count: int, optional
    	Desired Number of images, defaults to 0 which means as many as the crawler can get

    folder: str, optional
    	Path to folder where images should be saved, defaults to "" which means current working directory
    	Paths are relative to current working directory

    verbose: bool, optional
    	Flag whether this function and functions that are called should output information to the console
    	defaults to True

    Returns:
    --------
    Nothing
    """
    old_pwd = os.getcwd()
    if not crawling_base._change_folder(folder, verbose):
        return

    urls = crawl_soup._get_image_urls(query, image_count, verbose)
    crawling_base._save_images(urls, query, image_count, verbose)
    os.chdir(old_pwd)

def download_images_batch():
	""" TODO: implement
	"""
    pass