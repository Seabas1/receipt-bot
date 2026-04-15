import random

# Разделяем товары по категориям для разнообразия
GROCERY = [
    "МОЛОКО 2.5% 0.9Л", "ХЛЕБ ПШЕНИЧНЫЙ", "БАНАНЫ 1КГ", "ГРЕЧКА 900Г",
    "ЯЙЦО КУРИНОЕ С1", "СЫР РОССИЙСКИЙ", "ПАКЕТ-МАЙКА", "МАСЛО СЛИВ. 82%",
    "ВОДА ГАЗ. 1.5Л", "САХАР-ПЕСОК 1КГ", "СМЕТАНА 15% 200Г", "ШОКОЛАД МОЛОЧН."
]

CAFE_MENU = [
    "ЧИКЕНБУРГЕР", "КАРТОФЕЛЬ ФРИ СТАНД", "КОФЕ КАПУЧИНО 0.3", "НАГГЕТСЫ 6ШТ",
    "СОУС СЫРНЫЙ", "ПИЦЦА ПЕППЕРОНИ", "СЭНДВИЧ С ВЕТЧИНОЙ", "ЧАЙ ЗЕЛЕНЫЙ 0.4",
    "МОРОЖЕНОЕ РОЖОК", "КОКА-КОЛА 0.5Л", "ДОБРЫЙ КОЛА 0.5", "БОРЩ С ГОВЯДИНОЙ"
]

# Специфические сокращения (как в 1С или кассовых аппаратах)
ABBREVIATIONS = ["ОХЛ.", "ЗАМ.", "В/С", "СТ.", "Б/Г", "П/Ф", "ТУ", "АКЦИЯ"]

def generate_price():
    base = random.randint(35, 1200)
    cents = random.choice(["00", "50", "90", "99"])
    # Разные форматы цен в чеках
    return random.choice([f"{base}.{cents}", f"{base},{cents}", f"{base}"])

def generate_extensive_list(filename, count=7000):
    all_items = GROCERY + CAFE_MENU
    
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(count):
            item = random.choice(all_items)
            
            # В 30% случаев добавляем техническое сокращение
            if random.random() > 0.7:
                item = f"{item} {random.choice(ABBREVIATIONS)}"
            
            price = generate_price()
            
            # Выбираем стиль разделителя (чек - это всегда выравнивание)
            # 1. Точки (Блюдо........100.00)
            # 2. Пробелы (Блюдо        100.00)
            # 3. Количество + цена (Блюдо 1.000 x 100.00)
            
            style = random.random()
            if style < 0.4:
                sep = "." * random.randint(5, 15)
                line = f"{item}{sep}{price}"
            elif style < 0.8:
                sep = " " * random.randint(4, 12)
                line = f"{item}{sep}{price}"
            else:
                # Сложный формат: Кол-во * Цена
                qty = random.choice(["1", "2", "1.000", "0.542"])
                line = f"{item} {qty} x {price}"
                
            f.write(line + "\n")

generate_extensive_list('data/products.txt', count=7000)
print("Чистый список товаров (без названий магазинов) готов!")