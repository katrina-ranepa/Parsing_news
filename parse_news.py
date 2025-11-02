import requests
from bs4 import BeautifulSoup
import json


class NewsParser:

    def __init__(self):
        self.URL = "https://web.archive.org/web/20230903112115/https://iz.ru/news"
        self.ERROR_MESSAGE = "Error loading page!"
        self.news_data = self.__parse_news_page()

    def __parse_news_page(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        }

        try:
            response = requests.get(self.URL, headers=headers, timeout=10)
            if response.status_code != 200:
                return {"Error": self.ERROR_MESSAGE}

        except requests.exceptions.RequestException as e:
            return {"Error": str(e)}

        soup = BeautifulSoup(response.text, "html.parser")
        news_by_category = {}

        # Основные категории для поиска
        categories = [
            "Общество",
            "Политика",
            "Экономика",
            "Спорт",
            "Здоровье",
            "Культура",
        ]

        for category in categories:
            news_list = self.__find_news_by_category(soup, category)
            if news_list:
                news_by_category[category] = news_list

        return news_by_category

    def __find_news_by_category(self, soup, category):
        news_list = []

        # Ищем элементы, связанные с категорией
        elements = soup.find_all(
            class_=lambda x: x and category.lower() in str(x).lower()
        )

        for element in elements:
            # Ищем новости внутри элемента категории
            links = element.find_all("a", href=lambda x: x and "/news/" in x)

            for link in links:
                title = link.get_text().strip()
                href = link.get("href")

                if title and len(title) > 15:
                    full_url = (
                        href if href.startswith("http") else f"https://iz.ru{href}"
                    )

                    news_list.append({"title": title, "link": full_url})

        return news_list[:5]  # Ограничиваем количество


if __name__ == "__main__":
    parser = NewsParser()

    print("Новости с Iz.ru:")
    print("=" * 60)

    for category, news_list in parser.news_data.items():
        print(f"\n{category}:")
        print("-" * 40)
        for i, news in enumerate(news_list, 1):
            print(f"{i}. {news['title']}")
            print(f"   Ссылка: {news['link']}")

    # Сохраняем в JSON
    with open("iz_news.json", "w", encoding="utf-8") as f:
        json.dump(parser.news_data, f, ensure_ascii=False, indent=2)
    print("\n✅ Данные сохранены в iz_news.json")
