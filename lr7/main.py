import random
from typing import List, Tuple, Union


class CustomDiagonalGrid:
    def __init__(self, num_rows: int, num_cols: int):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    def store_data_row(self, data: List[int], begin_row: int, col: int) -> None:
        for idx, value in enumerate(data):
            row_idx = (begin_row + idx) % self.num_rows
            self.grid[row_idx][col] = value

    def store_diagonal_data(self, data: List[int], begin_row: int, begin_col: int) -> None:
        for idx, value in enumerate(data):
            row_idx = (begin_row + idx) % self.num_rows
            col_idx = (begin_col + idx) % self.num_cols
            self.grid[row_idx][col_idx] = value

    def fetch_data_row(self, begin_row: int, col: int, length: int) -> List[int]:
        result = []
        for i in range(length):
            row_idx = (begin_row + i) % self.num_rows
            result.append(self.grid[row_idx][col])
        return result

    def fetch_diagonal_data(self, begin_row: int, begin_col: int, length: int) -> List[int]:
        result = []
        for i in range(length):
            row_idx = (begin_row + i) % self.num_rows
            col_idx = (begin_col + i) % self.num_cols
            result.append(self.grid[row_idx][col_idx])
        return result

    def f1(self, col_a: int, col_b: int, result_col: int) -> List[int]:
        """Конъюнкция (логическое И) между столбцами col_a и col_b"""
        data_a = [self.grid[row][col_a] for row in range(self.num_rows)]
        data_b = [self.grid[row][col_b] for row in range(self.num_rows)]
        result = [a & b for a, b in zip(data_a, data_b)]  # Побитовое И
        for row in range(self.num_rows):
            self.grid[row][result_col] = result[row]
        return result

    def f3(self, col_src: int, col_dummy: int, result_col: int) -> List[int]:
        """Повторение 1-го аргумента (col_src), col_dummy игнорируется"""
        data = [self.grid[row][col_src] for row in range(self.num_rows)]
        for row in range(self.num_rows):
            self.grid[row][result_col] = data[row]
        return data

    def f12(self, col_src: int, col_dummy: int, result_col: int) -> List[int]:
        """Отрицание 1-го аргумента (col_src), col_dummy игнорируется"""
        data = [self.grid[row][col_src] for row in range(self.num_rows)]
        result = [1 if bit == 0 else 0 for bit in data]  # Инверсия
        for row in range(self.num_rows):
            self.grid[row][result_col] = result[row]
        return result

    def f14(self, col_a: int, col_b: int, result_col: int) -> List[int]:
        """Логическое И-НЕ (отрицание конъюнкции)"""
        data_a = [self.grid[row][col_a] for row in range(self.num_rows)]
        data_b = [self.grid[row][col_b] for row in range(self.num_rows)]
        result = [1 if not (a & b) else 0 for a, b in zip(data_a, data_b)]  # И-НЕ
        for row in range(self.num_rows):
            self.grid[row][result_col] = result[row]
        return result

    def binary_addition(self, num_a: List[int], num_b: List[int]) -> List[int]:
        carry = 0
        result = []
        for a, b in zip(reversed(num_a), reversed(num_b)):
            total = a + b + carry
            result.insert(0, total % 2)
            carry = total // 2
        if carry:
            result.insert(0, carry)
        return result

    def process_key_fields(self, key_data: List[int]) -> None:
        found = False
        for col in range(self.num_cols):
            row_data = self.fetch_data_row(col, col, self.num_rows)
            if row_data[:len(key_data)] == key_data:
                found = True
                print(f"Match found in column {col}: {''.join(map(str, row_data))}")

                v_len, ab_len, s_len = 3, 4, 5
                V = row_data[:v_len]
                A = row_data[v_len:v_len + ab_len]
                B = row_data[v_len + ab_len:v_len + 2 * ab_len]
                S = row_data[v_len + 2 * ab_len:v_len + 2 * ab_len + s_len]

                print(f"V (3 bits): {''.join(map(str, V))}")
                print(f"A (4 bits): {''.join(map(str, A))}")
                print(f"B (4 bits): {''.join(map(str, B))}")
                print(f"S (5 bits): {''.join(map(str, S))}")

                sum_ab = self.binary_addition(A, B)
                sum_ab = [0] * (s_len - len(sum_ab)) + sum_ab[:s_len]

                print(f"Sum A+B: {''.join(map(str, sum_ab))}")

                new_row = V + A + B + sum_ab
                new_row += [0] * (self.num_rows - len(new_row))
                self.store_data_row(new_row, col, col)

        if not found:
            print(f"No matches for key: {''.join(map(str, key_data))}")

    def find_closest_values(self, target: List[int]) -> Tuple[int, List[int], int, List[int]]:
        target_adjusted = target + [0] * (self.num_rows - len(target))
        target_adjusted = target_adjusted[:self.num_rows]

        below_cols = []
        above_cols = []

        for col in range(self.num_cols):
            data = self.fetch_data_row(col, col, self.num_rows)
            g = l = 0
            for t, d in zip(target_adjusted, data):
                g_new = g or (not t and d and not l)
                l_new = l or (t and not d and not g)
                g, l = g_new, l_new

            if not g and l:
                below_cols.append(col)
            elif g and not l:
                above_cols.append(col)

        max_below = None
        if below_cols:
            current_cols = below_cols
            for bit_pos in range(self.num_rows):
                next_cols = []
                for col in current_cols:
                    data = self.fetch_data_row(col, col, self.num_rows)
                    if data[bit_pos]:
                        next_cols.append(col)
                if next_cols:
                    current_cols = next_cols
            max_below = current_cols[0] if current_cols else None

        min_above = None
        if above_cols:
            current_cols = above_cols
            for bit_pos in range(self.num_rows):
                next_cols = []
                for col in current_cols:
                    data = self.fetch_data_row(col, col, self.num_rows)
                    if not data[bit_pos]:
                        next_cols.append(col)
                if next_cols:
                    current_cols = next_cols
            min_above = current_cols[0] if current_cols else None

        below_data = self.fetch_data_row(max_below, max_below, self.num_rows) if max_below is not None else []
        above_data = self.fetch_data_row(min_above, min_above, self.num_rows) if min_above is not None else []

        return (max_below, below_data, min_above, above_data)

    def display_grid(self) -> None:
        for row in self.grid:
            print(' '.join(map(str, row)))