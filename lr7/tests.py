import unittest
from main import *
import random


class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой матрицы 4x4 с фиксированными значениями"""
        random.seed(42)  # Фиксируем seed для воспроизводимости
        self.dm = DiagonalMatrix(4, 4)

        # Переопределяем матрицу фиксированными значениями для тестов
        self.dm.matrix = [
            [0b11010011, 0b01000011, 0b11010011, 0b01111000],  # 211, 67, 211, 120
            [0b00110111, 0b11010011, 0b01111000, 0b01000101],  # 55, 211, 120, 69
            [0b11110011, 0b01111000, 0b01000101, 0b11010011],  # 243, 120, 69, 211
            [0b10001011, 0b01000101, 0b11010011, 0b01111000]  # 139, 69, 211, 120
        ]

        # Пересчитываем bit_columns для фиксированных значений
        for col in range(4):
            for row in range(4):
                for bit_pos in range(4):
                    self.dm.bit_columns[col][bit_pos] = (self.dm.matrix[row][col] >> bit_pos) & 1

    def test_initialization(self):
        """Тест инициализации матрицы"""
        self.assertEqual(len(self.dm.matrix), 4)
        self.assertEqual(len(self.dm.matrix[0]), 4)
        self.assertEqual(len(self.dm.bit_columns), 4)
        self.assertEqual(len(self.dm.bit_columns[0]), 4)

    def test_set_get_value(self):
        """Тест установки и получения значений"""
        # Корректные значения
        self.dm.set_value(0, 0, 255)
        self.assertEqual(self.dm.get_value(0, 0), 255)

        # Некорректные индексы - теперь с проверкой логов
        with self.assertLogs(level='ERROR') as cm:
            self.dm.set_value(10, 10, 123)
        self.assertIn("Индексы вне диапазона", cm.output[0])

        with self.assertLogs(level='ERROR') as cm:
            self.assertIsNone(self.dm.get_value(10, 10))
        self.assertIn("Индексы вне диапазона", cm.output[0])

    def test_get_bit_column(self):
        """Тест получения разрядного столбца"""
        # Бит 0 в столбце 0: 1,1,1,1 (младшие биты)
        self.assertEqual(self.dm.get_bit_column(0, 0), [1, 1, 1, 1])

    def test_logical_and_simple(self):
        """Минимальный тест для AND"""
        self.dm = DiagonalMatrix(2, 2)
        self.dm.bit_columns[0] = [1, 0]  # Столбец 0
        self.dm.bit_columns[1] = [1, 1]  # Столбец 1

        and_res, _ = self.dm.logical_f1_f14(0, 1)
        self.assertEqual(and_res, [1 & 1, 0 & 1])  # [1, 0]

    def test_search_below_simple(self):
        """Ещё один минимальный тест"""
        # Создаем маленькую матрицу 2x2
        dm = DiagonalMatrix(2, 2)

        # Устанавливаем значение в (1,0)
        dm.set_value(1, 0, 100)

        # Ищем его ниже (0,0)
        self.assertEqual(dm.search_below(0, 0, 100), (1, 0))

    def test_add_fields_condition(self):
        """Тест сложения полей по условию"""
        # Установим конкретные значения Vj
        self.dm.set_value(0, 0, (5 << 6) | (3 << 3) | 2)  # Vj=5, Bj=3, Aj=2
        self.dm.set_value(1, 1, (5 << 6) | (4 << 3) | 1)  # Vj=5, Bj=4, Aj=1

        results = self.dm.add_fields_with_condition(5)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], (0, 0, 2, 3, 5))  # 2+3=5
        self.assertEqual(results[1], (1, 1, 1, 4, 5))  # 1+4=5

        # Проверка для несуществующего Vj
        self.assertEqual(len(self.dm.add_fields_with_condition(10)), 0)

    def test_random_fill(self):
        """Тест случайного заполнения матрицы"""
        test_dm = DiagonalMatrix(4, 4)
        for row in test_dm.matrix:
            for val in row:
                self.assertTrue(0 <= val <= 511)  # 9 бит максимум

        # Проверяем, что битовые столбцы правильно заполнены
        for col in range(4):
            for bit_pos in range(4):
                bit_col = test_dm.get_bit_column(col, bit_pos)
                self.assertEqual(len(bit_col), 4)
                self.assertTrue(all(b in (0, 1) for b in bit_col))

    def test_logical_f3_f12_basic(self):
        """Тест базовой функциональности NAND и NOR операций"""
        # Создаем тестовую матрицу 4x4
        dm = DiagonalMatrix(4, 4)

        # Устанавливаем битовые столбцы для теста
        dm.bit_columns = [
            [1, 0, 1, 0],  # Столбец 0
            [0, 1, 1, 0]  # Столбец 1
        ]

        # Выполняем операции между столбцами 0 и 1
        nand_res, nor_res = dm.logical_f3_f12(0, 1)

        # Проверяем NAND (И-НЕ)
        expected_nand = [~(1 & 0) & 1, ~(0 & 1) & 1, ~(1 & 1) & 1, ~(0 & 0) & 1]
        self.assertEqual(nand_res, expected_nand)

        # Проверяем NOR (ИЛИ-НЕ)
        expected_nor = [~(1 | 0) & 1, ~(0 | 1) & 1, ~(1 | 1) & 1, ~(0 | 0) & 1]
        self.assertEqual(nor_res, expected_nor)

    def test_search_above_basic(self):
        """Тест базового случая поиска значения выше указанной позиции"""
        # Создаем тестовую матрицу 3x3
        dm = DiagonalMatrix(3, 3)
        dm.matrix = [
            [10, 20, 30],
            [40, 50, 60],
            [70, 80, 90]
        ]

        # Ищем значение 40 выше (2,0) - должно найти (1,0)
        result = dm.search_above(0, 2, 40)
        self.assertEqual(result, (1, 0))

        # Ищем значение 10 выше (1,0) - должно найти (0,0)
        result = dm.search_above(0, 1, 10)
        self.assertEqual(result, (0, 0))

    def test_search_above_not_found(self):
        """Тест случая, когда значение не найдено"""
        dm = DiagonalMatrix(3, 3)
        dm.matrix = [
            [10, 20, 30],
            [40, 50, 60],
            [70, 80, 90]
        ]

        # Ищем несуществующее значение
        self.assertIsNone(dm.search_above(0, 2, 100))

        # Ищем выше первой строки (нечего искать)
        self.assertIsNone(dm.search_above(0, 0, 10))

    def test_search_above_duplicates(self):
        """Тест поиска при наличии дубликатов значений"""
        dm = DiagonalMatrix(4, 2)
        dm.matrix = [
            [10, 20],
            [10, 30],
            [20, 10],
            [10, 40]
        ]

        # Должен найти ближайший сверху (для (3,0) это (2,0))
        self.assertEqual(dm.search_above(0, 3, 20), (2, 0))

        # Должен найти первый сверху (для (3,1) это (2,1))
        self.assertEqual(dm.search_above(1, 3, 10), (2, 1))

    def test_search_above_invalid_indices(self):
        """Тест с неверными индексами"""
        dm = DiagonalMatrix(2, 2)

        # Негативные тесты должны проверять возвращаемое значение None
        # и не требуют проверки логов, если используется print

        # Отрицательные индексы
        self.assertIsNone(dm.search_above(-1, 0, 10))

        # Индексы больше размеров
        self.assertIsNone(dm.search_above(0, 5, 10))

        # Оба индекса неверные
        self.assertIsNone(dm.search_above(10, 10, 10))

    def test_search_above_edge_cases(self):
        """Тест граничных случаев"""
        # Матрица 1x1
        dm1 = DiagonalMatrix(1, 1)
        dm1.matrix = [[5]]
        self.assertIsNone(dm1.search_above(0, 0, 5))  # Нечего искать выше

        # Высокая матрица (3x1)
        dm2 = DiagonalMatrix(3, 1)
        dm2.matrix = [[1], [2], [3]]
        self.assertEqual(dm2.search_above(0, 2, 1), (0, 0))

        # Широкая матрица (1x3)
        dm3 = DiagonalMatrix(1, 3)
        dm3.matrix = [[1, 2, 3]]
        self.assertIsNone(dm3.search_above(1, 0, 2))  # Нечего искать выше

if __name__ == '__main__':
    unittest.main()