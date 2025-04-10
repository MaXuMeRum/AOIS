from main import *

def print_matrix(matrix):
    for row in matrix:
        print(row)


def main():
    print("Создание матрицы")
    rows = int(input("Введите количество строк: ") or 8)
    cols = int(input("Введите количество столбцов: ") or 8)

    dm = DiagonalMatrix(rows, cols)

    print("\nАвтоматически сгенерированная матрица:")
    print_matrix(dm.matrix)

    while True:
        print("\nМеню:")
        print("1. Показать матрицу")
        print("2. Показать разрядный столбец")
        print("3. Логические операции (f1 и f14)")
        print("4. Логические операции (f3 и f12)")
        print("5. Поиск значения сверху/снизу")
        print("6. Сложение полей Aj и Bj для заданного Vj")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nМатрица:")
            print_matrix(dm.matrix)



        elif choice == "2":

            col = int(input(f"Введите номер столбца (0-{dm.cols - 1}): "))

            bit_pos = int(input(f"Введите номер бита (0-{dm.rows - 1}): "))

            bit_column = dm.get_bit_column(col, bit_pos)

            if bit_column is not None:
                print(f"Разрядный столбец {col} для бита {bit_pos}:")

                print(bit_column)

        elif choice == "3":
            col1 = int(input(f"Введите первый столбец (0-{dm.cols - 1}): "))
            col2 = int(input(f"Введите второй столбец (0-{dm.cols - 1}): "))
            and_res, or_res = dm.logical_f1_f14(col1, col2)
            if and_res is not None and or_res is not None:
                print("Результат И (f1):", and_res)
                print("Результат ИЛИ (f14):", or_res)

        elif choice == "4":
            col1 = int(input(f"Введите первый столбец (0-{dm.cols - 1}): "))
            col2 = int(input(f"Введите второй столбец (0-{dm.cols - 1}): "))
            nand_res, nor_res = dm.logical_f3_f12(col1, col2)
            if nand_res is not None and nor_res is not None:
                print("Результат И-НЕ (f3):", nand_res)
                print("Результат ИЛИ-НЕ (f12):", nor_res)

        elif choice == "5":
            col = int(input(f"Введите столбец (0-{dm.cols - 1}): "))
            row = int(input(f"Введите строку (0-{dm.rows - 1}): "))
            value = int(input("Введите искомое значение: "))
            print(f"Поиск значения {value}:")
            above = dm.search_above(col, row, value)
            below = dm.search_below(col, row, value)
            print(f"Ближайшее сверху от ({row},{col}):", above)
            print(f"Ближайшее снизу от ({row},{col}):", below)

        elif choice == "6":
            v_value = int(input("Введите значение Vj (0-7): "))
            if 0 <= v_value <= 7:
                results = dm.add_fields_with_condition(v_value)
                print(f"\nСложение Aj и Bj для слов с Vj = {v_value}:")
                for res in results:
                    print(f"Позиция ({res[0]},{res[1]}): Aj={res[2]}, Bj={res[3]}, сумма={res[4]}")
            else:
                print("Ошибка: значение Vj должно быть от 0 до 7")

        elif choice == "0":
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()