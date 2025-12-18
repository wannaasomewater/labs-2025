import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Определение устройства
if torch.backends.mps.is_available():
    device = torch.device('mps')
elif torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

print(f"Используется: {device}")

class DigitRecognizer(nn.Module):
    def __init__(self):
        super(DigitRecognizer, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 784)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

print("Загрузка обученной модели...")
model = DigitRecognizer()
model.load_state_dict(torch.load('digit_recognition_pytorch.pth'))
model.to(device)
model.eval()  # Режим оценки (отключает dropout)
print("Модель загружена успешно!")

def predict_digit(image_array):
    """
    Предсказывает цифру по изображению

    Args:
        image_array: numpy массив (28, 28) со значениями 0-255 или 0-1

    Returns:
        digit: предсказанная цифра (0-9)
        confidence: уверенность в %
    """
    # Нормализация
    if image_array.max() > 1.0:
        image_array = image_array / 255.0

    # Преобразование в тензор
    image_tensor = torch.FloatTensor(image_array).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_digit = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_digit].item() * 100

        # Показываем все вероятности
        print("\nВероятности для каждой цифры:")
        for i in range(10):
            print(f"  Цифра {i}: {probabilities[0][i].item() * 100:.2f}%")

    return predicted_digit, confidence



# загрузка mnist
# print("\n" + "="*50)
# print("ТЕСТ 1: Загрузка примера из MNIST")
# print("="*50)

# from torchvision import datasets, transforms

# # Загрузка тестового набора MNIST
# test_dataset = datasets.MNIST(root='./data', train=False, download=True,
#                               transform=transforms.ToTensor())

# # Берём случайное изображение
# idx = np.random.randint(0, len(test_dataset))
# test_image, true_label = test_dataset[idx]

# # Предсказание
# image_np = test_image.squeeze().numpy()
# predicted, conf = predict_digit(image_np)

# # Визуализация
# plt.figure(figsize=(6, 6))
# plt.imshow(image_np, cmap='gray')
# color = 'green' if predicted == true_label else 'red'
# plt.title(f'Предсказано: {predicted} (уверенность: {conf:.1f}%)\n'
#           f'Реально: {true_label}', color=color, fontsize=14)
# plt.axis('off')
# plt.savefig('test_prediction.png', dpi=100, bbox_inches='tight')
# plt.show()

# print(f"\nПредсказанная цифра: {predicted}")
# print(f"Уверенность: {conf:.2f}%")
# print(f"Реальная цифра: {true_label}")
# print(f"Результат: {'✓ ПРАВИЛЬНО' if predicted == true_label else '✗ ОШИБКА'}")

# Тест на своем изображении
print("\n" + "="*50)
print("ТЕСТ 2: Использование своего изображения")
print("="*50)

try:
    # Загрузка изображения
    img = Image.open('my_digit.png').convert('L')  # Grayscale
    img = img.resize((28, 28))  # Изменение размера до 28x28
    img_array = np.array(img)

    # Инверсия (если нарисовали чёрную цифру на белом фоне)
    # img_array = 255 - img_array

    # Предсказание
    digit, confidence = predict_digit(img_array)

    plt.figure(figsize=(6, 6))
    plt.imshow(img_array, cmap='gray')
    plt.title(f'Предсказано: {digit} ({confidence:.1f}%)', fontsize=14)
    plt.axis('off')
    plt.show()

    print(f"Предсказанная цифра: {digit}")
    print(f"Уверенность: {confidence:.2f}%")
except FileNotFoundError:
    print("Файл 'my_digit.png' не найден")

print("\n" + "="*50)
print("Модель готова к использованию!")
print("="*50)
