import tensorflow as tf
import numpy as np
from tensorflow import keras
''' 
mnist = tf.keras.datasets.mnist

#load mnist data and convert from int to float
(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

#create sequential model to train
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])
predictions = model(x_train[:1]).numpy()
tf.nn.softmax(predictions).numpy()
print ("array", predictions)

#calculate losses using categorical crossentropy
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
print("loss ", loss_fn(y_train[:1],predictions).numpy())
'''
#learn what function the xs go into to get ys
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
model.compile(optimizer='sgd',loss='mean_squared_error')
xs = np.array([-1.0,0.0,1.0,2.0,3.0,4.0],dtype=float)
ys = np.array([-2.0,1.0,4.0,7.0,10.0,13.0],dtype=float)
model.fit(xs, ys, epochs=50)
print(model.predict([10.0]))