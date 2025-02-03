from pprint import pprint
import csv
import re


def normalize_phone(phone):
    phone_pattern = (r'(\+7|8)?[\(\s]*(\d{3})[\)\s-]*(\d{3})[-\s]*(\d{2})[-\s]*'
                     r'(\d{2})\s*\(?((\w+\.?)\s*(\d+)\)?)?')
    phone = phone.strip()
    match = re.search(phone_pattern, phone)
    if match:
        groups = match.groups()
        if groups[6] and groups[7]:
            phone_pattern_subst = r'+7(\2)\3-\4-\5 \7\8'
        else:
            phone_pattern_subst = r'+7(\2)\3-\4-\5'
        phone = re.sub(phone_pattern, phone_pattern_subst, phone)
    else: phone = ''
    return phone

def merge_duplicates(contacts):
    result = {}
    for contact in contacts:
        # Используем кортеж из lastname, firstname и surname в качестве ключа
        key = (contact[0], contact[1], contact[2])
        if key not in result:
            result[key] = contact
        else:
            # Объединяем информацию, сохраняя наиболее полные данные
            for i in range(len(contact)):
                if contact[i] and not result[key][i]:
                    result[key][i] = contact[i]
    return list(result.values())

# Чтение CSV файла
with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
    # pprint(contacts_list)

# Обработка данных
processed_contacts = []
for contact in contacts_list[1:]:  # Пропускаем заголовок
    # Обработка ФИО
    full_name = ' '.join(contact[:3]).split()
    lastname = full_name[0] if full_name[0] else ''
    firstname = full_name[1] if len(full_name) > 1 else ''
    surname = full_name[2] if len(full_name) > 2 else ''

    # Нормализация телефона
    phone = normalize_phone(contact[5]) if len(contact) > 5 else ''

    # Формирование обработанной записи
    processed_contact = [
        lastname, firstname, surname,  # Ф.И.О
        contact[3] if len(contact) > 3 else '',  # organization
        contact[4] if len(contact) > 4 else '',  # position
        phone,
        contact[6].lower() if len(contact) > 6 else ''  # email
    ]
    processed_contacts.append(processed_contact)
    # pprint(processed_contacts)

# Объединение дубликатов
final_contacts = merge_duplicates(processed_contacts)
# pprint(final_contacts)

# Добавление заголовка
final_contacts.insert(0, contacts_list[0])
print()
print('Обработка завершена. Результат:')
pprint(final_contacts)

# Запись результата в новый CSV файл
with open('phonebook.csv', 'w', encoding = 'utf-8', newline = '') as f:
    datawriter = csv.writer(f, delimiter = ',')
    datawriter.writerows(final_contacts)

print('Результат сохранен в файл \'phonebook.csv\'.')