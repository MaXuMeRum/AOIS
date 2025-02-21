import unittest

from main import *

class TestBinaryFunctions(unittest.TestCase):

    def test_to_direct_binary(self):
        self.assertEqual(to_direct_binary(5), '00000101')
        self.assertEqual(to_direct_binary(-5), '10000101')
        self.assertEqual(to_direct_binary(0), '00000000')

    def test_to_reverse_binary(self):
        self.assertEqual(to_reverse_binary(5), '00000101')
        self.assertEqual(to_reverse_binary(-5), '11111010')
        self.assertEqual(to_reverse_binary(0), '00000000')

    def test_to_additional_binary(self):
        self.assertEqual(to_additional_binary(5), '00000101')
        self.assertEqual(to_additional_binary(-5), '11111011')
        self.assertEqual(to_additional_binary(0), '00000000')

    def test_add_binary(self):
        self.assertEqual(add_binary('00000101', '00000011'), '00001000')
        self.assertEqual(add_binary('11111011', '00000001'), '11111100')

    def test_binary_to_dec(self):
        self.assertEqual(binary_to_dec('00000101'), 5)
        self.assertEqual(binary_to_dec('11111011'), -5)
        self.assertEqual(binary_to_dec('00000000'), 0)

    def test_subtract_binary(self):
        self.assertEqual(subtract_binary('00001000', '00000101'), '00000011')
        self.assertEqual(subtract_binary('00000101', '00000101'), '00000000')

    def test_multiply_binary(self):
        self.assertEqual(multiply_binary('00000101', '00000011'), '00001111')
        self.assertEqual(multiply_binary('00000010', '00000010'), '00000100')

    def test_divide_binary(self):
        self.assertEqual(divide_binary('00001000', '00000100'), '00000010 (Остаток: 00000000)')
        self.assertEqual(divide_binary('00000100', '00000000'), 'Ошибка: деление на ноль')

    def test_float_to_ieee754(self):
        self.assertEqual(float_to_ieee754(1.0), '00111111100000000000000000000000')
        self.assertEqual(float_to_ieee754(-1.0), '10111111100000000000000000000000')

    def test_ieee754_to_float(self):
        self.assertEqual(ieee754_to_float('01000000000000000000000000000000'), 2.0)
        self.assertEqual(ieee754_to_float('11000000000000000000000000000000'), -2.0)

    def test_add_floating_point(self):
        self.assertEqual(add_floating_point(1.0, 2.0), float_to_ieee754(3.0))
        self.assertEqual(add_floating_point(-1.0, -2.0), float_to_ieee754(-3.0))

if __name__ == '__main__':
    unittest.main()