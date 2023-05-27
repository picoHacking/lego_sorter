import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
import random
print(tf.__version__)
mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels),(test_images, test_labels) = mnist.load_data()
## we'll have to make our own load_data() function ##
class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle boot']

print('number, height, and width of training images', train_images.shape)
print('number, height, and width of test images', test_images.shape)

# scale color values to a number between 0 and 1

training_images = train_images / 255.0
test_images = test_images / 255.0

# create machine learning model

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)), # convert 2D array to 1D array of pixels
    keras.layers.Dense(128, activation = 'relu'), # 128 neurons
    keras.layers.Dense(10) # logits array of 10 scores that are how likely each image is to belong in each of 10 categories
])

# loss function : mathematical function to compare actual and predicted results
# optimizer : updates data based on loss function
# metrics : monitor information from testing and training (e.g. percent correctly classified)

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs = 10) # matches training images to training labels over 10 iterations

# show 25 training images

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1) # dimensions of plot
    plt.xticks([]) # remove x ticks
    plt.yticks([]) # remove y ticks
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.grid(False)
    plt.xlabel(class_names[train_labels[i]])
    #plt.colorbar()

test_loss, test_acc = model.evaluate(test_images, test_labels)

# show test images

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(7, 7, i+1) # dimensions of plot
    plt.xticks([]) # remove x ticks
    plt.yticks([]) # remove y ticks
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.grid(False)
    plt.xlabel(class_names[test_labels[i]])
    #plt.colorbar()

print('\nTest accuracy:', test_acc)

probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

plt.show()
