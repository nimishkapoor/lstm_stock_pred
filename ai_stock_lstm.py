# -*- coding: utf-8 -*-
"""AI Stock LSTM

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18WiSw1K0BW3jOKO56vxn11Fo9IyOuRjh

In this Colab, we will use a keras Long Short-Term Memory (LSTM) model to predict the stock price of Tata Global Beverages

Here are some imports we need to make: numpy for scientific computation, matplotlib for graphing, and pandas for manipulating data.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""Load training data set with the "Open" and "High" columns to use in our modeling."""

url = '/Users/nimishkapoor/Downloads/INDIACEM.NS.csv'
dataset_train = pd.read_csv(url)

dataset_train.head()

dataset_train.tail(12)

dataset_train = dataset_train[-12:]

dataset_train.head(12)

training_set = dataset_train.iloc[:, 1:2].values

"""Let's take a look at the first five rows of our dataset"""

dataset_train.head()

"""Import MinMaxScaler from scikit-learn to scale our dataset into numbers between 0 and 1 """

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

print(training_set_scaled)

"""We want our data to be in the form of a 3D array for our LSTM model. First, we create data in 60 timesteps and convert it into an array using NumPy. Then, we convert the data into a 3D array with X_train samples, 60 timestamps, and one feature at each step."""

X_train = []
y_train = []
for i in range(3, 12):
    X_train.append(training_set_scaled[i-3:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

print(X_train)



print(y_train)

"""Make the necessary imports from keras"""

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense

"""Add LSTM layer along with dropout layers to prevent overfitting. After that, we add a Dense layer that specifies a one unit output. Next, we compile the model using the adam optimizer and set the loss as the mean_squarred_error"""

model = Sequential()

model.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))

model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))

model.compile(optimizer='adam',loss='mean_squared_error')

model.fit(X_train,y_train,epochs=100,batch_size=32)

"""Import the test set for the model to make predictions on """

url = 'https://raw.githubusercontent.com/mwitiderrick/stockprice/master/tatatest.csv'
dataset_test = pd.read_csv(url)

dataset_test.head()

dataset_test = dataset_test[:6]

dataset_test.head(10)

real_stock_price = dataset_test.iloc[:, 1:2].values

print(real_stock_price)

dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)

dataset_total.head(20)

inputs = dataset_total[len(dataset_total) - len(dataset_test) - 3:].values

print(inputs)

inputs = inputs.reshape(-1,1)

print(inputs)

inputs = sc.fit_transform(inputs)

print(inputs)

X_test = []
for i in range(3, 9):
    X_test.append(inputs[i-3:i, 0])

print(X_test)

X_test = np.array(X_test)

print(X_test)

X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

print(X_test)

predicted_stock_price = model.predict(X_test)

print(predicted_stock_price)

predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print(predicted_stock_price)

"""Before predicting future stock prices, we have to manipulate the training set; we merge the training set and the test set on the 0 axis, set the time step to 60, use minmaxscaler, and reshape the dataset as done previously. After making predictions, we use inverse_transform to get back the stock prices in normal readable format.

"""



plt.plot(real_stock_price, color = 'black', label = 'TATA Stock Price')
plt.plot(predicted_stock_price, color = 'green', label = 'Predicted TATA Stock Price')
plt.title('TATA Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('TATA Stock Price')
plt.legend()
plt.show()