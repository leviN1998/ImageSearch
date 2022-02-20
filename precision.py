import ImageCrawling
import numpy as np
import io
import statistics
from ImageCrawling import database_tools

# search precision
def precision(database: str, network: str):
    keywords = ImageCrawling.get_keywords(database)

    precision_for_keyword = []
    precision_for_all = []

    for k in keywords:
        test_bi_feas = database_tools.get_test_images_for_class(database, network, "big", k)[:10]
        for fea in test_bi_feas:
            # feature = extractors.MobileNet.extractImage(img)
            classes = ImageCrawling.search_for_classes(database, "big", network, fea, count=50)
            count = 0
            for c in classes:
                if k == c:
                    count += 1
            pre = count/50
            # print(pre)
            precision_for_keyword.append(pre)
        avg_pre = sum(precision_for_keyword)/10
        print("precision for class:" + avg_pre)
        precision_for_all.append(avg_pre)
    return statistics.mean(precision_for_all)


if __name__ == "__main__":
    print(precision("final.db", ImageCrawling.mobileNet))