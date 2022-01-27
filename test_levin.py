from itertools import count
from ImageCrawling import build_small, database_tools
from ImageCrawling import feature_interface
from ImageCrawling import hashing_interface
from ImageCrawling import toolbox
from ImageCrawling import crawl_shutterstock
import ImageCrawling

if __name__ == '__main__':
    # ImageCrawling.calculate_features("test.db", "mobile_net", feature_interface.mobileNet_func, hashing_interface.dummy_hashing_func, count=0)
    image = toolbox.get_test_image()[2]
    toolbox.binary_to_image(image).show()
    images = ImageCrawling.get_nearest_images("test.db", image, "cifar10-like", "mobile_net", feature_interface.mobileNet_func, count=10)

    for i in images:
        i[0].show()
    # print(crawl_shutterstock.get_image_urls("horse", 200, True))
    # crawl_shutterstock.get_image_count("horse", headless=False)
    # print(crawl_shutterstock.get_image_count("horse", headless=True))
    # links = crawl_shutterstock.crawl_page("horse", 1, headless=True)
    # links = crawl_shutterstock.crawl_links("horse", 500, 5)
    # print(len(links))

    # conn = database_tools.connect("test.db")
    # database_tools.drop_db_from_images(conn, "cifar10-like")
    # database_tools.print_info_images(conn)
    # conn.close()

    # ImageCrawling.crawl_images("horse", "cifar10-like", 500, 0, 10)
