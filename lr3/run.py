from main import *


def tokenize(expr):
    return re.findall(r'\(|\)|[a-e]+|!|¬|∧|&|∨|\||->|~', expr)


def to_postfix(tokens):
    output, stack = [], []
    for token in tokens:
        if re.match(r'[a-e]', token):
            output.append(token)
        elif token in OPERATORS:
            while stack and stack[-1] in OPERATORS and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
    while stack:
        output.append(stack.pop())
    return output


def eval_rpn(rpn, values):
    stack = []
    for token in rpn:
        if token in values:
            stack.append(values[token])
        elif token in OPERATOR_FUNCTIONS:
            if OPERATORS[token][1] == "unary":
                stack.append(OPERATOR_FUNCTIONS[token](stack.pop()))
            else:
                b, a = stack.pop(), stack.pop()
                stack.append(OPERATOR_FUNCTIONS[token](a, b))
    return stack[0]


def truth_table(vars, expr):
    rpn = to_postfix(tokenize(expr))
    for row in itertools.product([0, 1], repeat=len(vars)):
        values = dict(zip(vars, row))
        yield row + (int(eval_rpn(rpn, values)),)


def build_sdnf_sknf(table, vars):
    sdnf_terms, sknf_terms = [], []
    for row in table:
        vals, res = row[:-1], row[-1]
        if res:
            sdnf_terms.append(' ∧ '.join(f"{'' if v else '¬'}{var}" for var, v in zip(vars, vals)))
        else:
            sknf_terms.append(' ∨ '.join(f"{var if v == 0 else '¬' + var}" for var, v in zip(vars, vals)))
    return sdnf_terms, sknf_terms


def print_minimization_results(title, method_name, terms, is_dnf, minimizer):
    print(f"\n{title}:")
    print("-" * 60)
    method = getattr(minimizer, method_name)
    result = method(terms, is_dnf)
    print("-" * 60)
    return result


def main():
    expr = input("Введите логическую формулу: ")
    vars = sorted(set(re.findall(r'[a-e]', expr)))
    table = list(truth_table(vars, expr))
    sdnf_terms, sknf_terms = build_sdnf_sknf(table, vars)

    print("\nИсходная СДНФ:")
    print(" ∨ ".join([f"({term})" for term in sdnf_terms]))

    print("\nИсходная СКНФ:")
    print(" ∧ ".join([f"({term})" for term in sknf_terms]))

    minimizer = BooleanMinimizer()

    # Минимизация расчетным методом
    results = {
        "1. СДНФ (расчетный метод)": ("minimize_calculus_method", sdnf_terms, True),
        "2. СКНФ (расчетный метод)": ("minimize_calculus_method", sknf_terms, False),
        "3. СДНФ (табличный метод)": ("minimize_table_calculus_method", sdnf_terms, True),
        "4. СКНФ (табличный метод)": ("minimize_table_calculus_method", sknf_terms, False)
    }

    minimized = {}
    for title, (method, terms, is_dnf) in results.items():
        minimized[title] = print_minimization_results(title, method, terms, is_dnf, minimizer)

    # Минимизация методом Карно
    print("\nМинимизация методом Карно:")
    print("=" * 60)

    karno_results = {
        "СДНФ (Карно)": (sdnf_terms, True),
        "СКНФ (Карно)": (sknf_terms, False)
    }

    for title, (terms, is_dnf) in karno_results.items():
        print(f"\n{title}:")
        print("-" * 60)
        result = minimizer.minimize_karnaugh(terms, vars, is_dnf)
        minimized[title] = result
        print("-" * 60)

    print("=" * 60)

    # Вывод всех результатов для сравнения
    print("\nИтоговые результаты минимизации:")
    for title, result in minimized.items():
        print(f"\n{title}:")
        print(result)


if __name__ == "__main__":
    main()