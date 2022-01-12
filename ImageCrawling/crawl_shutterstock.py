from . import crawl_soup
# import crawl_soup

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
    if verbose:
        print("Finished crawling " + str(len(image_urls)) + "/" + str(image_count) + " images.")
    return image_urls


def _get_urls_from_page_number(base_string: str, page_number: int, verbose: bool=False):
    url = base_string + str(page_number)
    return crawl_soup.get_urls_specific(url, 0, 'img', 'jss231', 'src', verbose)


# Testing -> temp
import requests
import io
from PIL import Image
import sqlite3
import os
def __get_binary_image(url: str):
    binary = requests.get(url).content
    return binary


def __clean_db():
    conn = sqlite3.connect('test_database')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS images")
    cur.execute("CREATE TABLE images (id int, class text, database_name text, website text, data BLOB)")
    conn.commit()


def __safe_into_db(images):
    conn = sqlite3.connect('test_database')
    cur = conn.cursor()
    cur.execute("SELECT max(i.id) FROM images AS i")
    max_index = cur.fetchall()[0][0]
    index = 0
    if max_index != None:
        index = max_index
        index += 1
    
    print(index)

    img_tuples = []
    for image in images:
        data = __get_binary_image(image)
        img_tuples.append((index, 'horse', 'cifar_100', 'shutterstock', data))
        index += 1

    cur.executemany("INSERT INTO images(id, class, database_name, website, data) VALUES (?, ?, ?, ?, ?)", img_tuples)
    cur.execute("SELECT i.id, i.website FROM images AS i")
    print(cur.fetchall())
    conn.commit()
        

def __show_first():
    conn = sqlite3.connect('test_database')
    cur = conn.cursor()
    cur.execute("SELECT i.data FROM images AS i")
    image_data = cur.fetchall()[0][0]
    image = Image.open(io.BytesIO(image_data)).convert("RGBA")
    image.show()


if __name__ == '__main__':
    images = get_image_urls('horse', 250, verbose=True)
    images_data = []
    for im in images:
        images_data.append(__get_binary_image(im))
    import crawling_base
    crawling_base._change_folder("ImageDatabases", verbose=True)
    # crawling_base._save_images(images, 'porcupine', 250, verbose=True)
    import database_tools
    database_tools.load_images_to_db("test_database", "images", images_data, "horse", "cifar_10", "shutterstock.com")
