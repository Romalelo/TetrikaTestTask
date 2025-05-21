"""
Скрипт собирает данные с русскоязычной Википедии по категории "Животные по алфавиту"
и сохраняет в CSV-файл количество записей на каждую букву алфавита.
"""

import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"
OUTPUT_CSV = "task2/beasts.csv"


def get_animals_by_letter_counts():
    """
    Обходит страницы категории "Животные по алфавиту" на Википедии и подсчитывает
    количество записей (животных, родов и пр.) на каждую букву русского алфавита.

    :return: dict: Словарь, где ключ — заглавная буква русского алфавита, значение — количество записей.
    """
    url = START_URL
    counts = {}

    while url:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        all_items = soup.select(".mw-category-group ul li a")

        if not all_items:
            print("Ничего не найдено на странице. Возможно, изменилась структура.")
            break

        for item in all_items:
            title = item.get_text()
            if title:
                first_letter = title[0].upper()
                if "А" <= first_letter <= "Я":
                    if first_letter not in counts:
                        counts[first_letter] = 0
                    counts[first_letter] += 1

        next_link = soup.find("a", string="Следующая страница")
        if next_link:
            url = BASE_URL + next_link["href"]
        else:
            url = None

    return counts


def write_counts_to_csv(counts, filename):
    """
    Записывает статистику количества животных на каждую букву в CSV-файл.

    Аргументы:
        counts (dict): Словарь с буквами и соответствующими количествами.
        filename (str): Путь к выходному CSV-файлу.
    """
    try:
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            for letter in sorted(counts):
                writer.writerow([letter, counts[letter]])
        print(f"CSV записан: {filename}")
    except Exception as e:
        print(f"Ошибка записи CSV: {e}")


if __name__ == "__main__":
    counts = get_animals_by_letter_counts()
    if counts:
        write_counts_to_csv(counts, OUTPUT_CSV)
        print(f"Успешно! Результат сохранён в {OUTPUT_CSV}")
    else:
        print("Не удалось получить данные.")
