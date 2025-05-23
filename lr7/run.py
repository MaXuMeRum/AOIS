from main import *
import random
from typing import List

def create_random_grid(rows: int, cols: int) -> List[List[int]]:
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]

def print_binary_data(data: List[int], label: str) -> None:
    print(f"{label}{''.join(map(str, data)) if data else 'Нет данных'}")

def get_user_input(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Пожалуйста, введите число между {min_val} и {max_val}")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

def get_binary_input(length: int, prompt: str) -> List[int]:
    print(prompt, end='')
    user_input = input().strip()
    result = []
    for ch in user_input:
        if ch in '01':
            result.append(int(ch))
            if len(result) == length:
                break
    result += [0] * (length - len(result))
    return result

def show_menu() -> None:
    print("\n=== Операции с диагональной матрицей ===")
    print("1. Записать строку данных")
    print("2. Записать диагональные данные")
    print("3. Прочитать строку данных")
    print("4. Прочитать диагональные данные")
    print("5. Логическое ИЛИ")
    print("6. Логическое ИЛИ-НЕ")
    print("7. Операция копирования")
    print("8. Операция инверсии")
    print("9. Обработать ключевые поля")
    print("10. Найти ближайшие значения")
    print("11. Показать матрицу")
    print("12. Сгенерировать случайную матрицу")
    print("13. Выход")
    print("Введите ваш выбор (1-13): ", end='')

def main():
    grid_size = 16
    custom_grid = CustomDiagonalGrid(grid_size, grid_size)

    while True:
        show_menu()
        choice = get_user_input("", 1, 13)

        if choice == 13:
            print("Завершение программы.")
            break

        if choice == 1:
            start_r = get_user_input("Введите начальную строку (0-15): ", 0, 15)
            col = get_user_input("Введите столбец (0-15): ", 0, 15)
            length = get_user_input("Введите длину данных (1-16): ", 1, 16)
            data = get_binary_input(length, "Введите бинарные данные (например, 1101): ")
            custom_grid.store_data_row(data, start_r, col)
            print("Данные успешно записаны.")

        elif choice == 2:
            start_r = get_user_input("Введите начальную строку (0-15): ", 0, 15)
            start_c = get_user_input("Введите начальный столбец (0-15): ", 0, 15)
            length = get_user_input("Введите длину данных (1-16): ", 1, 16)
            data = get_binary_input(length, "Введите бинарные данные (например, 1101): ")
            custom_grid.store_diagonal_data(data, start_r, start_c)
            print("Диагональные данные успешно записаны.")

        elif choice == 3:
            start_r = get_user_input("Введите начальную строку (0-15): ", 0, 15)
            col = get_user_input("Введите столбец (0-15): ", 0, 15)
            length = get_user_input("Введите длину данных (1-16): ", 1, 16)
            data = custom_grid.fetch_data_row(start_r, col, length)
            print_binary_data(data, "Прочитанные данные: ")

        elif choice == 4:
            start_r = get_user_input("Введите начальную строку (0-15): ", 0, 15)
            start_c = get_user_input("Введите начальный столбец (0-15): ", 0, 15)
            length = get_user_input("Введите длину данных (1-16): ", 1, 16)
            data = custom_grid.fetch_diagonal_data(start_r, start_c, length)
            print_binary_data(data, "Диагональные данные: ")

        elif choice == 5:
            col1 = get_user_input("Введите первый столбец (0-15): ", 0, 15)
            col2 = get_user_input("Введите второй столбец (0-15): ", 0, 15)
            res_col = get_user_input("Введите столбец для результата (0-15): ", 0, 15)
            result = custom_grid.perform_logical_or(col1, col2, res_col)
            print_binary_data(result, "Результат ИЛИ: ")
            print(f"Результат записан в столбец {res_col}")

        elif choice == 6:
            col1 = get_user_input("Введите первый столбец (0-15): ", 0, 15)
            col2 = get_user_input("Введите второй столбец (0-15): ", 0, 15)
            res_col = get_user_input("Введите столбец для результата (0-15): ", 0, 15)
            result = custom_grid.perform_logical_nor(col1, col2, res_col)
            print_binary_data(result, "Результат ИЛИ-НЕ: ")
            print(f"Результат записан в столбец {res_col}")

        elif choice == 7:
            col1 = get_user_input("Введите исходный столбец (0-15): ", 0, 15)
            col2 = get_user_input("Введите фиктивный столбец (0-15): ", 0, 15)
            res_col = get_user_input("Введите столбец для результата (0-15): ", 0, 15)
            result = custom_grid.perform_copy_operation(col1, col2, res_col)
            print_binary_data(result, "Скопированные данные: ")
            print(f"Результат записан в столбец {res_col}")

        elif choice == 8:
            col1 = get_user_input("Введите исходный столбец (0-15): ", 0, 15)
            col2 = get_user_input("Введите фиктивный столбец (0-15): ", 0, 15)
            res_col = get_user_input("Введите столбец для результата (0-15): ", 0, 15)
            result = custom_grid.perform_invert_operation(col1, col2, res_col)
            print_binary_data(result, "Инвертированные данные: ")
            print(f"Результат записан в столбец {res_col}")

        elif choice == 9:
            key_data = get_binary_input(3, "Введите 3-битный ключ (например, 101): ")
            custom_grid.process_key_fields(key_data)

        elif choice == 10:
            target = input("Введите целевое значение (16 бит): ").strip()
            target_data = []
            for ch in target:
                if ch in '01':
                    target_data.append(int(ch))
                else:
                    print("Неверный ввод - будут использованы нули")
                    target_data = [0] * 16
                    break
            target_data += [0] * (16 - len(target_data))
            target_data = target_data[:16]

            below_col, below_val, above_col, above_val = custom_grid.find_closest_values(target_data)

            print("Ближайшее снизу:", end=' ')
            if below_col is None:
                print("Не найдено")
            else:
                print(f"Столбец {below_col}: {''.join(map(str, below_val))}")

            print("Ближайшее сверху:", end=' ')
            if above_col is None:
                print("Не найдено")
            else:
                print(f"Столбец {above_col}: {''.join(map(str, above_val))}")

        elif choice == 11:
            print("Текущая матрица:")
            custom_grid.display_grid()

        elif choice == 12:
            random_data = create_random_grid(16, 16)
            for col in range(16):
                column_data = [random_data[row][col] for row in range(16)]
                custom_grid.store_data_row(column_data, 0, col)
            print("Случайная матрица создана и сохранена.")
            custom_grid.display_grid()

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()