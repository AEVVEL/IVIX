import csv


def save_to_csv(data, filename='crypto_data.csv'):
    if not data:
        return

    headers = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
