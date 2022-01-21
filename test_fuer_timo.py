import io
import os

import numpy as np
from PIL import Image
from ImageCrawling import toolbox
from ImageCrawling import feature_interface
import ImageCrawling


from ImageCrawling import database_tools

if __name__ == '__main__':
    # Ordner muss nicht mehr gewechselt werden!

    # generiere ein Bild zum suchen
    image = toolbox.get_test_image()[2]
    # Image ist ein binay --> also konvertieren
    toolbox.binary_to_image(image).show()


    # feature wird jetzt innerhalb der funktion neu berechnet
    # image muss ein Bild im Binärformat sein
    # toolbox.image_to_binary() kann ein Image zu binär umwandeln
    images = ImageCrawling.get_nearest_images("light_database.db", image, "cifar10", "mobileNet", feature_interface.mobileNet_func, count=10)
    # Gibt Liste der Form: [(Image, distance), ...] zurück
    # Image ist ein PIL Image Objekt
    # distance ist eine numpy float Zahl (funktioniert wie normale Float)

    # Zeige Ergebnisse an:
    for i in images:
        i[0].show()