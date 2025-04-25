import itertools
import re
import operator
from collections import defaultdict

OPERATORS = {
    "!": (4, "unary"),
    "¬": (4, "unary"),
    "∧": (3, "binary"),
    "&": (3, "binary"),
    "∨": (2, "binary"),
    "|": (2, "binary"),
    "->": (1, "binary"),
    "~": (0, "binary")
}

OPERATOR_FUNCTIONS = {
    "!": lambda a: not a,
    "¬": lambda a: not a,
    "∧": operator.and_,
    "&": operator.and_,
    "∨": operator.or_,
    "|": operator.or_,
    "->": lambda a, b: (not a) or b,
    "~": operator.eq
}


class BooleanMinimizer:
    BINARY_OPS = {"∧", "∨"}
    LITERALS = set("abcde")

    @staticmethod
    def _get_literals(term: str):
        literals = set()
        i = 0
        while i < len(term):
            if term[i] == '¬':
                literals.add(f"¬{term[i + 1]}")
                i += 2
            elif term[i] in BooleanMinimizer.LITERALS:
                literals.add(term[i])
                i += 1
            else:
                i += 1
        return literals

    @staticmethod
    def _are_adjacent(term1: str, term2: str):
        lits1 = BooleanMinimizer._get_literals(term1)
        lits2 = BooleanMinimizer._get_literals(term2)
        diff = lits1.symmetric_difference(lits2)

        if len(diff) != 2:
            return None

        a, b = diff.pop(), diff.pop()
        if a.replace("¬", "") != b.replace("¬", ""):
            return None

        return lits1.intersection(lits2)

    @staticmethod
    def _detect_operator(terms):
        for term in terms:
            for char in term:
                if char in BooleanMinimizer.BINARY_OPS:
                    return char
        return None

    @staticmethod
    def _print_calculus_step(current_terms, step, is_dnf):
        print(f"\nЭтап склеивания {step}")
        print(f"Ищем термы, отличающиеся одной переменной (n={len(current_terms[0].split('∧'))}):")

    @staticmethod
    def _find_combinations(current_terms, is_dnf):
        new_terms = []
        used_indices = set()
        combinations = []

        for i in range(len(current_terms)):
            for j in range(i + 1, len(current_terms)):
                common = BooleanMinimizer._are_adjacent(current_terms[i], current_terms[j])
                if common is not None:
                    used_indices.add(i)
                    used_indices.add(j)
                    merged = f"{'∧' if is_dnf else '∨'}".join(sorted(common))
                    combinations.append(f"({current_terms[i]}){i + 1} ∨ ({current_terms[j]}){j + 1} => ({merged})")
                    if merged not in new_terms:
                        new_terms.append(merged)

        return new_terms, used_indices, combinations

    @staticmethod
    def _add_unused_terms(current_terms, new_terms, used_indices):
        for i in range(len(current_terms)):
            if i not in used_indices and current_terms[i] not in new_terms:
                new_terms.append(current_terms[i])
        return new_terms

    @staticmethod
    def _check_redundant_implicants(current_terms, is_dnf):
        redundant = set()
        for i in range(len(current_terms)):
            print(f"{i + 1}) Проверяем ({current_terms[i]})")
            covered = False
            for j in range(len(current_terms)):
                if i != j:
                    lits_i = BooleanMinimizer._get_literals(current_terms[i])
                    lits_j = BooleanMinimizer._get_literals(current_terms[j])
                    if is_dnf:
                        if lits_j.issubset(lits_i):
                            covered = True
                            break
                    else:
                        if lits_i.issubset(lits_j):
                            covered = True
                            break
            if covered:
                print(f"  Терм ({current_terms[i]}) покрывается другими и может быть лишним")
                redundant.add(i)
            else:
                print(f"  Терм ({current_terms[i]}) необходим")
        return redundant

    @staticmethod
    def minimize_calculus_method(terms, is_dnf=True):
        print("\nРасчетный метод")
        print(f"Исходная {'СДНФ' if is_dnf else 'СКНФ'}:")
        print(" ∨ ".join([f"({term}){i + 1}" for i, term in enumerate(terms)]))

        current_terms = terms.copy()
        step = 1

        while True:
            BooleanMinimizer._print_calculus_step(current_terms, step, is_dnf)
            new_terms, used_indices, combinations = BooleanMinimizer._find_combinations(current_terms, is_dnf)

            if not combinations:
                print("Нет возможных склеиваний")
                break

            for comb in combinations:
                print(comb)

            new_terms = BooleanMinimizer._add_unused_terms(current_terms, new_terms, used_indices)
            print("\nРезультат:")
            print(" ∨ ".join([f"({term}){i + 1}" for i, term in enumerate(new_terms)]))

            if len(new_terms) == len(current_terms):
                break

            current_terms = new_terms
            step += 1

        print("\nПроверка на лишние импликанты:")
        redundant = BooleanMinimizer._check_redundant_implicants(current_terms, is_dnf)
        final_terms = [term for i, term in enumerate(current_terms) if i not in redundant]

        print("\nИтоговый результат:")
        result = " ∨ ".join([f"({term})" for term in final_terms]) if is_dnf else " ∧ ".join(
            [f"({term})" for term in final_terms])
        print(result)
        return result

    @staticmethod
    def _find_prime_implicants(terms, is_dnf):
        current_terms = terms.copy()
        prime_implicants = []
        changed = True

        while changed:
            changed = False
            new_terms = []
            used = set()

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    common = BooleanMinimizer._are_adjacent(current_terms[i], current_terms[j])
                    if common is not None:
                        used.add(i)
                        used.add(j)
                        merged = f"{'∨' if not is_dnf else '∧'}".join(sorted(common))
                        if merged not in new_terms:
                            new_terms.append(merged)
                            changed = True

            for i in range(len(current_terms)):
                if i not in used and current_terms[i] not in new_terms:
                    prime_implicants.append(current_terms[i])

            current_terms = new_terms

        prime_implicants.extend(current_terms)
        return prime_implicants

    @staticmethod
    def _build_coverage_table(prime_implicants, terms, is_dnf):
        coverage = []
        for imp in prime_implicants:
            row = []
            imp_lits = BooleanMinimizer._get_literals(imp)
            for term in terms:
                term_lits = BooleanMinimizer._get_literals(term)
                if not is_dnf:
                    covers = term_lits.issubset(imp_lits)
                else:
                    covers = imp_lits.issubset(term_lits)
                row.append("X" if covers else " ")
            coverage.append((imp, row))
        return coverage

    @staticmethod
    def _select_minimal_coverage(coverage, terms, is_dnf):
        selected = []
        remaining_terms = set(range(1, len(terms) + 1))

        if not is_dnf:
            print("Для КНФ выбираем все простые импликанты:")
            selected = [imp for imp, _ in coverage]
            remaining_terms = set()
        else:
            term_coverage = defaultdict(list)
            for i, (imp, row) in enumerate(coverage):
                for j, val in enumerate(row):
                    if val == "X":
                        term_coverage[j + 1].append(i)

            while remaining_terms:
                best_imp = None
                best_cover = set()
                best_idx = -1

                for i, (imp, row) in enumerate(coverage):
                    if imp in selected:
                        continue
                    current_cover = {j + 1 for j, val in enumerate(row) if val == "X" and (j + 1) in remaining_terms}
                    if len(current_cover) > len(best_cover):
                        best_cover = current_cover
                        best_imp = imp
                        best_idx = i

                if best_imp:
                    selected.append(best_imp)
                    remaining_terms -= best_cover
                    print(f"Выбираем ({best_imp}), покрывающую термы {sorted(best_cover)}")
                else:
                    break

        return selected

    @staticmethod
    def minimize_table_calculus_method(terms, is_dnf=True):
        print("\nРасчетно-табличный метод")
        print("Этап склеивания:")

        prime_implicants = BooleanMinimizer._find_prime_implicants(terms, is_dnf)
        print("\nПолученные простые импликанты:")
        print(" ∨ ".join([f"({term}){i + 1}" for i, term in enumerate(prime_implicants)]))

        print("\nПостроение таблицы покрытий:")
        print("Импликанты\\Конституенты | " + " | ".join([f"({term}){i + 1}" for i, term in enumerate(terms)]))
        print("-" * (30 + 8 * len(terms)))

        coverage = BooleanMinimizer._build_coverage_table(prime_implicants, terms, is_dnf)
        for imp, row in coverage:
            print(f"({imp})".ljust(25) + " | " + " | ".join(row))

        print("\nВыбор минимального покрытия:")
        selected = BooleanMinimizer._select_minimal_coverage(coverage, terms, is_dnf)

        print("\nИтоговый результат:")
        result = " ∨ ".join([f"({imp})" for imp in selected]) if is_dnf else " ∧ ".join(
            [f"({imp})" for imp in selected])
        print(result)
        return result

    @staticmethod
    def _create_karnaugh_map(values, variables, var_count):
        if var_count == 2:
            k_map = [[0, 0], [0, 0]]
            for val in values:
                a = val.get(variables[0], 0)
                b = val.get(variables[1], 0)
                if a is not None and b is not None:
                    k_map[b][a] = 1
            return k_map

        elif var_count == 3:
            gray_order = ['00', '01', '11', '10']
            k_map = [[0, 0], [0, 0], [0, 0], [0, 0]]
            for val in values:
                a = val.get(variables[0], 0)
                b = val.get(variables[1], 0)
                c = val.get(variables[2], 0)
                if a is not None and b is not None and c is not None:
                    row = gray_order.index(f"{b}{a}")
                    k_map[row][c] = 1
            return k_map

        elif var_count == 4:
            gray_order = ['00', '01', '11', '10']
            k_map = [[0] * 4 for _ in range(4)]
            for val in values:
                a = val.get(variables[0], 0)
                b = val.get(variables[1], 0)
                c = val.get(variables[2], 0)
                d = val.get(variables[3], 0)
                if all(v is not None for v in [a, b, c, d]):
                    row = gray_order.index(f"{b}{a}")
                    col = gray_order.index(f"{d}{c}")
                    k_map[row][col] = 1
            return k_map

        elif var_count == 5:
            gray_order = ['00', '01', '11', '10']
            k_map0 = [[0] * 4 for _ in range(4)]
            k_map1 = [[0] * 4 for _ in range(4)]
            for val in values:
                a = val.get(variables[0], 0)
                b = val.get(variables[1], 0)
                c = val.get(variables[2], 0)
                d = val.get(variables[3], 0)
                e = val.get(variables[4], 0)
                if all(v is not None for v in [a, b, c, d, e]):
                    row = gray_order.index(f"{b}{a}")
                    col = gray_order.index(f"{d}{c}")
                    if e == 0:
                        k_map0[row][col] = 1
                    else:
                        k_map1[row][col] = 1
            return (k_map0, k_map1)

        return None

    @staticmethod
    def _print_karnaugh_map(k_map, variables, var_count):
        if var_count == 2:
            print("\nКарта Карно для 2 переменных:")
            print("   " + variables[1] + "\\" + variables[0] + " | 0 | 1")
            print("   ----|---|---")
            for b in [0, 1]:
                print(f"   {b}   | {' | '.join(str(k_map[b][a]) for a in [0, 1])}")

        elif var_count == 3:
            print("\nКарта Карно для 3 переменных:")
            print("   " + variables[1] + variables[0] + "\\" + variables[2] + " | 0 | 1")
            print("   -----|---|---")
            gray_order = ['00', '01', '11', '10']
            for row in range(4):
                print(f"   {gray_order[row]}  | {' | '.join(str(k_map[row][c]) for c in [0, 1])}")

        elif var_count == 4:
            print("\nКарта Карно для 4 переменных:")
            print("   " + variables[1] + variables[0] + "\\" + variables[3] + variables[2] + " | 00 | 01 | 11 | 10")
            print("   ------|----|----|----|----")
            gray_order = ['00', '01', '11', '10']
            for row in range(4):
                print(f"   {gray_order[row]}  | {' | '.join(str(k_map[row][col]) for col in range(4))}")

        elif var_count == 5:
            k_map0, k_map1 = k_map
            print("\nКарта Карно для 5 переменных (2 карты 4x4):")
            print("Для e=0:")
            print("   " + variables[1] + variables[0] + "\\" + variables[3] + variables[2] + " | 00 | 01 | 11 | 10")
            print("   ------|----|----|----|----")
            gray_order = ['00', '01', '11', '10']
            for row in range(4):
                print(f"   {gray_order[row]}  | {' | '.join(str(k_map0[row][col]) for col in range(4))}")

            print("\nДля e=1:")
            print("   " + variables[1] + variables[0] + "\\" + variables[3] + variables[2] + " | 00 | 01 | 11 | 10")
            print("   ------|----|----|----|----")
            for row in range(4):
                print(f"   {gray_order[row]}  | {' | '.join(str(k_map1[row][col]) for col in range(4))}")

    @staticmethod
    def _format_result(prime_implicants, variables, is_dnf):
        result_terms = []
        for imp in prime_implicants:
            parts = []
            for var in variables:
                if var in imp:
                    parts.append(var)
                elif f"¬{var}" in imp:
                    parts.append(f"¬{var}")
            if is_dnf:
                result_terms.append(" ∧ ".join(parts))
            else:
                result_terms.append(" ∨ ".join(parts))

        result = " ∨ ".join([f"({term})" for term in result_terms]) if is_dnf else " ∧ ".join(
            [f"({term})" for term in result_terms])
        return result

    @staticmethod
    def minimize_karnaugh(terms, variables, is_dnf=True):
        var_count = len(variables)
        if var_count > 5:
            print("\nКарта Карно не поддерживается для более чем 5 переменных")
            return " ∨ ".join([f"({term})" for term in terms]) if is_dnf else " ∧ ".join(
                [f"({term})" for term in terms])

        print(f"\nМинимизация {'СДНФ' if is_dnf else 'СКНФ'} методом Карно:")

        values = []
        for term in terms:
            lits = BooleanMinimizer._get_literals(term)
            val = {}
            for var in variables:
                if f"¬{var}" in lits:
                    val[var] = 0
                elif var in lits:
                    val[var] = 1
                else:
                    val[var] = None
            values.append(val)

        k_map = BooleanMinimizer._create_karnaugh_map(values, variables, var_count)
        BooleanMinimizer._print_karnaugh_map(k_map, variables, var_count)

        prime_implicants = BooleanMinimizer._quine_mccluskey(
            [BooleanMinimizer._get_literals(term) for term in terms],
            var_count
        )

        result = BooleanMinimizer._format_result(prime_implicants, variables, is_dnf)
        print("\nИтоговый результат:")
        print(result)
        return result

    @staticmethod
    def _quine_mccluskey(minterms, var_count):
        binary_terms = []
        for term in minterms:
            bits = ['-'] * var_count
            for lit in term:
                var_idx = ord(lit[-1]) - ord('a')
                if lit.startswith('¬'):
                    bits[var_idx] = '0'
                else:
                    bits[var_idx] = '1'
            binary_terms.append(''.join(bits))

        groups = defaultdict(list)
        for term in binary_terms:
            ones = term.count('1')
            groups[ones].append(term)

        prime_implicants = set()
        changed = True

        while changed:
            changed = False
            new_groups = defaultdict(list)
            used = set()

            for ones in sorted(groups.keys()):
                for term1 in groups[ones]:
                    if ones + 1 in groups:
                        for term2 in groups[ones + 1]:
                            diff = 0
                            merged = []
                            for b1, b2 in zip(term1, term2):
                                if b1 == b2:
                                    merged.append(b1)
                                elif b1 == '-' or b2 == '-':
                                    break
                                else:
                                    diff += 1
                                    merged.append('-')
                            else:
                                if diff == 1:
                                    merged_str = ''.join(merged)
                                    new_ones = merged_str.count('1')
                                    new_groups[new_ones].append(merged_str)
                                    used.add(term1)
                                    used.add(term2)
                                    changed = True

            for ones in groups:
                for term in groups[ones]:
                    if term not in used:
                        prime_implicants.add(term)

            groups = new_groups

        result = []
        for imp in prime_implicants:
            lits = set()
            for i, bit in enumerate(imp):
                var = chr(ord('a') + i)
                if bit == '0':
                    lits.add(f'¬{var}')
                elif bit == '1':
                    lits.add(var)
            result.append(frozenset(lits))

        return result