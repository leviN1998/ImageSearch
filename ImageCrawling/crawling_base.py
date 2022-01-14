""" File to privide basic functionality needed to save images
    and handle folder operations

Imports:
--------
    requests needed to use http requests to download image referred by a url
    os needed for creating folders and saving images

Functions:
----------
_change_folder(folder_name, verbose): str, bool -> bool
    creates folder with given path and changes into it
    if folder already exists only changes into it
    Throws exeption if anything goes wrong

_save_images(urls, name, image_count, verbose): [str], str, int, bool -> Nothing
    saves a list of images as given name with an index added


TODOS:
------
    see __init__.py
"""
import requests
import os
from . import database_tools
# import database_tools


def _change_folder(folder_name: str, verbose: bool) -> bool:
    """ changes working directory to desired folder and creates this folder if needed
        returns False if folder was not created

    Parameters:
    -----------
    folder_name: str
        realtive path of folder to switch to

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    bool: Was this operation succesfull?
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


def _save_images(urls, name: str, image_count: int, verbose: bool):
    """ saves images referred by a list of urls into File-System

    Parameters:
    -----------
    urls: [str]
        List of Image-Urls to save

    name: str
        name which generated files should have

    image_count: int
        how many images should originally be crawled
        used for outputting information

    verbose: bool
        Flag whether this function and functions that are called should output information to the console

    Returns:
    --------
    Nothing
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
        print("Finished downloading images for keyword: ", name, " " , count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)")


def _save_images_to_db(urls, database: str, table_name: str, class_name: str, database_name: str, website_name: str,
                        image_count: int, test_img_count: int, verbose: bool=False):
    # change folder to default database folder
    _change_folder("ImageDatabases", verbose=True)
    # get content for urls
    images_data = []
    test_images_data = []
    for url in urls:
        if verbose and (len(images_data) + len(test_images_data)) % 100 == 0:
            print("Collected binary data " + str(len(images_data) + len(test_images_data)) + "/" + str(image_count))

        if len(images_data) + len(test_images_data) >= image_count:
            break
        if len(images_data) < (image_count - test_img_count):
            images_data.append(requests.get(url).content)
        else:
            test_images_data.append(requests.get(url).content)

    if verbose:
        print("Finished extracting binary data")

    database_tools.load_images_to_db(database, table_name, images_data, class_name, database_name, website_name)
    if verbose:
        print("finished loading normal images into database.")
    database_tools.load_images_to_db(database, table_name, test_images_data, class_name, database_name + "_test", website_name)
    if verbose:
        database_tools.print_info_images_connect(database, table_name)



if __name__ == "__main__":
    pass