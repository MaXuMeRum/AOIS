from main import *

# Функция для ввода термов пользователем
def input_terms():
    terms = []
    print("Введите термы (каждый терм — строка из 0, 1 или X). Введите 'q' для завершения.")
    while True:
        term = input(f"Терм {len(terms) + 1}: ").strip()
        if term.lower() == 'q':
            break
        terms.append(list(term))
    return terms

# Основная программа
def main():
    print("Выберите тип формы для минимизации:")
    print("1. DNF (Дизъюнктивная нормальная форма)")
    print("2. CNF (Конъюнктивная нормальная форма)")
    choice = input("Введите номер (1 или 2): ").strip()

    if choice == '1':
        print("Введите термы для DNF:")
        terms = input_terms()
        minimized_terms = minimize_form_calculational(terms)
        print("Минимизированная DNF (расчетный метод):", minimized_terms)
    elif choice == '2':
        print("Введите термы для CNF:")
        terms = input_terms()
        print("Выберите метод минимизации CNF:")
        print("1. Расчетный метод")
        print("2. Табличный метод")
        method_choice = input("Введите номер (1 или 2): ").strip()
        if method_choice == '1':
            minimized_terms = minimize_form_calculational(terms)
            print("Минимизированная CNF (расчетный метод):", minimized_terms)
        elif method_choice == '2':
            minimized_terms = minimize_cnf_tabular(terms)
            print("Минимизированная CNF (табличный метод):", minimized_terms)
        else:
            print("Неверный выбор метода.")
    else:
        print("Неверный выбор типа формы.")

# Запуск программы
if __name__ == "__main__":
    main()