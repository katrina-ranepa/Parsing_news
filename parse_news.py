import requests
from bs4 import BeautifulSoup
import json

# URL страницы с новостями
url = "https://web.archive.org/web/20230903112115/https://iz.ru/news"

# Получаем HTML страницы
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Словарь для хранения новостей по категориям
news_by_category = {}

# Ищем все новостные блоки
news_items = soup.find_all("div", class_="node__cart__item")

for item in news_items:
    # Извлекаем категорию
    category_div = item.find("div", class_="node__cart__item__category_news")
    if category_div:
        category_link = category_div.find("a")
        if category_link:
            category = category_link.get_text().strip()
        else:
            category = category_div.get_text().strip()

        # Извлекаем заголовок и ссылку
        title_div = item.find("div", class_="node__cart__item__inside__info__title")
        link_tag = item.find("a", href=True)

        if title_div and link_tag:
            title = title_div.get_text().strip()
            link = link_tag["href"]

            # Преобразуем относительную ссылку в абсолютную
            if link.startswith("/"):
                link = f"https://iz.ru{link}"

            # Добавляем новость в соответствующую категорию
            if category not in news_by_category:
                news_by_category[category] = []

            news_item = {"title": title, "link": link}

            # Проверяем на дубликаты
            if news_item not in news_by_category[category]:
                news_by_category[category].append(news_item)

# Выводим результат
print("Новости по категориям:")
print("=" * 60)

for category, news_list in news_by_category.items():
    print(f"\n{category.upper()}:")
    print("-" * 40)
    for i, news in enumerate(news_list, 1):
        print(f"{i}. {news['title']}")
        print(f"   🔗 {news['link']}")

# Сохраняем в JSON файл
with open("iz_news.json", "w", encoding="utf-8") as f:
    json.dump(news_by_category, f, ensure_ascii=False, indent=2)

# Статистика
total_categories = len(news_by_category)
total_news = sum(len(news_list) for news_list in news_by_category.values())

print(f"\n✅ Данные сохранены в iz_news.json")
print(f"📊 Статистика: {total_categories} категорий, {total_news} новостей")

# Дополнительная информация о категориях
print("\n📈 Категории и количество новостей:")
for category, news_list in news_by_category.items():
    print(f"   {category}: {len(news_list)} новостей")
