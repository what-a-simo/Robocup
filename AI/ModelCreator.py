import os
import cv2
import keras
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import layers
from keras.api.datasets import mnist
import keras.api as k_api
from keras.src.metrics.accuracy_metrics import accuracy
from tensorboard.plugins.image.summary import image

img_height = 64
img_width = 40
batch_size = 2

model = keras.Sequential([
    layers.Input((img_height,img_width,1)),
    layers.Conv2D(16,3, padding='same'),
    layers.Conv2D(16,3, padding='same'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(10),
])

ds_train = keras.preprocessing.image_dataset_from_directory(
    'TestTraining',
    labels='inferred',
    label_mode = 'int',
    color_mode='grayscale',
    batch_size=batch_size,
    image_size=(img_height,img_width),
    shuffle=True,
    seed=123,
    validation_split=0.1,
    subset="training",
)

ds_validation = keras.preprocessing.image_dataset_from_directory(
    'TestTraining',
    labels='inferred',
    label_mode = 'int',
    color_mode='grayscale',
    batch_size=batch_size,
    image_size=(img_height,img_width),
    shuffle=True,
    seed=123,
    validation_split=0.1,
    subset="validation",
)

def augment(x, y):
    image = tf.image.random_brightness(x, max_delta=0.05)
    return image , y

ds_train = ds_train.map(augment)

model.compile(
    optimizer=keras.optimizers.Adam(),
    loss=[
        keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    ],
    metrics=["accuracy"],
)

model.fit(ds_train, epochs=10, verbose=2)

model.save('testModel.keras')


