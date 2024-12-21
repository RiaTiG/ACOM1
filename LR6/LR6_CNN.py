import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import time

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1).astype('float32') / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

def build_cnn():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(10, activation='softmax'))
    
    return model

epochs_list = [5, 10, 20, 50]
results = []
for epochs in epochs_list:
    print(f"\nТренировка модели с {epochs} эпохами...\n")
    cnn_model = build_cnn()
    cnn_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    train_start_time = time.time()
    cnn_model.fit(x_train, y_train, epochs=epochs, batch_size=32, validation_split=0.2, verbose=1)
    train_end_time = time.time()
    train_duration = train_end_time - train_start_time
    test_start_time = time.time()
    test_loss, test_acc = cnn_model.evaluate(x_test, y_test, verbose=0)
    test_end_time = time.time()
    test_duration = test_end_time - test_start_time
    
    results.append({
        'epochs': epochs,
        'train_time': train_duration,
        'test_accuracy': test_acc,
        'test_time': test_duration
    })

for res in results:
    print(f"\nЭпохи: {res['epochs']}")
    print(f"  Время тестирования: {res['test_time']:.2f} сек")
    print(f"  Точность на тестовых данных: {res['test_accuracy']:.2%}")
    print(f"  Время Обучения: {res['train_time']:.2f} сек")
