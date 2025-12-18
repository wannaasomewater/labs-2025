import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

# загрузка датасета
print("Загрузка датасета MNIST...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(f"Размер обучающей выборки: {x_train.shape}")
print(f"Размер тестовой выборки: {x_test.shape}")

# нормализация данных
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# преобразование изображений 28x28 в вектор 784
x_train = x_train.reshape(-1, 28*28)
x_test = x_test.reshape(-1, 28*28)

# преобразование меток в one-hot encoding
y_train_categorical = keras.utils.to_categorical(y_train, 10)
y_test_categorical = keras.utils.to_categorical(y_test, 10)

print(f"Форма после преобразования: {x_train.shape}")
print(f"Форма меток: {y_train_categorical.shape}")

print("\nСоздание модели нейросети...")

model = keras.Sequential([
    # 128 - число нейронов в скрытом слое
    # 784 - число нейронов на входном слое
    layers.Dense(128, activation='relu', input_shape=(784,), name='hidden_layer'),

    # дропаут для предотвращения переобучения
    # случайным образом выключает 20 % нейронов
    layers.Dropout(0.2, name='dropout_layer'),

    # выходной слой - 10 нейронов, softmax для представления значений в виде вероятностей
    layers.Dense(10, activation='softmax', name='output_layer')
])

# компиляция модели
model.compile(


    optimizer='adam',  # подстраивает learning rate (вместо обычно градиентного спуска)
    loss='categorical_crossentropy',  # функция потерь
    metrics=['accuracy']
)

# вывод архитектуры модели
model.summary()

# обучение
print("\nНачало обучения...")

history = model.fit(
    x_train,
    y_train_categorical,
    epochs=10,
    # обработка 128 пачек данных перед обновлением весов
    batch_size=128,
    validation_split=0.1,
    verbose=1
)

print("\nОценка модели на тестовых данных...")
test_loss, test_accuracy = model.evaluate(x_test, y_test_categorical, verbose=0)
print(f"Точность на тестовой выборке: {test_accuracy * 100:.2f}%")
print(f"Потери на тестовой выборке: {test_loss:.4f}")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Точность на обучении')
plt.plot(history.history['val_accuracy'], label='Точность на валидации')
plt.title('Точность модели')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Потери на обучении')
plt.plot(history.history['val_loss'], label='Потери на валидации')
plt.title('Потери модели')
plt.xlabel('Эпоха')
plt.ylabel('Потери')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_history.png', dpi=100)
print("\nГрафик обучения сохранен в 'training_history.png'")

print("\nТестирование на случайных примерах...")

indices = np.random.choice(len(x_test), 10, replace=False)

plt.figure(figsize=(15, 3))
for i, idx in enumerate(indices):

    prediction = model.predict(x_test[idx:idx+1], verbose=0)
    predicted_digit = np.argmax(prediction)
    true_digit = y_test[idx]

    plt.subplot(2, 5, i + 1)
    plt.imshow(x_test[idx].reshape(28, 28), cmap='gray')
    color = 'green' if predicted_digit == true_digit else 'red'
    plt.title(f'Предсказано: {predicted_digit}\nРеально: {true_digit}', color=color)
    plt.axis('off')

plt.tight_layout()
plt.savefig('predictions.png', dpi=100)
print("Примеры предсказаний сохранены в 'predictions.png'")

# функция для пользовательского ввода
def predict_digit(image_array):
    """
    Функция для предсказания цифры из массива изображения

    Args:
        image_array: numpy массив размером (28, 28) со значениями 0-255

    Returns:
        predicted_digit: предсказанная цифра (0-9)
        confidence: уверенность модели в %
    """
    # нормализация и преобразование формы
    if image_array.max() > 1.0:
        image_array = image_array / 255.0

    image_array = image_array.reshape(1, 784)

    # предсказание
    prediction = model.predict(image_array, verbose=0)
    predicted_digit = np.argmax(prediction)
    confidence = prediction[0][predicted_digit] * 100

    return predicted_digit, confidence

# пример использования функции
print("\nПример использования функции предсказания:")
test_image = x_test[0].reshape(28, 28)
digit, conf = predict_digit(test_image)
print(f"Предсказанная цифра: {digit}")
print(f"Уверенность: {conf:.2f}%")
print(f"Реальная цифра: {y_test[0]}")

print("\nСохранение модели...")
model.save('digit_recognition_model.h5')
print("Модель сохранена в 'digit_recognition_model.h5'")

# если надо загрузить
# loaded_model = keras.models.load_model('digit_recognition_model.h5')

print("\n" + "="*60)
print("ОБУЧЕНИЕ ЗАВЕРШЕНО!")
print(f"Финальная точность: {test_accuracy * 100:.2f}%")
print("="*60)
