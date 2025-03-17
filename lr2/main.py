import itertools
import re
import operator

# Операторы и их приоритеты
OPERATORS = {
    "!": (4, "unary"),  # НЕ (унарный)
    "∧": (3, "binary"),  # И
    "&": (3, "binary"),  # И (альтернативный символ)
    "∨": (2, "binary"),  # ИЛИ
    "|": (2, "binary"),  # ИЛИ (альтернативный символ)
    "->": (1, "binary"),  # Импликация
    "~": (0, "binary")  # Эквивалентность
}

# Функции операций
OPERATOR_FUNCTIONS = {
    "!": lambda a: not a,
    "∧": operator.and_,
    "&": operator.and_,
    "∨": operator.or_,
    "|": operator.or_,
    "->": lambda a, b: (not a) or b,  # Импликация
    "~": operator.eq  # Эквивалентность
}


def tokenize(expression):
    """Разбивает выражение на токены (переменные, операторы, скобки)."""
    return re.findall(r'\(|\)|[a-e]+|!|∧|&|∨|\||->|~', expression)


def to_postfix(tokens):
    """Преобразует инфиксное выражение в обратную польскую запись (RPN)"""
    output = []
    stack = []

    for token in tokens:
        if token in "a b c d e":  # Переменные
            output.append(token)
        elif token in OPERATORS:
            while (stack and stack[-1] in OPERATORS and
                   OPERATORS[token][0] <= OPERATORS[stack[-1]][0]):
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()  # Убираем '('

    while stack:
        output.append(stack.pop())

    return output


def evaluate_rpn(rpn_tokens, values):
    """Вычисляет значение выражения, представленного в RPN"""
    stack = []

    for token in rpn_tokens:
        if token in values:  # Переменная
            stack.append(values[token])
        elif token in OPERATOR_FUNCTIONS:
            if OPERATORS[token][1] == "unary":  # Унарный оператор (!)
                a = stack.pop()
                stack.append(OPERATOR_FUNCTIONS[token](a))
            else:  # Бинарный оператор
                b = stack.pop()
                a = stack.pop()
                stack.append(OPERATOR_FUNCTIONS[token](a, b))

    return stack[0]


def generate_truth_table(variables, expression):
    """Создаёт таблицу истинности."""
    table = []
    tokens = tokenize(expression)
    rpn_expr = to_postfix(tokens)

    for values in itertools.product([0, 1], repeat=len(variables)):
        local_dict = dict(zip(variables, values))
        result = evaluate_rpn(rpn_expr, local_dict)
        table.append((*values, int(result)))

    return table


def build_sdnf_sknf(table, variables):
    """Формирует СДНФ и СКНФ."""
    sdnf_terms, sknf_terms = [], []
    sdnf_nums, sknf_nums = [], []

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
    """Вычисляет индексную форму функции."""
    binary_str = "".join(str(row[-1]) for row in table)
    decimal_value = int(binary_str, 2)
    return f"{binary_str} - {decimal_value}"