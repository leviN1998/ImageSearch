import requests
from bs4 import BeautifulSoup
import os


def download_images(category, image_count=0, folder="", verbose=True):
    folder_path = os.path.join(os.getcwd(), folder)
    if folder != "" and not os.path.exists(folder_path):
        try:
            os.mkdir(folder_path)
        except:
            print("Error creating folder!")

    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        if verbose:
            print("Changing folder to: ", folder_path)

    links = get_image_urls(category, image_count)
    if verbose:
        print("finished crawling ", len(links), " image-urls")

    count = 0
    for link in links:
        with open(category + str(count) + '.jpg', 'wb') as f:
            image = requests.get(link)
            f.write(image.content)

        count = count + 1
        if verbose and count % 10 == 0:
            print("Saving files... ", count, "/", len(links))

    if verbose:
        print("Finished downloading images! ", count, " Images downloaded, ", image_count, " images should be downloaded! ", "(0 means as many as possible)")


def get_image_urls(category, image_count=10): # count = 0 means all images

    # The User-Agent (needed because google won't show images if we don't have one)
    u_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }

    base_url = "https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&"   # Base Url to start a search query on google images
    url = base_url + "q=" + category                                                        # Final url with the categroy name for which we want
                                                                                            # to get images for
    r = requests.get(url, headers=u_agent)
    class_name = 'rg_i Q4LuWd'                                                              # Googles name for tags with actual images in it

    soup = BeautifulSoup(r.text, 'html.parser')                                             # Create and filter BeautifulSoup-Object of the website
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})                                 # Filter for all Tags that have images in it


    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count = count + 1
            if (count >= image_count and image_count != 0):                                 # Stop adding images if we have enough (image_count = 0
                break                                                                       # means that we want to get as many images as possible)

        except KeyError:
            continue                                                                        # some images do not have a 'data-src' identifier... we skip those

    return imagelinks

if __name__ == "__main__":
    download_images("Tübingen", image_count=0, folder="Test_Tübingen")