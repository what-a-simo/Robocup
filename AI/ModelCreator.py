import os
import cv2
import keras
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
from keras import layers
from keras.api.datasets import mnist
import keras.api as k_api
from keras.src.metrics.accuracy_metrics import accuracy
from tensorboard.plugins.image.summary import image

img_height = 64
img_width = 40
batch_size = 16

# model = keras.Sequential([
#     layers.Input((img_height,img_width,3)),
#     layers.Conv2D(32,3, padding='same'),
#     layers.Conv2D(32,3, padding='same'),
#     layers.MaxPooling2D(),
#     layers.Flatten(),
#     layers.Dense(10),
# ])
#
# ds_train = keras.preprocessing.image_dataset_from_directory(
#     'TestTraining',
#     labels='inferred',
#     label_mode = 'int',
#     color_mode='rgb',
#     batch_size=batch_size,
#     image_size=(img_height,img_width),
#     shuffle=True,
#     seed=123,
#     validation_split=0.1,
#     subset="training",
# )
#
# ds_validation = keras.preprocessing.image_dataset_from_directory(
#     'TestTraining',
#     labels='inferred',
#     label_mode = 'int',
#     color_mode='rgb',
#     batch_size=batch_size,
#     image_size=(img_height,img_width),
#     shuffle=True,
#     seed=123,
#     validation_split=0.1,
#     subset="validation",
# )
#
# def augment(x, y):
#     image = tf.image.random_brightness(x, max_delta=0.05)
#     return image , y
#
# ds_train = ds_train.map(augment)
#
# model.compile(
#     optimizer=keras.optimizers.Adam(),
#     loss=[
#         keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#     ],
#     metrics=["accuracy"],
# )
#
# model.fit(ds_train, epochs=10, verbose=2)
#
# model.save('testModel.keras')

model= keras.models.load_model('testModel.keras')

image1 = tf.io.read_file("TestTraining/onlyWall/img2.png")
image1 = tf.image.decode_jpeg(image1, channels=3)
image1 = tf.image.resize(image1, [64, 40])
image1 = image1 / 255.0
image1 = tf.expand_dims(image1, axis=0)

output = model.predict(image1)
predicted_class = tf.argmax(output, axis=-1).numpy()[0]
match predicted_class:
    case 0:
        print("Is corrosive")
    case 1:
        print("Is flammable")
    case 2:
        print("Is an H")
    case 3:
        print("Is a wall")
    case 4:
        print("Is organic")
    case 5:
        print("Is poison")
    case 6:
        print("Is an S")
    case 7:
        print("Is an U")
    case _:
        print("Undefined")
