from main import *

def main():
    expression = input("Введите логическую функцию: ")
    variables = sorted(set(re.findall(r'[a-e]', expression)))

    print("\nПеременные:", variables)
    table = generate_truth_table(variables, expression)

    print("\nТаблица истинности:")
    print_table(table, variables)

    sdnf, sknf, sdnf_nums, sknf_nums = build_sdnf_sknf(table, variables)
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
    print(sdnf)
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
    print(sknf)

    print("\nЧисловые формы:")
    print(f"({', '.join(map(str, sdnf_nums))}) ∧")
    print(f"({', '.join(map(str, sknf_nums))}) ∨")

    index_form = compute_index_form(table)
    print("\nИндексная форма:")
    print(index_form)


if __name__ == "__main__":
    main()

