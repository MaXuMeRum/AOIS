from main import *

def input_terms(variables, form_type):
    """Функция для ввода термов пользователем"""
    print(f"\nВведите термы для {form_type} (по одному терму в строке, {len(variables)} цифр 0 или 1)")
    print("Пример: 011 для ¬a b c")
    print("Введите 'end' для завершения ввода")

    terms = []
    while True:
        term_str = input(f"Терм {len(terms) + 1}: ").strip()
        if term_str.lower() == 'end':
            break
        if len(term_str) != len(variables):
            print(f"Ошибка: терм должен содержать ровно {len(variables)} цифр")
            continue
        if not all(c in '01' for c in term_str):
            print("Ошибка: терм должен содержать только 0 и 1")
            continue

        term = tuple(int(c) for c in term_str)
        terms.append(term)

    return terms


def main():
    print("Минимизация СКНФ и СДНФ")

    # Ввод переменных
    variables = input("Введите переменные (например, a b c): ").split()
    if not variables:
        print("Используются переменные по умолчанию: a b c")
        variables = ['a', 'b', 'c']

    minimizer = Minimizer(variables)

    while True:
        print("\nМеню:")
        print("1. Минимизация СДНФ")
        print("2. Минимизация СКНФ")
        print("3. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            terms = input_terms(variables, "СДНФ")
            if not terms:
                print("Не введены термы для минимизации")
                continue

            print_header("Минимизация СДНФ расчетным методом")
            minimizer.calculate_method(terms, is_dnf=True)

            print_header("Минимизация СДНФ расчетно-табличным методом")
            minimizer.table_method(terms, is_dnf=True)

            print_header("Минимизация СДНФ табличным методом (Карта Карно)")
            minimizer.karnaugh_method(terms, is_dnf=True)

        elif choice == '2':
            terms = input_terms(variables, "СКНФ")
            if not terms:
                print("Не введены термы для минимизации")
                continue

            print_header("Минимизация СКНФ расчетным методом")
            minimizer.calculate_method(terms, is_dnf=False)

            print_header("Минимизация СКНФ расчетно-табличным методом")
            minimizer.table_method(terms, is_dnf=False)

            print_header("Минимизация СКНФ табличным методом (Карта Карно)")
            minimizer.karnaugh_method(terms, is_dnf=False)

        elif choice == '3':
            break
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    main()