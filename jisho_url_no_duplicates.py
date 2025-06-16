from collections import defaultdict

# Замените 'links.txt' на путь к вашему файлу
input_file = 'C:\\Users\\sheshulin\\Downloads\\jisho_urls_all.txt'
unique_file = 'jisho_urls_all_unique_links.txt'
duplicates_file = 'jisho_urls_all_duplicate_links.txt'

# Читаем ссылки из файла
with open(input_file, 'r') as file:
    links = file.readlines()

# Удаляем пробелы и символы новой строки
links = [link.strip() for link in links]

# Группируем ссылки
link_counts = defaultdict(list)
for index, link in enumerate(links):
    link_counts[link].append(index)

# Разделяем уникальные ссылки и повторы
unique_links = []
duplicate_links = []

for link, indices in link_counts.items():
    unique_links.append(link)  # Оставляем одну копию в уникальных
    if len(indices) > 1:
        duplicate_links.extend([link] * (len(indices) - 1))  # Добавляем остальные в дубликаты

# Сохраняем уникальные ссылки в файл
with open(unique_file, 'w') as file:
    for link in unique_links:
        file.write(link + '\n')

# Сохраняем повторы в файл
with open(duplicates_file, 'w') as file:
    for link in duplicate_links:
        file.write(link + '\n')

print(f'Уникальные ссылки сохранены в {unique_file}.')
print(f'Повторяющиеся ссылки сохранены в {duplicates_file}.')
