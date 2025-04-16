import psycopg2
import csv

def connect_db():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="22041983re", 
        host="localhost"
    )

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        );
    """)
    conn.commit()
    conn.close()

def create_csv_file():
    try:
        with open('phones.csv', 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['first_name', 'phone'])
    except FileExistsError:
        pass

def insert_from_csv():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        with open('phones.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cursor.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                    row
                )
        conn.commit()
        print("✅ Данные из CSV добавлены!")
    except FileNotFoundError:
        print("❌ Файл 'phones.csv' не найден!")
    finally:
        conn.close()

def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    conn.close()
    print(f"✅ Контакт '{name}' добавлен в базу данных!")
    try:
        with open('phones.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, phone])
        print(f"✅ Контакт '{name}' добавлен в файл phones.csv!")
    except Exception as e:
        print(f"❌ Ошибка при записи в CSV: {e}")

def update_data():
    user_id = input("Введите ID контакта: ")
    new_name = input("Новое имя (оставьте пустым, если не меняется): ")
    new_phone = input("Новый телефон (оставьте пустым, если не меняется): ")
    conn = connect_db()
    cursor = conn.cursor()
    if new_name:
        cursor.execute(
            "UPDATE phonebook SET first_name = %s WHERE id = %s",
            (new_name, user_id)
        )
    if new_phone:
        cursor.execute(
            "UPDATE phonebook SET phone = %s WHERE id = %s",
            (new_phone, user_id)
        )
    conn.commit()
    conn.close()
    print("✅ Данные обновлены!")

def delete_data():
    target = input("Удалить по имени (1) или телефону (2)? ")
    conn = connect_db()
    cursor = conn.cursor()
    if target == "1":
        name = input("Введите имя: ")
        cursor.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    else:
        phone = input("Введите телефон: ")
        cursor.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    conn.close()
    print("✅ Данные удалены!")

def query_data():
    search = input("Введите имя или телефон для поиска: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM phonebook WHERE first_name LIKE %s OR phone LIKE %s",
        (f"%{search}%", f"%{search}%")
    )
    results = cursor.fetchall()
    if results:
        print("\n🔍 Результаты поиска:")
        for row in results:
            print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    else:
        print("❌ Ничего не найдено.")
    conn.close()

def show_all_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phonebook ORDER BY id")
    results = cursor.fetchall()
    print("\n📋 Все сохранённые контакты:")
    for row in results:
        print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    conn.close()

def main():
    create_table()
    create_csv_file()
    while True:
        print("\n=== PhoneBook Manager ===")
        print("1. Добавить из CSV\n2. Добавить вручную\n3. Обновить\n4. Удалить\n5. Поиск\n6. Показать все\n7. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            query_data()
        elif choice == "6":
            show_all_contacts()
        elif choice == "7":
            print("Выход из программы.")
            break
        else:
            print("❌ Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
