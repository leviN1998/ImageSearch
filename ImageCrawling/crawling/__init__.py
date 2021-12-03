from .crawl_soup import *
from .crawling_base import *
import os


"""
Every scraper needs to have a function _get_image_urls(query, image_count, verbose)
That collects all image urls on that website

"""
def download_images(query: str, image_count: int = 0, folder: str = "", verbose: bool = True):
    old_pwd = os.getcwd()
    if not crawling_base._change_folder(folder, verbose):
        return

    urls = crawl_soup._get_image_urls(query, image_count, verbose)
    crawling_base._save_images(urls, query, image_count, verbose)
    os.chdir(old_pwd)

def download_images_batch():
    pass