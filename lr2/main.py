import itertools
import operator

def parse_expression(expr):
    """Заменяет логические операторы на Python-аналоги."""
    expr = expr.replace("∨", " or ")  # Поддержка Unicode-символов
    expr = expr.replace("∧", " and ")
    expr = expr.replace("&", " and ")
    expr = expr.replace("|", " or ")
    expr = expr.replace("!", " not ")
    expr = expr.replace("->", " <= ")
    expr = expr.replace("~", " == ")
    return expr

def evaluate_expression(expr, local_dict):
    # Преобразуем выражение в функцию
    expr = parse_expression(expr)
    # Создаем лямбда-функцию, которая будет выполнять выражение
    func = lambda **kwargs: eval(expr, {}, kwargs)
    return func(**local_dict)

def generate_truth_table(variables, expression):
    """Создаёт таблицу истинности."""
    table = []
    parsed_expr = parse_expression(expression)

    for values in itertools.product([0, 1], repeat=len(variables)):
        local_dict = dict(zip(variables, values))
        result = evaluate_expression(parsed_expr, local_dict)
        table.append((*values, int(result)))

    return table

def build_sdnf_sknf(table, variables):
    """Формирует СДНФ и СКНФ."""
    sdnf_terms = []
    sknf_terms = []
    sdnf_nums = []
    sknf_nums = []

    for i, row in enumerate(table):
        values, result = row[:-1], row[-1]
        term = []

        if result == 1:
            for var, val in zip(variables, values):
                term.append(f"{'¬' if val == 0 else ''}{var}")
            sdnf_terms.append(f"({' ∧ '.join(term)})")
            sdnf_nums.append(i)
        else:
            for var, val in zip(variables, values):
                term.append(f"{var if val == 0 else '¬' + var}")
            sknf_terms.append(f"({' ∨ '.join(term)})")
            sknf_nums.append(i)

    return " ∨ ".join(sdnf_terms), " ∧ ".join(sknf_terms), tuple(sdnf_nums), tuple(sknf_nums)

def compute_index_form(table):
    """Вычисляет индексную форму, учитывая всю таблицу истинности."""
    binary_str = "".join(str(row[-1]) for row in table)
    decimal_value = int(binary_str, 2)
    return f"{binary_str} - {decimal_value}"

def print_table(table, variables):
    """Выводит таблицу истинности в красивом формате."""
    header = " | ".join(variables) + " | F"
    print(header)
    print("-" * len(header))
    for row in table:
        print(" | ".join(map(str, row)))
