from itertools import count
from ImageCrawling import build_small
from ImageCrawling import feature_interface
from ImageCrawling import hashing_interface
from ImageCrawling import toolbox
import ImageCrawling

if __name__ == '__main__':
    # ImageCrawling.calculate_features("test.db", "mobile_net", feature_interface.mobileNet_func, hashing_interface.dummy_hashing_func, count=0)
    image = toolbox.get_test_image()[2]
    toolbox.binary_to_image(image).show()
    images = ImageCrawling.get_nearest_images("test.db", image, "cifar10", "mobile_net", feature_interface.mobileNet_func, count=10)

    for i in images:
        i[0].show()

