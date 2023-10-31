import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt


col_names = ['i', 'pSist', 'pDiast', 'qPA', 'pulso', 'resp', 'gravid', 'classe']
data = pd.read_csv("treino_sinais_vitais_com_label.csv", header=None, names=col_names)

data = data.drop('gravid', axis=1)
col_names.remove('gravid')
print(data.head(10))

X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=50)

num_columns = X_train.shape[1]

model = Sequential()
model.add(Dense(units=32, activation='relu', input_dim=num_columns))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=4, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics='accuracy')
# model.compile(loss='mean_absolute_error', optimizer='adam', metrics='accuracy')
y_train_one_hot = to_categorical(Y_train - 1)
history = model.fit(X_train, y_train_one_hot, epochs=100, batch_size=32, validation_data=(X_test, Y_test))


plt.plot(history.history['loss'], label='Loss (Training)')
plt.plot(history.history['val_loss'], label='Loss (Validation)')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()