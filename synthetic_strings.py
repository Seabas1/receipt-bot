import os
import random
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.ndimage import map_coordinates

class ReceiptSyntheticGenerator:
    def __init__(self, products_file, fonts_dir, output_dir):
        self.output_dir = output_dir
        self.fonts_dir = fonts_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Загрузка названий продуктов
        with open(products_file, 'r', encoding='utf-8') as f:
            self.products = [line.strip() for line in f if line.strip()]
            
        # Загрузка путей к шрифтам
        self.fonts = [os.path.join(fonts_dir, f) for f in os.listdir(fonts_dir) 
                      if f.endswith(('.ttf', '.otf'))]
        
        if not self.fonts:
            raise Exception(f"Шрифты не найдены в папке {fonts_dir}")

    # --- ГЕОМЕТРИЧЕСКИЕ ИСКАЖЕНИЯ ---
    def _apply_curve(self, img_np):
        """Имитация изгиба чека"""
        rows, cols = img_np.shape[:2]
        intensity = random.uniform(0.05, 0.12)
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))
        offset = intensity * rows * np.sin(2 * np.pi * x / (cols * 1.5))
        distorted_y = y + offset
        coords = np.vstack((distorted_y.flatten(), x.flatten()))
        distorted_img = map_coordinates(img_np, coords, order=1, mode='reflect')
        return distorted_img.reshape(rows, cols)

    def _apply_perspective(self, img_np):
        """Легкий наклон камеры"""
        rows, cols = img_np.shape[:2]
        pts1 = np.float32([[0,0], [cols,0], [0,rows], [cols,rows]])
        d = random.randint(3, 8)
        pts2 = np.float32([
            [random.randint(0,d), random.randint(0,d)],
            [cols-random.randint(0,d), random.randint(0,d)],
            [random.randint(0,d), rows-random.randint(0,d)],
            [cols-random.randint(0,d), rows-random.randint(0,d)]
        ])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        return cv2.warpPerspective(img_np, matrix, (cols, rows), borderValue=255)

    def _apply_shadow(self, img_np):
        """Неравномерное освещение"""
        img_np = img_np.astype(np.float32)
        rows, cols = img_np.shape[:2]
        # Градиент от 0.7 (тень) до 1.0 (свет)
        light_map = np.tile(np.linspace(random.uniform(0.7, 0.9), 1.0, cols), (rows, 1))
        if random.choice([True, False]): # Случайное направление тени
            light_map = np.fliplr(light_map)
        return np.clip(img_np * light_map, 0, 255).astype(np.uint8)

    # --- ГЕНЕРАЦИЯ СТРОКИ ---
    def create_sample(self, index):
        # Составляем текст чека
        product = random.choice(self.products)
        price = f"{random.randint(50, 2000)}.{random.choice(['00', '50', '90', '99'])}"
        
        # Имитируем заполнение точками или пробелами как в реальном чеке
        padding = "." * random.randint(3, 15)
        text = f"{product}{padding}{price}"

        # 1. Отрисовка текста (Pillow)
        width, height = 800, 100
        bg_color = random.randint(240, 255)
        img = Image.new('L', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        font_path = random.choice(self.fonts)
        font_size = random.randint(28, 38)
        font = ImageFont.truetype(font_path, font_size)
        
        # Рисуем текст в центре
        draw.text((30, 25), text, font=font, fill=random.randint(0, 70))
        
        # 2. Обработка OpenCV
        img_np = np.array(img)
        
        # Применяем эффекты в случайном порядке
        if random.random() > 0.4:
            img_np = self._apply_curve(img_np)
        
        img_np = self._apply_perspective(img_np)
        img_np = self._apply_shadow(img_np)
        
        # Размытие и шум
        if random.random() > 0.5:
            img_np = cv2.GaussianBlur(img_np, (3, 3), 0)
        
        # Добавляем соль и перец (шум)
        noise = np.random.randint(0, 15, img_np.shape, dtype='uint8')
        img_np = cv2.add(img_np, noise)

        # 3. Сохранение
        file_name = f"receipt_line_{index}.png"
        cv2.imwrite(os.path.join(self.output_dir, file_name), img_np)
        
        return file_name, text

# --- ЗАПУСК ---
if __name__ == "__main__":
    config = {
        "products_file": "data/products.txt",
        "fonts_dir": "fonts",
        "output_dir": "data/synthetic/string"
    }

    generator = ReceiptSyntheticGenerator(**config)
    
    num_samples = 1000 # Сколько картинок создать
    labels_path = os.path.join(config["output_dir"], "labels.txt")
    
    print(f"Начинаю генерацию {num_samples} образцов...")
    
    with open(labels_path, "w", encoding="utf-8") as f:
        for i in range(num_samples):
            try:
                fname, label = generator.create_sample(i)
                f.write(f"{fname}\t{label}\n")
                if i % 100 == 0:
                    print(f"Создано {i}...")
            except Exception as e:
                print(f"Ошибка на итерации {i}: {e}")

    print(f"Готово! Данные и файл разметки сохранены в {config['output_dir']}")