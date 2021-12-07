import ImageCrawling as ic

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

folder = "ImageDatabases/cifar10_80"


if __name__ == "__main__":
	for s in searchstrings:
		ic.download_images(s, folder=folder)