import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import time

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

def create_model():
    model = Sequential([
        Flatten(input_shape=(28, 28)),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

results = []
for epochs in [5, 10, 20, 50]:
    print(f'\n=== Обучение модели (количество эпох: {epochs}) ===')
    
    model = create_model()
    
    start_time = time.time()
    model.fit(x_train, y_train, epochs=epochs, batch_size=32, validation_split=0.5, verbose=0)
    training_time = time.time() - start_time
    print(f'Время обучения: {training_time:.2f} сек')
    
    start_time = time.time()
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    inference_time = time.time() - start_time
    print(f'Точность на тестовых данных: {test_accuracy:.2%}')
    print(f'Время работы модели на тестовых данных: {inference_time:.2f} сек')

    results.append({
        'epochs': epochs,
        'training_time': training_time,
        'test_accuracy': test_accuracy,
        'inference_time': inference_time
    })

print("\n=== Сравнительные результаты ===")
for res in results:
    print(f"Эпохи: {res['epochs']}, "
          f"Время обучения: {res['training_time']:.2f} сек, "
          f"Точность: {res['test_accuracy']:.2%}, "
          f"Время работы на тесте: {res['inference_time']:.4f} сек")






