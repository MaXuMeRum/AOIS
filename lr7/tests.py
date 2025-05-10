import unittest
from unittest.mock import patch
import random
import logging
from main import DiagonalMatrix


class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        # Фиксируем random для предсказуемости тестов
        random.seed(42)
        self.rows = 4
        self.cols = 4
        self.matrix = DiagonalMatrix(self.rows, self.cols)

    def test_initialization(self):
        self.assertEqual(self.matrix.rows, self.rows)
        self.assertEqual(self.matrix.cols, self.cols)
        self.assertEqual(len(self.matrix.matrix), self.rows)
        self.assertEqual(len(self.matrix.matrix[0]), self.cols)
        self.assertEqual(len(self.matrix.bit_columns), self.cols)
        self.assertEqual(len(self.matrix.bit_columns[0]), self.rows)

    def test_random_fill(self):
        # Проверяем, что матрица заполнена 0 и 1
        for row in self.matrix.matrix:
            for val in row:
                self.assertIn(val, [0, 1])

    def test_set_value_valid(self):
        self.matrix.set_value(0, 0, 1)
        self.assertEqual(self.matrix.get_value(0, 0), 1)

        self.matrix.set_value(self.rows - 1, self.cols - 1, 0)
        self.assertEqual(self.matrix.get_value(self.rows - 1, self.cols - 1), 0)

    def test_set_value_invalid(self):
        with self.assertLogs(level='ERROR'):
            self.matrix.set_value(-1, 0, 1)
        with self.assertLogs(level='ERROR'):
            self.matrix.set_value(0, -1, 1)
        with self.assertLogs(level='ERROR'):
            self.matrix.set_value(self.rows, 0, 1)
        with self.assertLogs(level='ERROR'):
            self.matrix.set_value(0, self.cols, 1)

    def test_get_value_valid(self):
        # Поскольку матрица заполняется случайно, проверим хотя бы тип
        val = self.matrix.get_value(0, 0)
        self.assertIn(val, [0, 1])

    def test_get_value_invalid(self):
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.get_value(-1, 0))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.get_value(0, -1))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.get_value(self.rows, 0))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.get_value(0, self.cols))

    @patch('builtins.input', return_value='1')
    def test_get_bit_column_with_input(self, mock_input):
        # Сначала установим конкретные значения для теста
        self.matrix.set_value(0, 0, 1)  # 1 в битовом представлении: 0001
        self.matrix.set_value(1, 0, 0)  # 0 в битовом представлении: 0000
        self.matrix.set_value(2, 0, 1)
        self.matrix.set_value(3, 0, 0)

        bit_column = self.matrix.get_bit_column(0)
        self.assertEqual(bit_column, [0, 0, 0, 0])  # Для бита 1 (второй с конца)

    def test_get_bit_column_with_param(self):
        self.matrix.set_value(0, 0, 1)  # 1 в битовом представлении: 0001
        self.matrix.set_value(1, 0, 0)
        self.matrix.set_value(2, 0, 1)
        self.matrix.set_value(3, 0, 0)

        bit_column = self.matrix.get_bit_column(0, bit_pos=0)
        self.assertEqual(bit_column, [1, 0, 1, 0])  # Для бита 0 (младший бит)

    def test_get_bit_column_invalid(self):
        self.assertIsNone(self.matrix.get_bit_column(-1))
        self.assertIsNone(self.matrix.get_bit_column(self.cols))
        self.assertIsNone(self.matrix.get_bit_column(0, bit_pos=-1))
        self.assertIsNone(self.matrix.get_bit_column(0, bit_pos=self.rows))

    def test_logical_f1_f14_valid(self):
        # Устанавливаем тестовые данные
        for i in range(self.rows):
            self.matrix.set_value(i, 0, 1 if i % 2 == 0 else 0)  # 1, 0, 1, 0
            self.matrix.set_value(i, 1, 1 if i < 2 else 0)  # 1, 1, 0, 0

        and_result, or_result = self.matrix.logical_f1_f14(0, 1)
        self.assertEqual(and_result, [1, 0, 0, 0])
        self.assertEqual(or_result, [1, 1, 1, 0])

    def test_logical_f1_f14_invalid(self):
        and_result, or_result = self.matrix.logical_f1_f14(-1, 0)
        self.assertIsNone(and_result)
        self.assertIsNone(or_result)

        and_result, or_result = self.matrix.logical_f1_f14(0, self.cols)
        self.assertIsNone(and_result)
        self.assertIsNone(or_result)

    def test_logical_f3_f12_valid(self):
        # Устанавливаем тестовые данные
        for i in range(self.rows):
            self.matrix.set_value(i, 0, 1 if i % 2 == 0 else 0)  # 1, 0, 1, 0
            self.matrix.set_value(i, 1, 1 if i < 2 else 0)  # 1, 1, 0, 0

        nand_result, nor_result = self.matrix.logical_f3_f12(0, 1)
        self.assertEqual(nand_result, [0, 1, 1, 1])
        self.assertEqual(nor_result, [0, 0, 0, 1])

    def test_logical_f3_f12_invalid(self):
        nand_result, nor_result = self.matrix.logical_f3_f12(-1, 0)
        self.assertIsNone(nand_result)
        self.assertIsNone(nor_result)

        nand_result, nor_result = self.matrix.logical_f3_f12(0, self.cols)
        self.assertIsNone(nand_result)
        self.assertIsNone(nor_result)

    def test_search_above_found(self):
        # Устанавливаем тестовые данные
        for i in range(self.rows):
            self.matrix.set_value(i, 0, i)

        result = self.matrix.search_above(0, 2, 1)  # Ищем 1 выше строки 2
        self.assertEqual(result, (1, 0))

    def test_search_above_not_found(self):
        for i in range(self.rows):
            self.matrix.set_value(i, 0, i)

        result = self.matrix.search_above(0, 2, 5)  # 5 нет в матрице
        self.assertIsNone(result)

    def test_search_above_invalid(self):
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.search_above(-1, 0, 1))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.search_above(0, -1, 1))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.search_above(self.cols, 0, 1))
        with self.assertLogs(level='ERROR'):
            self.assertIsNone(self.matrix.search_above(0, self.rows, 1))

    def test_search_below_found(self):
        # Устанавливаем тестовые данные
        for i in range(self.rows):
            self.matrix.set_value(i, 0, i)

        result = self.matrix.search_below(0, 1, 3)  # Ищем 3 ниже строки 1
        self.assertEqual(result, (3, 0))

    def test_search_below_not_found(self):
        for i in range(self.rows):
            self.matrix.set_value(i, 0, i)

        result = self.matrix.search_below(0, 2, 1)  # 1 есть, но выше строки 2
        self.assertIsNone(result)

    def test_set_bit_column_valid(self):
        # Устанавливаем битовый столбец
        bit_values = [0, 0, 0, 0]
        self.matrix.set_bit_column(0, 0, bit_values)

        # Проверяем, что биты установились правильно
        for row in range(self.rows):
            self.assertEqual((self.matrix.matrix[row][0] >> 0) & 1, bit_values[row])
            self.assertEqual(self.matrix.bit_columns[0][0], bit_values[row])

    def test_set_bit_column_invalid(self):
        # Просто проверяем, что метод не падает при невалидных данных
        self.matrix.set_bit_column(-1, 0, [1] * self.rows)
        self.matrix.set_bit_column(self.cols, 0, [1] * self.rows)
        self.matrix.set_bit_column(0, -1, [1] * self.rows)
        self.matrix.set_bit_column(0, self.rows, [1] * self.rows)
        self.matrix.set_bit_column(0, 0, [1] * (self.rows + 1))

        # Если мы дошли сюда без исключений - тест пройден
        self.assertTrue(True)

    @patch('builtins.print')
    def test_print_word_valid(self, mock_print):
        self.matrix.set_value(0, 0, 42)
        self.matrix.print_word(0, 0)
        mock_print.assert_called_with(f"Слово в позиции (0, 0): 42")

    @patch('builtins.print')
    def test_print_word_invalid(self, mock_print):
        self.matrix.print_word(-1, 0)
        mock_print.assert_called_with("Ошибка: Неверные индексы")


if __name__ == '__main__':
    unittest.main()