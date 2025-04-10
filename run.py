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

    # Минимизация СДНФ расчетным методом
    print("\n1. Минимизация СДНФ расчетным методом:")
    min_sdnf_calc = minimizer.minimize_calculus_method(sdnf_terms, True)

    # Минимизация СКНФ расчетным методом
    print("\n2. Минимизация СКНФ расчетным методом:")
    min_sknf_calc = minimizer.minimize_calculus_method(sknf_terms, False)

    # Минимизация СДНФ расчетно-табличным методом
    print("\n3. Минимизация СДНФ расчетно-табличным методом:")
    min_sdnf_table = minimizer.minimize_table_calculus_method(sdnf_terms, True)

    # Минимизация СКНФ расчетно-табличным методом
    print("\n4. Минимизация СКНФ расчетно-табличным методом:")
    min_sknf_table = minimizer.minimize_table_calculus_method(sknf_terms, False)

    # В основной программе:
    print("\nМинимизация методом Карно:")
    print("=" * 60)

    print("\nДля СДНФ:")
    print("-" * 60)
    min_sdnf_karno = minimizer.minimize_karnaugh(sdnf_terms, vars, True)

    print("\nДля СКНФ:")
    print("-" * 60)
    min_sknf_karno = minimizer.minimize_karnaugh(sknf_terms, vars, False)

    print("=" * 60)

if __name__ == "__main__":
    main()