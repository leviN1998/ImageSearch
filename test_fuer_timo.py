import os
from PIL import Image
import io
from tensorflow import keras
import numpy as np
from ImageCrawling import database_tools

if __name__ == '__main__':
    old_dir = os.getcwd()
    os.chdir('ImageDatabases')

    image = database_tools.__dummy_get_test_image()
    Image.open(io.BytesIO(image[2])).convert("RGB").resize((500, 500)).show()
    feature = np.load(io.BytesIO(image[1]))

    images = database_tools.get_nearest_images("light_database.db", feature, "cifar10", "mobileNet", count=10)
    # Gibt Liste der Form: [(Image, distance), ...] zurück
    # Image ist ein PIL Image Objekt
    # distance ist eine numpy float Zahl (funktioniert wie normale Float)

    # Zeige Ergebnisse an:
    for i in images:
        i[0].show()