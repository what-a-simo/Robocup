import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.api.datasets import mnist
import keras.api as k_api
from keras.src.metrics.accuracy_metrics import accuracy

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = k_api.utils.normalize(x_train, axis=1)
x_test = k_api.utils.normalize(x_test, axis=1)

model = k_api.models.Sequential()
model.add(k_api.layers.Flatten(input_shape=(28,28)))
model.add(k_api.layers.Dense(128, activation='relu'))
model.add(k_api.layers.Dense(128, activation='relu'))
model.add(k_api.layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train,y_train, epochs=10)

model.save('handwritten.keras')

loss, accuracy = model.evaluate(x_test,y_test)

print(loss)
print(accuracy)

#model = k_api.models.load_model('handwritten.keras')

#image_number = 1
#while os.path.isfile(f"digits/digit{image_number}.png"):
#    try:
#        img = cv2.imread(f"digits/digit{image_number}.png")[:,:,0]
#        img = np.invert(np.array([img]))
#        prediction = model.predict(img)
#        print(f"This is digit is propably a {np.argmax(prediction)}")
#        print(prediction)
#        plt.imshow(img[0], cmap=plt.cm.binary)
#        plt.show()
#    except:
#        print("error")
#    finally:
#        image_number += 1

