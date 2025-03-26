def input_terms(variables_count):
    """Функция для ввода термов от пользователя"""
    terms = []
    print(f"Введите термы (используйте {variables_count} переменных, например, 'a∨b∨¬c'):")
    while True:
        term = input("Введите терм (или пустую строку чтобы закончить): ").strip()
        if not term:
            break
        terms.append(term)
    return terms


def minimize_sknf_calculation(variables, terms):
    """Минимизация СКНФ расчетным методом"""
    print("\n1. Минимизация СКНФ расчетным методом")
    print(f"Исходная СКНФ: {' ∧ '.join(terms)}")

    # Этап склеивания
    print("\nЭтап склеивания:")
    new_terms = []
    n = len(variables)

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            # Находим общие переменные в скобках
            diff = 0
            common = []
            for v in variables:
                vi = v in terms[i].split('∨')
                vj = v in terms[j].split('∨')
                if vi != vj:
                    diff += 1
                    if diff > 1:
                        break
                elif vi and vj:
                    common.append(v)

            if diff == 1:
                new_term = '∨'.join(common)
                print(f"{terms[i]} ∨ {terms[j]} => {new_term}")
                if new_term not in new_terms:
                    new_terms.append(new_term)

    print("\nРезультат после склеивания:")
    print(' ∧ '.join(new_terms) if new_terms else "Невозможно минимизировать дальше")

    # Проверка на лишние импликанты
    print("\nПроверка на лишние импликанты:")
    essential = []
    for term in new_terms:
        print(f"Проверяем {term}:")
        temp = [t for t in new_terms if t != term]
        if not temp:
            essential.append(term)
            continue

        # Проверяем покрытие
        covered = True
        for t in terms:
            if not any(all(v in t.split('∨') for v in et.split('∨')) for et in temp):
                covered = False
                break

        if not covered:
            essential.append(term)
            print(f"Импликанта {term} необходима")
        else:
            print(f"Импликанта {term} лишняя")

    print("\nМинимизированная СКНФ:")
    print(' ∧ '.join(essential) if essential else "Не удалось минимизировать")


def minimize_sdnf_calculation(variables, terms):
    """Минимизация СДНФ расчетным методом"""
    print("\n2. Минимизация СДНФ расчетным методом")
    print(f"Исходная СДНФ: {' ∨ '.join(terms)}")

    # Этап склеивания
    print("\nЭтап склеивания:")
    new_terms = []
    n = len(variables)

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            # Находим общие переменные в скобках
            diff = 0
            common = []
            for v in variables:
                vi = v in terms[i].split('∧')
                vj = v in terms[j].split('∧')
                if vi != vj:
                    diff += 1
                    if diff > 1:
                        break
                elif vi and vj:
                    common.append(v)

            if diff == 1:
                new_term = '∧'.join(common)
                print(f"{terms[i]} ∧ {terms[j]} => {new_term}")
                if new_term not in new_terms:
                    new_terms.append(new_term)

    print("\nРезультат после склеивания:")
    print(' ∨ '.join(new_terms) if new_terms else "Невозможно минимизировать дальше")

    # Проверка на лишние импликанты
    print("\nПроверка на лишние импликанты:")
    essential = []
    for term in new_terms:
        print(f"Проверяем {term}:")
        temp = [t for t in new_terms if t != term]
        if not temp:
            essential.append(term)
            continue

        # Проверяем покрытие
        covered = True
        for t in terms:
            if not any(all(v in t.split('∧') for v in et.split('∧')) for et in temp):
                covered = False
                break

        if not covered:
            essential.append(term)
            print(f"Импликанта {term} необходима")
        else:
            print(f"Импликанта {term} лишняя")

    print("\nМинимизированная СДНФ:")
    print(' ∨ '.join(essential) if essential else "Не удалось минимизировать")


def minimize_sknf_table(variables, terms):
    """Минимизация СКНФ расчетно-табличным методом"""
    print("\n3. Минимизация СКНФ расчетно-табличным методом")
    print(f"Исходная СКНФ: {' ∧ '.join(terms)}")

    # Этап склеивания
    print("\nЭтап склеивания:")
    new_terms = []
    n = len(variables)

    for i in range(len(terms)):
        for j in range(i + 1, len(terms)):
            diff = 0
            common = []
            for v in variables:
                vi = v in terms[i].split('∨')
                vj = v in terms[j].split('∨')
                if vi != vj:
                    diff += 1
                    if diff > 1:
                        break
                elif vi and vj:
                    common.append(v)

            if diff == 1:
                new_term = '∨'.join(common)
                print(f"{terms[i]} ∨ {terms[j]} => {new_term}")
                if new_term not in new_terms:
                    new_terms.append(new_term)

    print("\nРезультат после склеивания:")
    print(' ∧ '.join(new_terms) if new_terms else "Невозможно минимизировать дальше")

    # Построение таблицы покрытия
    print("\nПостроение таблицы покрытия:")
    header = "Импликанты\\Термы | " + " | ".join(terms)
    print(header)
    print("-" * len(header))

    for term in new_terms:
        coverage = []
        for orig_term in terms:
            covered = all(v in orig_term.split('∨') for v in term.split('∨'))
            coverage.append('X' if covered else ' ')
        print(f"{term:15} | " + " | ".join(coverage))

    # Выбор существенных импликант
    print("\nВыбор существенных импликант:")
    essential = []
    for i, term in enumerate(new_terms):
        is_essential = False
        for j in range(len(terms)):
            count = 0
            for k in range(len(new_terms)):
                if all(v in terms[j].split('∨') for v in new_terms[k].split('∨')):
                    count += 1
            if count == 1 and all(v in terms[j].split('∨') for v in term.split('∨')):
                is_essential = True
                break

        if is_essential:
            essential.append(term)
            print(f"Импликанта {term} существенная")

    print("\nМинимизированная СКНФ:")
    print(' ∧ '.join(essential) if essential else "Не удалось минимизировать")