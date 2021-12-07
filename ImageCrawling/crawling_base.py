import requests
import os


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
        print("Finished downloading images for keyword: ", name, " " , count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)")



if __name__ == "__main__":
    pass