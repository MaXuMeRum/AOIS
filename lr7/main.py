import random
import logging

class DiagonalMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        self.bit_columns = [[0 for _ in range(rows)] for _ in range(cols)]
        self.random_fill()
        logging.basicConfig(level=logging.ERROR)

    def random_fill(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.randint(0, 1)  # Заполняем 0 или 1
                # Обновляем bit_columns
                for bit in range(self.rows):
                    self.bit_columns[j][bit] = (self.matrix[i][j] >> bit) & 1

    def set_value(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.matrix[row][col] = value
            for i in range(self.rows):
                self.bit_columns[col][i] = (self.matrix[i][col] >> row) & 1
        else:
            logging.error("Индексы вне диапазона")

    def get_value(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.matrix[row][col]
        else:
            logging.error("Индексы вне диапазона")
            return None

    def get_bit_column(self, col, bit_pos=None):
        """Возвращает разрядный столбец для конкретного бита"""
        if 0 <= col < self.cols:
            if bit_pos is None:
                bit_pos = int(input(f"Введите номер бита (0-{self.rows-1}): "))
            if 0 <= bit_pos < self.rows:
                return [(self.matrix[row][col] >> bit_pos) & 1 for row in range(self.rows)]
            else:
                print(f"Ошибка: Номер бита должен быть от 0 до {self.rows-1}")
                return None
        else:
            print(f"Ошибка: Номер столбца должен быть от 0 до {self.cols-1}")
            return None

    def logical_f1_f14(self, col1, col2):
        if 0 <= col1 < self.cols and 0 <= col2 < self.cols:
            # Берём целые числа из столбцов (если матрица 0/1)
            col1_data = [self.matrix[i][col1] for i in range(self.rows)]
            col2_data = [self.matrix[i][col2] for i in range(self.rows)]

            and_result = [a & b for a, b in zip(col1_data, col2_data)]
            or_result = [a | b for a, b in zip(col1_data, col2_data)]
            return and_result, or_result
        else:
            print("Ошибка: Столбцы вне диапазона")
            return None, None

    def logical_f3_f12(self, col1, col2):
        if 0 <= col1 < self.cols and 0 <= col2 < self.cols:
            # Берём значения из столбцов (не биты!)
            col1_data = [self.matrix[i][col1] for i in range(self.rows)]
            col2_data = [self.matrix[i][col2] for i in range(self.rows)]

            # NAND = NOT AND
            nand_result = [int(not (a and b)) for a, b in zip(col1_data, col2_data)]
            # NOR = NOT OR
            nor_result = [int(not (a or b)) for a, b in zip(col1_data, col2_data)]

            return nand_result, nor_result
        else:
            print("Ошибка: Столбцы вне диапазона")
            return None, None

    def search_above(self, col, row, value):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            for r in range(row - 1, -1, -1):
                if self.matrix[r][col] == value:
                    return r, col
            return None
        else:
            logging.error("Индексы вне диапазона")
            return None

    def search_below(self, col, row, value):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            for r in range(row + 1, self.rows):
                if self.matrix[r][col] == value:
                    return r, col
            return None
        else:
            print("Ошибка: Индексы вне диапазона")
            return None

    def add_fields_with_condition(self, v_value):
        result = []
        for j in range(self.cols):
            for i in range(self.rows):
                word = self.matrix[i][j]
                vj = (word >> 6) & 0b111
                if vj == v_value:
                    aj = (word >> 0) & 0b111
                    bj = (word >> 3) & 0b111
                    sum_ab = aj + bj
                    result.append((i, j, aj, bj, sum_ab))
        return result

    def set_bit_column(self, col, bit_pos, bit_values):
        """Устанавливает разрядный столбец для бита bit_pos"""
        if 0 <= col < self.cols and 0 <= bit_pos < self.rows:
            for row in range(self.rows):
                # Обновляем бит в слове
                if bit_values[row] == 1:
                    self.matrix[row][col] |= (1 << bit_pos)
                else:
                    self.matrix[row][col] &= ~(1 << bit_pos)
                # Обновляем bit_columns
                self.bit_columns[col][bit_pos] = bit_values[row]
        else:
            logging.error("Неверные индексы")

    def print_word(self, row, col):
        """Печатает слово из матрицы по заданным индексам"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            print(f"Слово в позиции ({row}, {col}): {self.matrix[row][col]}")
        else:
            print("Ошибка: Неверные индексы")