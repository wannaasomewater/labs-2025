import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms

# использование процессора
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

print("Загрузка датасета MNIST...")

# загрузка mnist
transform = transforms.Compose([
    transforms.ToTensor(),
])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

print(f"Размер обучающей выборки: {len(train_dataset)}")
print(f"Размер тестовой выборки: {len(test_dataset)}")

# аналог batch процессинга в Keras
batch_size = 128
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# отдельный валидационный набор (10% от train)
train_size = int(0.9 * len(train_dataset))
val_size = len(train_dataset) - train_size
train_subset, val_subset = torch.utils.data.random_split(train_dataset, [train_size, val_size])

train_loader = DataLoader(train_subset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=batch_size, shuffle=False)

print("\nСоздание модели нейросети...")

class DigitRecognizer(nn.Module):
    def __init__(self):
        super(DigitRecognizer, self).__init__()

        # входной слой 784
        self.fc1 = nn.Linear(784, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

        # выходной слой 10
        self.fc2 = nn.Linear(128, 10)
        # в PyTorch softmax НЕ добавляется в модель,
        # CrossEntropyLoss уже включает softmax

    def forward(self, x):
        # преобразование изображения 28x28 в вектор 784
        x = x.view(-1, 784)

        # прямое распространение
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)

        return x

model = DigitRecognizer().to(device)

# вывод архитектуры
print(model)
print(f"\nВсего параметров: {sum(p.numel() for p in model.parameters())}")

# Функция потерь (включает softmax автоматически!)
criterion = nn.CrossEntropyLoss()

# оптимизатор тот же самый что и в tensorflow
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("\nНачало обучения...")

epochs = 10
history = {
    'train_loss': [],
    'train_acc': [],
    'val_loss': [],
    'val_acc': []
}

for epoch in range(epochs):
    model.train()
    train_loss = 0
    train_correct = 0
    train_total = 0

    for batch_idx, (images, labels) in enumerate(train_loader):
        # перенос данных на cpu или gpu
        images, labels = images.to(device), labels.to(device)

        # обнуление градиентов
        optimizer.zero_grad()

        # прямое распространение
        outputs = model(images)
        loss = criterion(outputs, labels)

        # обратное распространение
        loss.backward()

        # обновление весов
        optimizer.step()

        # статистика
        train_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        train_total += labels.size(0)
        train_correct += (predicted == labels).sum().item()

    train_loss = train_loss / len(train_loader)
    train_acc = train_correct / train_total

    # валидация
    model.eval()
    val_loss = 0
    val_correct = 0
    val_total = 0

    with torch.no_grad():  # отключаем вычисление градиентов
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_loss = val_loss / len(val_loader)
    val_acc = val_correct / val_total

    # сохранение истории
    history['train_loss'].append(train_loss)
    history['train_acc'].append(train_acc)
    history['val_loss'].append(val_loss)
    history['val_acc'].append(val_acc)

    print(f"Эпоха {epoch+1}/{epochs} - "
          f"loss: {train_loss:.4f} - acc: {train_acc:.4f} - "
          f"val_loss: {val_loss:.4f} - val_acc: {val_acc:.4f}")


# ОЦЕНКА НА ТЕСТЕ


print("\nОценка модели на тестовых данных...")
model.eval()
test_correct = 0
test_total = 0
test_loss = 0

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        test_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        test_total += labels.size(0)
        test_correct += (predicted == labels).sum().item()

test_accuracy = test_correct / test_total
test_loss = test_loss / len(test_loader)
print(f"Точность на тестовой выборке: {test_accuracy * 100:.2f}%")
print(f"Потери на тестовой выборке: {test_loss:.4f}")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history['train_acc'], label='Точность на обучении')
plt.plot(history['val_acc'], label='Точность на валидации')
plt.title('Точность модели')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history['train_loss'], label='Потери на обучении')
plt.plot(history['val_loss'], label='Потери на валидации')
plt.title('Потери модели')
plt.xlabel('Эпоха')
plt.ylabel('Потери')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_history_pytorch.png', dpi=100)
print("\nГрафик обучения сохранен в 'training_history_pytorch.png'")

print("\nТестирование на случайных примерах...")

# получаем несколько примеров из тестового набора
test_images = []
test_labels = []
for images, labels in test_loader:
    test_images = images
    test_labels = labels
    break

# выбираем 10 случайных
indices = np.random.choice(len(test_images), 10, replace=False)

model.eval()
plt.figure(figsize=(15, 3))
with torch.no_grad():
    for i, idx in enumerate(indices):
        image = test_images[idx].unsqueeze(0).to(device)
        label = test_labels[idx].item()

        output = model(image)
        probabilities = torch.softmax(output, dim=1)
        predicted = torch.argmax(probabilities, dim=1).item()

        plt.subplot(2, 5, i + 1)
        plt.imshow(test_images[idx].squeeze(), cmap='gray')
        color = 'green' if predicted == label else 'red'
        plt.title(f'Предсказано: {predicted}\nРеально: {label}', color=color)
        plt.axis('off')

plt.tight_layout()
plt.savefig('predictions_pytorch.png', dpi=100)
print("Примеры предсказаний сохранены в 'predictions_pytorch.png'")


def predict_digit(image_array):
    """
    Функция для предсказания цифры

    Args:
        image_array: numpy массив (28, 28) со значениями 0-1

    Returns:
        predicted_digit, confidence
    """
    model.eval()

    # преобразование в тензор
    if image_array.max() > 1.0:
        image_array = image_array / 255.0

    image_tensor = torch.FloatTensor(image_array).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_digit = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_digit].item() * 100

    return predicted_digit, confidence

# пример использования
print("\nПример использования функции предсказания:")
test_image = test_images[0].squeeze().numpy()
digit, conf = predict_digit(test_image)
print(f"Предсказанная цифра: {digit}")
print(f"Уверенность: {conf:.2f}%")
print(f"Реальная цифра: {test_labels[0].item()}")

print("\nСохранение модели...")
torch.save(model.state_dict(), 'digit_recognition_pytorch.pth')
print("Модель сохранена в 'digit_recognition_pytorch.pth'")

# Для загрузки:
# model = DigitRecognizer()
# model.load_state_dict(torch.load('digit_recognition_pytorch.pth'))
# model.to(device)
# model.eval()

print("\n" + "="*60)
print("ОБУЧЕНИЕ ЗАВЕРШЕНО!")
print(f"Финальная точность: {test_accuracy * 100:.2f}%")
print("="*60)
