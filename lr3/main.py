from itertools import combinations

# Функция для склеивания двух термов
def merge_terms(term1, term2):
    differences = 0
    merged_term = []
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            differences += 1
            merged_term.append('X')  # Обозначаем пропущенную переменную
        else:
            merged_term.append(term1[i])
    if differences == 1:
        return merged_term
    return None

# Функция для минимизации DNF или CNF расчетным методом
def minimize_form_calculational(form):
    terms = form.copy()
    while True:
        new_terms = []
        used = set()
        for i, j in combinations(range(len(terms)), 2):
            merged = merge_terms(terms[i], terms[j])
            if merged:
                used.add(i)
                used.add(j)
                if merged not in new_terms:
                    new_terms.append(merged)
        if not new_terms:
            break
        for i in range(len(terms)):
            if i not in used and terms[i] not in new_terms:
                new_terms.append(terms[i])
        terms = new_terms
    return terms

# Функция для минимизации CNF табличным методом
def minimize_cnf_tabular(cnf):
    terms = cnf.copy()
    table = []
    for i in range(len(terms)):
        table.append([0] * len(terms))
    for i, j in combinations(range(len(terms)), 2):
        merged = merge_terms(terms[i], terms[j])
        if merged:
            table[i][j] = 1
            table[j][i] = 1
    used = set()
    minimized_terms = []
    for i in range(len(terms)):
        if i not in used:
            minimized_terms.append(terms[i])
            for j in range(len(terms)):
                if table[i][j]:
                    used.add(j)
    return minimized_terms

# Запуск программы
if __name__ == "__main__":
    main()