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
        """Автоматическое заполнение матрицы случайными значениями"""
        for i in range(self.rows):
            for j in range(self.cols):
                aj = random.randint(0, 7)  # 3 бита (0-7)
                bj = random.randint(0, 7)  # 3 бита (0-7)
                vj = random.randint(0, 7)  # 3 бита (0-7)
                word = (vj << 6) | (bj << 3) | aj
                self.set_value(i, j, word)

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
            and_result = [a & b for a, b in zip(self.bit_columns[col1], self.bit_columns[col2])]
            or_result = [a | b for a, b in zip(self.bit_columns[col1], self.bit_columns[col2])]
            return and_result, or_result
        else:
            print("Ошибка: Столбцы вне диапазона")
            return None, None

    def logical_f3_f12(self, col1, col2):
        if 0 <= col1 < self.cols and 0 <= col2 < self.cols:
            nand_result = [~(a & b) & 1 for a, b in zip(self.bit_columns[col1], self.bit_columns[col2])]
            nor_result = [~(a | b) & 1 for a, b in zip(self.bit_columns[col1], self.bit_columns[col2])]
            return nand_result, nor_result

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