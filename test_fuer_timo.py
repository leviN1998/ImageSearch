import os
from PIL import Image
import io
from tensorflow import keras
import numpy as np
from ImageCrawling import database_tools

if __name__ == '__main__':
    # Wichtig! sonst wird Datenbank nicht gefunden
    # am ende wieder zurückwechseln mit os.chdir(old_dir)
    old_dir = os.getcwd()
    os.chdir('ImageDatabases')

    # Der Teil generiert nur ein Bild zum testen und das feature dazu
    image = database_tools.__dummy_get_test_image()
    Image.open(io.BytesIO(image[2])).convert("RGB").resize((500, 500)).show()
    feature = np.load(io.BytesIO(image[1]))


    # feature muss das von MoblieNet berechnete Numpy-Array sein
    # um ein feature zu berechnen kann database_tools.__dummy_feature_func(images) verwendet werden
    # images muss ein Array aus PIL Images sein z.b. [image1] oder so
    images = database_tools.get_nearest_images("light_database.db", feature, "cifar10", "mobileNet", count=10)
    # Gibt Liste der Form: [(Image, distance), ...] zurück
    # Image ist ein PIL Image Objekt
    # distance ist eine numpy float Zahl (funktioniert wie normale Float)

    os.chdir(old_dir)

    # Zeige Ergebnisse an:
    for i in images:
        i[0].show()