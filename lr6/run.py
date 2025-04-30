from main import *

if __name__ == "__main__":
    capacity = 20
    hash_table = HashTable(capacity)

    while True:
        print("\nВыберите действие:")
        print("1. Вставить элемент (ключ, данные)")
        print("2. Найти элемент (ключ)")
        print("3. Удалить элемент (ключ)")
        print("4. Показать хеш-таблицу")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            key = input("Введите ключ: ")
            data = input("Введите данные: ")
            try:
                hash_table.insert(key, data)
                print(f"Элемент с ключом '{key}' успешно вставлен.")
            except OverflowError as e:
                print(e)
        elif choice == '2':
            key = input("Введите ключ для поиска: ")
            result = hash_table.get(key)
            if result is not None:
                print(f"Найден элемент: {key} -> {result}")
            else:
                print(f"Элемент с ключом '{key}' не найден.")
        elif choice == '3':
            key = input("Введите ключ для удаления: ")
            if hash_table.delete(key):
                print(f"Элемент с ключом '{key}' успешно удален.")
            else:
                print(f"Элемент с ключом '{key}' не найден.")
        elif choice == '4':
            hash_table.display_table()
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из списка.")