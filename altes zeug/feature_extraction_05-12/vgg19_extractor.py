from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG19, preprocess_input
from tensorflow.keras.models import Model
import numpy as np

model = tf.keras.application.VGG19(include_top=True, weight='imagenet')