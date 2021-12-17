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

# folder = "ImageDatabases/cifar10_80"
# folder = "ImageDatabases/cifar10_200"
folder = "ImageDatabases/cifar10_6000"


if __name__ == "__main__":
	for s in searchstrings:
		ic.download_images(s, image_count=6000, folder=folder, verbose=True)