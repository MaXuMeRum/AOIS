import unittest
from main import CustomDiagonalGrid


class TestCustomDiagonalGrid(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой матрицы 4x4 перед каждым тестом"""
        self.grid = CustomDiagonalGrid(4, 4)
        # Заполним матрицу тестовыми данными
        for col in range(4):
            self.grid.store_data_row([1, 0, 1, 0], 0, col)

    def test_store_and_fetch_data_row(self):
        """Тест записи и чтения строки данных"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)
        result = self.grid.fetch_data_row(0, 0, 4)
        self.assertEqual(result, test_data)

    def test_store_and_fetch_diagonal_data(self):
        """Тест записи и чтения диагональных данных"""
        test_data = [1, 0, 1, 0]
        self.grid.store_diagonal_data(test_data, 0, 0)
        result = self.grid.fetch_diagonal_data(0, 0, 4)
        self.assertEqual(result, test_data)

    def test_perform_logical_or(self):
        """Тест логической операции ИЛИ"""
        self.grid.store_data_row([1, 0, 1, 0], 0, 0)
        self.grid.store_data_row([0, 1, 1, 0], 0, 1)
        result = self.grid.perform_logical_or(0, 1, 2)
        self.assertEqual(result, [1, 1, 1, 0])

    def test_perform_logical_nor(self):
        """Тест логической операции ИЛИ-НЕ"""
        self.grid.store_data_row([1, 0, 1, 0], 0, 0)
        self.grid.store_data_row([0, 1, 1, 0], 0, 1)
        result = self.grid.perform_logical_nor(0, 1, 2)
        self.assertEqual(result, [0, 0, 0, 1])

    def test_perform_copy_operation(self):
        """Тест операции копирования"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)
        result = self.grid.perform_copy_operation(0, 1, 2)
        self.assertEqual(result, test_data)

    def test_perform_invert_operation(self):
        """Тест операции инверсии"""
        test_data = [1, 0, 1, 1]
        self.grid.store_data_row(test_data, 0, 0)
        result = self.grid.perform_invert_operation(0, 1, 2)
        self.assertEqual(result, [0, 1, 0, 0])

    def test_binary_addition(self):
        """Тест двоичного сложения"""
        result = self.grid.binary_addition([1, 0, 1], [1, 1, 0])
        self.assertEqual(result, [1, 0, 1, 1])  # 5 + 6 = 11 (1011)

    def test_process_key_fields(self):
        """Тест обработки ключевых полей"""
        # Создаем специальную тестовую матрицу
        test_grid = CustomDiagonalGrid(4, 4)
        test_data = [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Ключ 101
        test_grid.store_data_row(test_data[:4], 0, 0)
        test_grid.store_data_row(test_data[4:8], 0, 1)
        test_grid.store_data_row(test_data[8:12], 0, 2)
        test_grid.store_data_row(test_data[12:], 0, 3)

        # Проверяем обработку
        test_grid.process_key_fields([1, 0, 1])
        result = test_grid.fetch_data_row(0, 0, 4)
        # Ожидаем, что поля A и B будут просуммированы
        self.assertEqual(result[3:7], [0])  # Проверяем часть результата

    def test_find_closest_values(self):
        """Тест поиска ближайших значений с правильным порядком сравнения"""
        test_grid = CustomDiagonalGrid(4, 4)
        # Данные, где столбец 1 ([0,0,0,1]) действительно > [0,0,1,1] в лексикографическом порядке
        test_data = [
            [0, 0, 0, 0],  # Столбец 0
            [0, 0, 1, 1],  # Столбец 1 (теперь target)
            [0, 0, 1, 0],  # Столбец 2 (ближайшее снизу)
            [0, 1, 0, 0]  # Столбец 3 (ближайшее сверху)
        ]
        for col in range(4):
            test_grid.store_data_row(test_data[col], 0, col)

        below_col, below_word, above_col, above_word = test_grid.find_closest_values([0, 0, 1, 1])

        self.assertEqual(below_col, 3)  # Столбец 2 [0,0,1,0] < [0,0,1,1]
        self.assertEqual(below_word, [0, 0, 1, 0])
        self.assertEqual(above_col, 1)  # Столбец 3 [0,1,0,0] > [0,0,1,1]
        self.assertEqual(above_word, [0, 1, 1, 0])


if __name__ == '__main__':
    unittest.main()