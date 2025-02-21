import struct

def to_direct_binary(a: int, bits=8) -> str:
    """Прямой код."""
    if a < 0:
        sign_bit = '1'
        a = abs(a)
    else:
        sign_bit = '0'

    binary = ''
    for _ in range(bits - 1):  # Один бит для знака
        binary = str(a % 2) + binary
        a //= 2
        if a == 0:
            break

    binary = binary.zfill(bits - 1)  # Дополняем нулями
    return sign_bit + binary

def to_reverse_binary(a: int, bits=8) -> str:
    """Обратный код."""
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        direct_code = to_direct_binary(a, bits)
        reverse_code = direct_code[0] + ''.join('1' if bit == '0' else '0' for bit in direct_code[1:])
        return reverse_code

def to_additional_binary(a: int, bits=8) -> str:
    """Дополнительный код."""
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        reverse_code = to_reverse_binary(a, bits)
        additional_code = add_binary(reverse_code, '0' * (bits - 1) + '1', bits)
        return additional_code

def add_binary(x: str, y: str, bits=8) -> str:
    """Сложение двух двоичных чисел."""
    carry = 0
    result = ""
    for i in range(bits - 1, -1, -1):
        sum_bits = carry
        sum_bits += 1 if x[i] == '1' else 0
        sum_bits += 1 if y[i] == '1' else 0
        result = ('1' if sum_bits % 2 else '0') + result
        carry = 1 if sum_bits > 1 else 0
    return result.zfill(bits)

def binary_to_dec(binary: str) -> int:
    """Двоичное число в десятичное."""
    if binary[0] == '1':  # Отрицательное число
        return -int(''.join('1' if bit == '0' else '0' for bit in binary), 2) - 1
    else:
        return int(binary, 2)

def subtract_binary(x: str, y: str, bits=8) -> str:
    """Вычитание через дополнительный код."""
    y_complement = to_additional_binary(-binary_to_dec(y), bits)
    return add_binary(x, y_complement, bits)

def multiply_binary(x: str, y: str, bits=8) -> str:
    """Умножение двух двоичных чисел."""
    x_dec = binary_to_dec(x)
    y_dec = binary_to_dec(y)
    product = x_dec * y_dec
    return to_direct_binary(product, bits)

def divide_binary(x: str, y: str, bits=8) -> str:
    """Деление двух двоичных чисел."""
    x_dec = binary_to_dec(x)
    y_dec = binary_to_dec(y)

    if y_dec == 0:
        return "Ошибка: деление на ноль"

    quotient = x_dec // y_dec
    remainder = x_dec % y_dec
    return to_direct_binary(quotient, bits) + " (Остаток: " + to_direct_binary(remainder, bits) + ")"

def float_to_ieee754(f: float) -> str:
    """Число с плавающей запятой в IEEE 754."""
    packed = struct.pack('>f', f)
    binary = ''.join(f'{byte:08b}' for byte in packed)
    return binary

def ieee754_to_float(binary: str) -> float:
    """Двоичное представление (IEEE 754) обратно в float."""
    packed = int(binary, 2).to_bytes(4, byteorder='big')
    return struct.unpack('>f', packed)[0]

def add_floating_point(a: float, b: float) -> str:
    """Сложение двух чисел с плавающей точкой по IEEE 754."""
    a_binary = float_to_ieee754(a)
    b_binary = float_to_ieee754(b)
    sum_float = a + b
    sum_binary = float_to_ieee754(sum_float)
    return sum_binary


if __name__ == '__main__':
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
    print(f"Сложение {float1} и {float2} в формате IEEE 754: {sum_float_bin} (Десятичный результат: {ieee754_to_float(sum_float_bin)})")

    x1_i = float_to_ieee754(x1)
    print(f"первый:{x1_i}")
    x2_i = float_to_ieee754(x2)
    print(f"второй:{x2_i}")