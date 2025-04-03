from itertools import product, combinations


def print_header(title):
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)


def print_step(title):
    print("\n" + "-" * 50)
    print(f"{title:^50}")
    print("-" * 50)


class Minimizer:
    def __init__(self, variables):
        self.variables = variables
        self.n = len(variables)

    def term_to_str(self, term):
        """Преобразует терм в строку"""
        res = []
        for var, val in zip(self.variables, term):
            if val == 0:
                res.append(f"¬{var}")
            elif val == 1:
                res.append(var)
        return "".join(res)

    def str_to_term(self, s):
        """Преобразует строку в терм (с учетом отрицаний)"""
        term = []
        i = 0
        while i < len(s):
            if s[i] == '¬':
                term.append(0)
                i += 1
            else:
                term.append(1)
            i += 1
        return tuple(term)

    def is_implicant_covered(self, implicant, term):
        """Проверяет, покрывает ли импликант терм"""
        for i in range(self.n):
            if implicant[i] != 'X' and int(implicant[i]) != term[i]:
                return False
        return True

    def can_merge(self, term1, term2):
        """Проверяет, можно ли склеить два терма"""
        diff = 0
        res = []
        for i in range(self.n):
            if term1[i] == term2[i]:
                res.append(term1[i])
            else:
                res.append('X')
                diff += 1
        return (diff == 1, tuple(res))

    def calculate_method(self, terms, is_dnf=True):
        """Расчетный метод минимизации"""
        print_step("Этап склеивания")
        current_terms = [tuple(str(bit) for bit in term) for term in terms]
        prime_implicants = set()

        while True:
            new_terms = set()
            used = set()

            for i, j in combinations(range(len(current_terms)), 2):
                can_merge, merged = self.can_merge(current_terms[i], current_terms[j])
                if can_merge:
                    new_terms.add(merged)
                    used.add(i)
                    used.add(j)

            # Добавляем неиспользованные термы в простые импликанты
            for i in range(len(current_terms)):
                if i not in used:
                    prime_implicants.add(current_terms[i])

            print("Склеенные термы:")
            for term in new_terms:
                print(self.implicant_to_str(term))

            if not new_terms:
                break

            current_terms = list(new_terms)

        prime_implicants = list(prime_implicants)
        print_step("Результат после склеивания")
        print(" ∨ ".join(self.implicant_to_str(imp) for imp in prime_implicants))

        # Удаление лишних импликант
        print_step("Проверка на лишние импликанты")
        essential_implicants = []
        for i in range(len(prime_implicants)):
            cover_terms = []
            # Проверяем, покрываются ли термы другими импликантами
            for term in terms:
                if self.is_implicant_covered(prime_implicants[i], term):
                    covered_by_others = False
                    for j in range(len(prime_implicants)):
                        if j != i and self.is_implicant_covered(prime_implicants[j], term):
                            covered_by_others = True
                            break
                    if not covered_by_others:
                        cover_terms.append(term)

            if cover_terms:
                print(f"Импликант {self.implicant_to_str(prime_implicants[i])}")
                print(f"Покрывает термы: {', '.join(self.term_to_str(t) for t in cover_terms)}")
                essential_implicants.append(prime_implicants[i])
            else:
                print(f"Импликант {self.implicant_to_str(prime_implicants[i])} - лишний")

        print_step("Минимизированная форма")
        result = " ∨ ".join(self.implicant_to_str(imp) for imp in essential_implicants)
        print(result)
        return result

    def implicant_to_str(self, implicant):
        """Преобразует импликант в строку"""
        res = []
        for var, val in zip(self.variables, implicant):
            if val == '0':
                res.append(f"¬{var}")
            elif val == '1':
                res.append(var)
            # 'X' пропускаем
        if not res:  # для случая, когда все 'X'
            return "1" if len(self.variables) > 0 else "0"
        return "".join(res)

    def table_method(self, terms, is_dnf=True):
        """Расчетно-табличный метод"""
        print_step("Этап склеивания (как в расчетном методе)")
        current_terms = [tuple(str(bit) for bit in term) for term in terms]
        prime_implicants = set()

        while True:
            new_terms = set()
            used = set()

            for i, j in combinations(range(len(current_terms)), 2):
                can_merge, merged = self.can_merge(current_terms[i], current_terms[j])
                if can_merge:
                    new_terms.add(merged)
                    used.add(i)
                    used.add(j)

            for i in range(len(current_terms)):
                if i not in used:
                    prime_implicants.add(current_terms[i])

            if not new_terms:
                break

            current_terms = list(new_terms)

        prime_implicants = list(prime_implicants)

        # Построение таблицы покрытий
        print_step("Таблица покрытий")
        header = ["Импликанты\\Конституенты"] + [self.term_to_str(t) for t in terms]
        print("{:<20}".format(header[0]), end="")
        for col in header[1:]:
            print("{:>10}".format(col), end="")
        print()

        for imp in prime_implicants:
            print("{:<20}".format(self.implicant_to_str(imp)), end="")
            for term in terms:
                if self.is_implicant_covered(imp, term):
                    print("{:>10}".format("X"), end="")
                else:
                    print("{:>10}".format(""), end="")
            print()

        # Выбор существенных импликант (упрощенный)
        essential = []
        for term in terms:
            covering = []
            for imp in prime_implicants:
                if self.is_implicant_covered(imp, term):
                    covering.append(imp)
            if len(covering) == 1 and covering[0] not in essential:
                essential.append(covering[0])

        print_step("Существенные импликанты")
        for imp in essential:
            print(self.implicant_to_str(imp))

        # Попытка найти минимальное покрытие (упрощенный алгоритм)
        remaining_terms = [t for t in terms if not any(self.is_implicant_covered(e, t) for e in essential)]
        if remaining_terms:
            print("Остались непокрытые термы:", ", ".join(self.term_to_str(t) for t in remaining_terms))
            # Добавляем первый попавшийся импликант, который их покрывает
            for imp in prime_implicants:
                if imp not in essential and any(self.is_implicant_covered(imp, t) for t in remaining_terms):
                    essential.append(imp)
                    break

        print_step("Минимизированная форма")
        result = " ∨ ".join(self.implicant_to_str(imp) for imp in essential)
        print(result)
        return result

    def karnaugh_method(self, terms, is_dnf=True):
        """Табличный метод (карты Карно)"""
        print_step("Карта Карно")

        # Для 3 переменных создаем карту 2x4
        if self.n == 3:
            var1, var2, var3 = self.variables
            print(f"Карта Карно для {var1}{var2}\\{var3}:")
            print("     00  01  11  10")

            # Создаем карту в памяти
            karnaugh = [[0 for _ in range(4)] for _ in range(2)]

            # Заполняем карту
            for term in terms:
                a, b, c = term
                row = a
                col = (b << 1) | c
                if b and c:  # 11
                    col = 2
                elif b and not c:  # 10
                    col = 3
                elif not b and c:  # 01
                    col = 1
                else:  # 00
                    col = 0
                karnaugh[row][col] = 1

            # Выводим карту
            for row in range(2):
                print(f"{row} |", end="")
                for col in range(4):
                    print(f"  {karnaugh[row][col]}", end="")
                print()

            # Находим прямоугольные области
            rectangles = []

            # Проверяем всю строку (4 клетки)
            for row in range(2):
                if all(karnaugh[row][col] == 1 for col in range(4)):
                    rectangles.append((f"{var1}" if row else f"¬{var1}"))

            # Проверяем столбцы (2 клетки)
            for col1, col2 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                if karnaugh[0][col1] == 1 and karnaugh[1][col1] == 1 and \
                        karnaugh[0][col2] == 1 and karnaugh[1][col2] == 1:
                    # Определяем переменные для столбцов
                    b1, c1 = (col1 >> 1) & 1, col1 & 1
                    b2, c2 = (col2 >> 1) & 1, col2 & 1
                    if b1 == b2:  # меняется только c
                        rectangles.append(f"{var2 if b1 else f'¬{var2}'}")
                    elif c1 == c2:  # меняется только b
                        rectangles.append(f"{var3 if c1 else f'¬{var3}'}")

            # Проверяем одиночные пары
            for row in range(2):
                for col in range(4):
                    if karnaugh[row][col] == 1:
                        # Проверяем пару по вертикали
                        if row == 0 and karnaugh[1][col] == 1:
                            b, c = (col >> 1) & 1, col & 1
                            rectangles.append(f"{var2 if b else f'¬{var2}'}{var3 if c else f'¬{var3}'}")
                        # Проверяем пару по горизонтали
                        if col < 3 and karnaugh[row][col] == 1 and karnaugh[row][col + 1] == 1:
                            b1, c1 = (col >> 1) & 1, col & 1
                            b2, c2 = ((col + 1) >> 1) & 1, (col + 1) & 1
                            if b1 == b2:  # меняется только c
                                rectangles.append(f"{var1 if row else f'¬{var1}'}{var2 if b1 else f'¬{var2}'}")
                            elif c1 == c2:  # меняется только b
                                rectangles.append(f"{var1 if row else f'¬{var1}'}{var3 if c1 else f'¬{var3}'}")

            # Удаляем дубликаты
            rectangles = list(dict.fromkeys(rectangles))

            # Выбираем минимальное покрытие (упрощенный подход)
            covered = [[False for _ in range(4)] for _ in range(2)]
            result_parts = []

            # Сначала добавляем самые большие области
            for rect in rectangles:
                if len(rect) == 1 or (len(rect) == 2 and rect[0] == '¬'):  # вся строка
                    var = rect
                    row = 1 if var == var1 else 0
                    for col in range(4):
                        if karnaugh[row][col] == 1:
                            covered[row][col] = True
                    result_parts.append(var)

            # Затем добавляем оставшиеся
            for row in range(2):
                for col in range(4):
                    if karnaugh[row][col] == 1 and not covered[row][col]:
                        b, c = (col >> 1) & 1, col & 1
                        part = f"{var2 if b else f'¬{var2}'}{var3 if c else f'¬{var3}'}"
                        result_parts.append(part)
                        covered[row][col] = True

            # Удаляем дубликаты
            result_parts = list(dict.fromkeys(result_parts))

            print_step("Минимизированная форма")
            result = " ∨ ".join(result_parts)
            print(result)
            return result

        else:
            print("Реализовано только для 3 переменных")
            return ""