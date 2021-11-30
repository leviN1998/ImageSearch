# Image Crawling

Python Skripts to crawl images from different websites using search-keywords

crawling.py contains base functions needed to crawl images
crawl_images.py contains skript to generate the first image-set

Known Issues:
- only ca. 80 images per keyword are crawled
- images might be not very usefull logos, toys etc.
- only GOOGLE supportet to get images from
- no keywording or metric implemented yet

TODOs:
- Change Engine to Selenium instead of BeatifulSoup
- try other websites (See TODO.txt)
- implement keywording as metric
- think of other usefull metrics to increase image quality
- generate larger imageset
- think of usefull keywords to get new images
