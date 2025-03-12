from main import *
# Ввод целых чисел
x1 = int(input("Введите целое число 1: "))
x2 = int(input("Введите целое число 2: "))

# Вывод кодов для первого числа
print("\nЧисло 1:")
print_binary_codes(x1)

# Вывод кодов для второго числа
print("\nЧисло 2:")
print_binary_codes(x2)

# Сложение в дополнительном коде
print("\nРезультат сложения (в дополнительном коде):")
x1_add = to_additional_binary(x1)
x2_add = to_additional_binary(x2)
sum_bin = add_binary(x1_add, x2_add)
sum_dec = additional_binary_to_dec(sum_bin)
print(f"Результат (в 10-ом формате): {sum_dec}")
print(f"Прямой код: {to_direct_binary(sum_dec)}")
print(f"Обратный код: {to_reverse_binary(sum_dec)}")
print(f"Дополнительный код: {to_additional_binary(sum_dec)}")

# Вычитание в дополнительном коде
print("\nРезультат вычитания (в дополнительном коде):")
sub_bin = subtract_binary(x1_add, x2_add)
sub_dec = additional_binary_to_dec(sub_bin)
print(f"Результат (в 10-ом формате): {sub_dec}")
print(f"Прямой код: {to_direct_binary(sub_dec)}")
print(f"Обратный код: {to_reverse_binary(sub_dec)}")
print(f"Дополнительный код: {to_additional_binary(sub_dec)}")

# Умножение в прямом коде
print("\nРезультат умножения (в прямом коде):")
x1_bin = to_direct_binary(x1)
x2_bin = to_direct_binary(x2)
mul_bin = multiply_binary(x1_bin, x2_bin)
mul_dec = direct_binary_to_dec(mul_bin)
print(f"Результат (в 10-ом формате): {mul_dec}")
print(f"Прямой код: {mul_bin}")
print(f"Обратный код: {to_reverse_binary(mul_dec)}")
print(f"Дополнительный код: {to_additional_binary(mul_dec)}")

# Деление в прямом коде
print("\nРезультат деления (в прямом коде):")
x1_bin = to_direct_binary(x1)
x2_bin = to_direct_binary(x2)
quotient_bin, remainder_bin = divide_binary_code(x1_bin, x2_bin)
if quotient_bin == "Ошибка: деление на ноль":
    print(quotient_bin)
else:
    quotient_dec = direct_binary_to_dec('0' + quotient_bin)  # Добавляем знаковый бит
    remainder_dec = direct_binary_to_dec('0' + remainder_bin)  # Добавляем знаковый бит
    print(f"Результат (в 10-ом формате): {quotient_dec}")
    print(f"Прямой код: {to_direct_binary(quotient_dec)}")
    print(f"Обратный код: {to_reverse_binary(quotient_dec)}")
    print(f"Дополнительный код: {to_additional_binary(quotient_dec)}")
    print(f"Остаток (в 10-ом формате): {remainder_dec}")
    print(f"Прямой код остатка: {to_direct_binary(remainder_dec)}")
    print(f"Обратный код остатка: {to_reverse_binary(remainder_dec)}")
    print(f"Дополнительный код остатка: {to_additional_binary(remainder_dec)}")

# Ввод чисел с плавающей точкой
num1 = float(input("Введите число 1 (с плавающей точкой): "))
num2 = float(input("Введите число 2 (с плавающей точкой): "))

print(f"Число {num1} в бинарном представлении:")
encoded_num1 = convert_to_binary(num1)

# Декодирование бинарного представления обратно в число
decoded_num1 = decode_binary(encoded_num1)
print(f"Декодированное число: {decoded_num1}")

print(f"Число {num2} в бинарном представлении:")
encoded_num2 = convert_to_binary(num2)

# Сложение двух чисел с плавающей точкой
print("\nРезультат сложения:")
sum_encoded = binary_addition(encoded_num1, encoded_num2)
sum_decoded = decode_binary(sum_encoded)
print(f"Результат сложения (в 10-ом формате): {sum_decoded}")