# from . import crawl_soup
import crawl_soup

base_url = "https://www.shutterstock.com/de/search/"
base_url_2 = "?image_type=photo&page="

def get_image_urls(query: str, image_count: int, verbose: bool=False):
    # could crash if image_count is greater than available images
    image_urls = []
    page_number = 1
    url = base_url + query + base_url_2
    while len(image_urls) < image_count:
        image_urls += _get_urls_from_page_number(url, page_number, verbose=False)
        page_number += 1
        # print(len(image_urls))
    return image_urls


def _get_urls_from_page_number(base_string: str, page_number: int, verbose: bool=False):
    url = base_string + str(page_number)
    return crawl_soup.get_urls_specific(url, 0, 'img', 'jss231', 'src', verbose)


# Testing -> temp
import requests
import io
from PIL import Image
def __get_binary_image(url: str):
    binary = requests.get(url).content
    return binary


if __name__ == '__main__':
    images = get_image_urls('porcupine', 250, verbose=True)
    # import crawling_base
    # crawling_base._change_folder("test", verbose=True)
    # crawling_base._save_images(images, 'porcupine', 250, verbose=True)
    image_data = __get_binary_image(images[1])
    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
    image.show()
