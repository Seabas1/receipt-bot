from iftg.generators import BatchesImagesGenerator
from iftg.noises import (
    RandomBlurNoise, RandomBrightnessNoise, RandomPixelDropoutNoise,
    RandomShadowNoise, RandomElasticNoise, RandomRotationNoise,
    RandomGaussianNoise
)
import os

# ПРАВИЛЬНЫЙ путь к файлу с текстами
file_path = r"C:\Users\Егор\Desktop\Receipt_bot\texts.txt"

# Проверяем, существует ли файл
if not os.path.exists(file_path):
    print(f"Файл не найден: {file_path}")
    print("Создаю файл с тестовыми данными...")

    test_content = """Молоко 89.99
Хлеб бородинский 54.50
Сыр Российский 349.90
Колбаса Докторская 499.00
Масло сливочное 129.99"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    print("Файл создан!")

# Загружаем тексты
with open(file_path, 'r', encoding='utf-8') as f:
    texts = [line.strip() for line in f.readlines() if line.strip()]

print(f"Загружено {len(texts)} позиций")

# Разбиваем на батчи
batches = [texts[i::5] for i in range(5)]

# Настройка шумов для каждого батча
noises_configs = [
    [RandomBlurNoise(), RandomBrightnessNoise()],
    [RandomPixelDropoutNoise(), RandomShadowNoise()],
    [RandomElasticNoise(), RandomRotationNoise()],
    [RandomGaussianNoise(), RandomBlurNoise(), RandomBrightnessNoise()],
    [RandomShadowNoise(), RandomPixelDropoutNoise(), RandomElasticNoise()]
]

# ПУТИ К ШРИФТАМ (стандартные шрифты Windows)
# Выберите один из вариантов:

# Вариант 1: Arial
font_path = r"C:\Windows\Fonts\arial.ttf"

# Вариант 2: Times New Roman (если Arial не подойдёт)
# font_path = r"C:\Windows\Fonts\times.ttf"

# Вариант 3: Calibri
# font_path = r"C:\Windows\Fonts\calibri.ttf"

# Проверяем существование шрифта
if not os.path.exists(font_path):
    print(f"Шрифт не найден: {font_path}")
    # Попробуем найти любой шрифт
    possible_fonts = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\cour.ttf"
    ]
    for f in possible_fonts:
        if os.path.exists(f):
            font_path = f
            print(f"Найден шрифт: {font_path}")
            break

# Пути для сохранения результатов
output_path = r"C:\Users\Егор\Desktop\Receipt_bot\dataset"

# Создаём папки
os.makedirs(output_path, exist_ok=True)
os.makedirs(os.path.join(output_path, 'images'), exist_ok=True)
os.makedirs(os.path.join(output_path, 'labels'), exist_ok=True)

# Генерация
print("Начинаю генерацию...")
print(f"Использую шрифт: {font_path}")
print(f"Сохраняю в: {output_path}")

try:
    results = BatchesImagesGenerator(
        texts=batches,
        font_paths=[font_path] * 5,
        noises=noises_configs,
        font_sizes=[32, 36, 40, 44, 48],
        font_colors=['black'] * 5,
        background_colors=['white'] * 5,
        margins=[(10, 10, 10, 10)] * 5,
        dpi=[(300, 300)] * 5,
        img_names=['receipt_batch1', 'receipt_batch2', 'receipt_batch3', 'receipt_batch4', 'receipt_batch5'],
        img_formats=['.png'] * 5,
        img_output_paths=[os.path.join(output_path, 'images')] * 5,
        txt_names=['labels_batch1', 'labels_batch2', 'labels_batch3', 'labels_batch4', 'labels_batch5'],
        txt_formats=['.txt'] * 5,
        txt_output_paths=[os.path.join(output_path, 'labels')] * 5
    )

    results.generate_batches(is_with_label=True)
    print("Генерация завершена успешно!")
    print(f"Результаты сохранены в {output_path}")

except Exception as e:
    print(f"Ошибка при генерации: {e}")

    # Альтернативный простой способ без батчей
    print("\nПробую упрощённый способ генерации...")
    from iftg.generators import ImagesGenerator

    simple_generator = ImagesGenerator(
        texts=texts[:20],  # берём первые 20 для теста
        font_path=font_path,
        noises=[RandomBlurNoise(), RandomBrightnessNoise()],
        font_size=40,
        font_color='black',
        background_color='white',
        margin=(10, 10, 10, 10),
        dpi=(300, 300),
        img_name='test_receipt',
        img_format='.png',
        img_output_path=os.path.join(output_path, 'images'),
        txt_name='test_labels',
        txt_format='.txt',
        txt_output_path=os.path.join(output_path, 'labels')
    )

    simple_generator.generate_images_with_text()
    print("Упрощённая генерация завершена!")