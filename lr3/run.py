from main import *

def main():
    print("Программа для минимизации логических функций")
    print("------------------------------------------")

    # Ввод количества переменных
    while True:
        try:
            variables_count = int(input("Введите количество переменных (2-4): "))
            if 2 <= variables_count <= 4:
                break
            print("Пожалуйста, введите число от 2 до 4")
        except ValueError:
            print("Ошибка: введите целое число")

    # Генерация имен переменных
    variables = [chr(97 + i) for i in range(variables_count)]  # a, b, c, ...

    # Ввод СКНФ
    print("\nВвод СКНФ (конъюнкция дизъюнктов):")
    sknf_terms = input_terms(variables_count)

    # Ввод СДНФ
    print("\nВвод СДНФ (дизъюнкция конъюнктов):")
    sdnf_terms = input_terms(variables_count)

    # Выполнение минимизаций
    if sknf_terms:
        minimize_sknf_calculation(variables, sknf_terms)
        minimize_sknf_table(variables, sknf_terms)

    if sdnf_terms:
        minimize_sdnf_calculation(variables, sdnf_terms)


if __name__ == "__main__":
    main()