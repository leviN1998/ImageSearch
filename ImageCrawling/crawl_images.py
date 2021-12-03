import crawling

searchstrings = [   "airplane",
					"automobile",
					"bird",
					"cat",
					"deer",
					"dog",
					"frog",
					"horse",
					"ship",
					"truck" ]

folder = "ImageCrawling/image_set_1"


if __name__ == "__main__":
	for s in searchstrings:
		crawling.download_images(s, folder=folder)