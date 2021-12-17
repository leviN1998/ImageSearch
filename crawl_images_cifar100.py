import ImageCrawling as ic

aquatic_mammals = ["beaver", "dolphin", "otter", "seal", "whale"]
fish = ["aquarium fish", "flatfish", "ray", "shark", "trout"]
flowers = ["orchids", "poppies", "roses", "sunflowers", "tulips"]
food_containers = ["bottles", "bowls", "cans", "cups", "plates"]
fruit_and_vegetables = ["apples", "mushrooms", "oranges", "pears", "sweet peppers"]
household_electrical_devices = ["clock", "computer keyboard", "lamp", "telephone", "television"]
household_furniture = ["bed", "chair", "couch", "table", "wardrobe"]
insects = [	"bee", "beetle", "butterfly", "caterpillar", "cockroach"]
large_carnivores = ["bear", "leopard", "lion", "tiger", "wolf"]
large_man_made_outdoor_things = ["bridge", "castle", "house", "road", "skyscraper"]
large_natural_outdoor_scenes = ["cloud", "forest", "mountain", "plain", "sea"]
large_omnivores_and_herbivores = ["camel", "cattle", "chimpanzee", "elephant", "kangaroo"]
medium_sized_mammals = ["fox", "porcupine", "possum", "raccoon", "skunk"]
non_insect_invertebrates = ["crab", "lobster", "snail", "spider", "worm"]
people = ["baby", "boy", "girl", "man", "woman"]
reptiles = ["crocodile", "dinosaur", "lizard", "snake", "turtle"]
small_mammals = ["hamster", "mouse", "rabbit", "shrew", "squirrel"]
trees = ["maple", "oak", "palm", "pine", "willow"]
vehicles_1 = ["bicycle", "bus", "motorcycle", "pickup truck", "train"]
vehicles_2 = ["lawn-mower", "rocket", "streetcar", "tank", "tractor"]

keywords = [aquatic_mammals, fish, flowers, food_containers, fruit_and_vegetables, household_electrical_devices, household_furniture,
insects, large_carnivores, large_man_made_outdoor_things, large_natural_outdoor_scenes, large_omnivores_and_herbivores, medium_sized_mammals,
non_insect_invertebrates, people, reptiles, small_mammals, trees, vehicles_1, vehicles_2]


folder1 = "ImageDatabases/cifar100_2000/" + "aquatic_mammals"
folder2 = "ImageDatabases/cifar100_2000/" + "fish"
folder3 = "ImageDatabases/cifar100_2000/" + "flowers"
folder4 = "ImageDatabases/cifar100_2000/" + "food_containers"
folder5 = "ImageDatabases/cifar100_2000/" + "fruit_and_vegetables"
folder6 = "ImageDatabases/cifar100_2000/" + "household_electrical_devices"
folder7 = "ImageDatabases/cifar100_2000/" + "household_furniture"
folder8 = "ImageDatabases/cifar100_2000/" + "insects"
folder9 = "ImageDatabases/cifar100_2000/" + "large_carnivores"
folder10 = "ImageDatabases/cifar100_2000/" + "large_man_made_outdoor_things"
folder11 = "ImageDatabases/cifar100_2000/" + "large_natural_outdoor_scenes"
folder12 = "ImageDatabases/cifar100_2000/" + "large_omnivores_and_herbivores"
folder13 = "ImageDatabases/cifar100_2000/" + "medium_sized_mammals"
folder14 = "ImageDatabases/cifar100_2000/" + "non_insect_invertebrates"
folder15 = "ImageDatabases/cifar100_2000/" + "people"
folder16 = "ImageDatabases/cifar100_2000/" + "reptiles"
folder17 = "ImageDatabases/cifar100_2000/" + "small_mammals"
folder18 = "ImageDatabases/cifar100_2000/" + "trees"
folder19 = "ImageDatabases/cifar100_2000/" + "vehicles_1"
folder20 = "ImageDatabases/cifar100_2000/" + "vehicles_2"

folders = [ folder1, folder2,  folder3, folder4, folder5, folder6, folder7, folder8, folder9, folder10, folder11, folder12, folder13, folder14, folder15, folder16, folder17, folder18, folder19, folder20]


if __name__ == "__main__":
    print(len(folders))
    print(len(keywords))

    for i in range(0,20):
        for s in keywords[i]:
            try:
                ic.download_images(s, image_count=2000, folder=folders[i], verbose=True)
            except:
                ic.download_images(s, image_count=2000, folder=folders[i], verbose=True)