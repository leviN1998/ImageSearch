import time
import ImageCrawling
from ImageCrawling import extractors
from ImageCrawling import toolbox
from ImageCrawling import database_tools
from statistics import mean

from website_main import mobilenet

def hashing_time_one_search(feature):
    
    #feature = mobilenet_extractor.extractImage(img)
    #uploaded_img = toolbox.image_to_base64(img)

    #image = toolbox.image_to_binary(img)
    startTime = time.time()
    
    results = ImageCrawling.get_nearest_images_2("final.db", None, "big", ImageCrawling.mobileNet, feature,
                                                count=50)
    return (time.time() - startTime)

def euklid_time_one_search(feature):
    
    #feature = mobilenet_extractor.extractImage(img)
    #uploaded_img = toolbox.image_to_base64(img)

    #image = toolbox.image_to_binary(img)
    startTime = time.time()
    
    results = ImageCrawling.get_nearest_images("final.db", None, "big", ImageCrawling.mobileNet, feature,
                                                count=50)[:50]
    return (time.time() - startTime)


def get_avg_time(func):
    mobilenet = extractors.MobileNet()
    time_list = []
    keywords = database_tools.get_all_keywords
    
    for image_class in keywords:
        class_time_list = []
        test_images = database_tools.get_test_images_for_class("final.db", ImageCrawling.mobileNet, "big", image_class)[:100]
        
        for img in test_images:
            t = func(mobilenet.extractImage(img))
            class_time_list.append(t)
            mean_class_time = mean(class_time_list)
        print('Average time for ' + image_class + " : " + str(mean_class_time))
        time_list.append(mean_class_time)
    
    print("Average time in total: " + str(mean(time_list)))


if __name__=="__main__":
    
    print('hasing time: \n')
    get_avg_time(hashing_time_one_search)
    print('\n')
    print('euklid time: \n')
    get_avg_time(euklid_time_one_search)



