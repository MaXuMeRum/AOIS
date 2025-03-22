import unittest
from main import *

class TestBinaryOperations(unittest.TestCase):

    def test_direct_binary_to_dec(self):
        self.assertEqual(direct_binary_to_dec("00000101"), 5)
        self.assertEqual(direct_binary_to_dec("00000000"), 0)

    def test_additional_binary_to_dec(self):
        self.assertEqual(additional_binary_to_dec("00000101"), 5)
        self.assertEqual(additional_binary_to_dec("00000000"), 0)

    def test_to_direct_binary(self):
        self.assertEqual(to_direct_binary(5), "00000101")
        self.assertEqual(to_direct_binary(0), "00000000")

    def test_to_reverse_binary(self):
        self.assertEqual(to_reverse_binary(5), "00000101")
        self.assertEqual(to_reverse_binary(0), "00000000")

    def test_to_additional_binary(self):
        self.assertEqual(to_additional_binary(5), "00000101")
        self.assertEqual(to_additional_binary(0), "00000000")

    def test_add_binary(self):
        self.assertEqual(add_binary("00000101", "00000001"), "00000110")
        self.assertEqual(add_binary("11111011", "11111111"), "11111010")
        self.assertEqual(add_binary("11111111", "11111111"), "11111110")

    def test_subtract_binary(self):
        self.assertEqual(subtract_binary("00000101", "00000001"), "00000100")
        self.assertEqual(subtract_binary("11111011", "00000101"), "11110110")
        self.assertEqual(subtract_binary("11111111", "11111111"), "00000000")

    def test_multiply_binary(self):
        self.assertEqual(multiply_binary("00000101", "00000101"), "0000011001")
        self.assertEqual(multiply_binary("11111011", "11111111"), "011110100000101")

    def test_divide_binary_code(self):
        quotient, remainder = divide_binary_code("00000101", "00000001")
        self.assertEqual(quotient, "0000000000000101")
        self.assertEqual(remainder, "0000000000000000")

        quotient, remainder = divide_binary_code("00000101", "00000101")
        self.assertEqual(quotient, "0000000000000001")
        self.assertEqual(remainder, "0000000000000000")

    def test_convert_to_binary(self):
        # Тестируем преобразование чисел с плавающей точкой в IEEE 754
        self.assertEqual(convert_to_binary(3231711232), 1329635328)

    def test_decode_binary(self):
        # Тестируем декодирование бинарных чисел в числа с плавающей точкой
        self.assertEqual(decode_binary(0b01000000000000000000000001000000), 2.0000152587890625)
        self.assertEqual(decode_binary(0b11000000000000000000000001000000), -2.0000152587890625)

    def test_binary_addition(self):
        # Тестируем сложение чисел с плавающей точкой
        num11 = 0b01000000000000000000000001000000  # 5.0
        num21 = 0b01000000000000000000000000100000  # 2.0
        result = binary_addition(num11, num21)
        self.assertEqual(decode_binary(result), 4.000022888183594)
