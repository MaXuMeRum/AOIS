from lib import *

# Ввод чисел
x1 = int(input("Введите целое число 1: "))
x2 = int(input("Введите целое число 2: "))

# Прямой код для первого числа (x1)
print("\nЧисло 1: ", x1)
x1_bin = to_direct_binary(x1)
print(f"Прямой код: {x1_bin} ")

# Дополнительный код для первого числа (x1)
x1_add = to_additional_binary(x1)
print(f"Дополнительный код: {x1_add} ")

# Обратный код для первого числа (x1)
x1_rev = to_reverse_binary(x1)
print(f"Обратный код: {x1_rev} ")

# Прямой код для второго числа (x2)
print("\nЧисло 2: ", x2)
x2_bin = to_direct_binary(x2)
print(f"Прямой код: {x2_bin}")

# Дополнительный код для второго числа (x2)
x2_add = to_additional_binary(x2)
print(f"Дополнительный код: {x2_add} ")

# Обратный код для второго числа (x2)
x2_rev = to_reverse_binary(x2)
print(f"Обратный код: {x2_rev} ")

# Сложение в дополнительном коде
print("\nРезультат сложения (в дополнительном коде):")
sum_bin = add_binary(x1_add, x2_add)
sum_decimal = binary_to_dec(sum_bin)
print(f"Результат (в 10-ом формате): {sum_decimal}")

# Вывод обратного и дополнительного кодов для суммы
print(f"Прямой код: {sum_bin}")
print(f"Обратный код: {to_reverse_binary(sum_decimal)}")
print(f"Дополнительный код: {to_additional_binary(sum_decimal)}")

# Вычитание в дополнительном коде
print("\nРезультат вычитания (в дополнительном коде):")
sub_bin = subtract_binary(x1_add, x2_add)
sub_decimal = binary_to_dec(sub_bin)
print(f"Результат (в 10-ом формате): {sub_decimal}")
print(f"Прямой код: {sub_bin}")
print(f"Обратный код: {to_reverse_binary(sub_decimal)}")
print(f"Дополнительный код: {to_additional_binary(sub_decimal)}")

# Умножение в прямом коде
print("\nРезультат умножения (в прямом коде):")
mul_bin = multiply_binary(x1_bin, x2_bin)
mul_decimal = binary_to_dec(mul_bin)
print(f"Результат (в 10-ом формате): {mul_decimal}")
print(f"Прямой код: {mul_bin}")
print(f"Обратный код: {to_reverse_binary(mul_decimal)}")
print(f"Дополнительный код: {to_additional_binary(mul_decimal)}")

# Деление в прямом коде
print("\nРезультат деления (в прямом коде):")
div_result = divide_binary(x1_bin, x2_bin)
print(f"Результат: {div_result}")

# Сложение двух положительных чисел с плавающей точкой
float1 = float(input("\nВведите число с плавающей точкой 1: "))
float2 = float(input("Введите число с плавающей точкой 2: "))
sum_float_bin = add_floating_point(float1, float2)
print(
    f"Сложение {float1} и {float2} в формате IEEE 754: {sum_float_bin} (Десятичный результат: {ieee754_to_float(sum_float_bin)})")

x1_i = float_to_ieee754(x1)
print(f"первый:{x1_i}")
x2_i = float_to_ieee754(x2)
print(f"второй:{x2_i}")
