import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from keras.utils import to_categorical
import matplotlib.pyplot as plt


col_names = ['i', 'pSist', 'pDiast', 'qPA', 'pulso', 'resp', 'gravid', 'classe']
data = pd.read_csv("treino_sinais_vitais_com_label.csv", header=None, names=col_names)
print(data.head(10))

X = pd.get_dummies(data.drop(['classe', 'gravid'], axis=1))
Y = data['classe']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.3)

model = Sequential()
model.add(Dense(units=16, activation='relu', input_dim=len(X_train.columns)))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=4, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',
               metrics=['accuracy'])

# Subtraia 1 se suas classes são 1, 2, 3 e 4 em vez de 0, 1, 2 e 3
Y_train_one_hot = to_categorical(Y_train - 1)

# Agora use y_train_one_hot em vez de y_train ao ajustar o modelo
history = model.fit(X_train, Y_train_one_hot, epochs=500, batch_size=32)

Y_hat = model.predict(X_test)
Y_hat = np.argmax(Y_hat, axis=1) + 1
print(accuracy_score(Y_test, Y_hat))

plt.plot(history.history['loss'], label='Loss (Training)')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()