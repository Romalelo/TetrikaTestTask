import csv
from solution import write_counts_to_csv


def test_write_counts_to_csv(tmp_path):
    # Подготовка тестового словаря
    test_counts = {
        'А': 3,
        'Б': 2,
        'В': 1
    }

    # Путь к временному CSV-файлу
    csv_file = tmp_path / "test_beasts.csv"

    # Вызов функции записи
    write_counts_to_csv(test_counts, csv_file)

    # Получение содержимого файла
    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['А', '3'],
        ['Б', '2'],
        ['В', '1']
    ]

    assert rows == expected_rows
