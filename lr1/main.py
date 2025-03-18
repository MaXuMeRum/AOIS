# Константы для формата IEEE 754
EXPONENT_BIAS = 127  # Смещение экспоненты
MANTISSA_BITS = 23   # Количество бит мантиссы
MANTISSA_MAX_SHIFT = 22  # Максимальный сдвиг для мантиссы

def direct_binary_to_dec(binary: str) -> int:
    """Перевод из прямого кода в десятичный формат."""
    if not binary:
        raise ValueError("Пустая строка не может быть преобразована в число.")

    sign_bit = binary[0]
    magnitude = binary[1:]

    # Переводим двоичное число в десятичное вручную
    decimal = 0
    power = 1
    for bit in reversed(magnitude):
        if bit == '1':
            decimal += power
        power *= 2

    # Учитываем знак
    return -decimal if sign_bit == '1' else decimal


def additional_binary_to_dec(binary: str) -> int:
    """Перевод из дополнительного кода в десятичный формат."""
    sign_bit = binary[0]
    magnitude = binary[1:]

    # Если число отрицательное, инвертируем биты и добавляем 1
    if sign_bit == '1':
        # Инвертируем биты
        inverted = ''
        for bit in magnitude:
            inverted += '1' if bit == '0' else '0'

        # Добавляем 1
        carry = 1
        magnitude_list = list(inverted)
        for i in range(len(magnitude_list) - 1, -1, -1):
            if magnitude_list[i] == '0' and carry == 1:
                magnitude_list[i] = '1'
                carry = 0
                break
            elif magnitude_list[i] == '1' and carry == 1:
                magnitude_list[i] = '0'
        magnitude = ''.join(magnitude_list)

    # Переводим двоичное число в десятичное
    decimal = 0
    power = 1
    for bit in reversed(magnitude):
        if bit == '1':
            decimal += power
        power *= 2

    # Учитываем знак
    return -decimal if sign_bit == '1' else decimal


def to_direct_binary(a: int, bits=8) -> str:
    """Перевод числа в прямой код."""
    if a < 0:
        sign_bit = '1'
        a = -a
    else:
        sign_bit = '0'

    binary = ''
    for _ in range(bits - 1):  # Один бит для знака
        binary = str(a % 2) + binary
        a = a // 2

    # Дополняем нулями
    binary = binary.zfill(bits - 1)
    return sign_bit + binary


def to_reverse_binary(a: int, bits=8) -> str:
    """Перевод числа в обратный код."""
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        direct_code = to_direct_binary(a, bits)
        reverse_code = direct_code[0]  # Знаковый бит
        for bit in direct_code[1:]:
            reverse_code += '1' if bit == '0' else '0'
        return reverse_code


def to_additional_binary(a: int, bits=8) -> str:
    """Перевод числа в дополнительный код."""
    if a >= 0:
        return to_direct_binary(a, bits)
    else:
        reverse_code = to_reverse_binary(a, bits)
        # Добавляем 1 к обратному коду
        carry = 1
        additional_code = list(reverse_code)
        for i in range(len(additional_code) - 1, 0, -1):
            if additional_code[i] == '0' and carry == 1:
                additional_code[i] = '1'
                carry = 0
                break
            elif additional_code[i] == '1' and carry == 1:
                additional_code[i] = '0'
        return ''.join(additional_code)


def add_binary(x: str, y: str, bits=8) -> str:
    """Сложение двух двоичных чисел."""
    result = ''
    carry = 0
    for i in range(bits - 1, -1, -1):
        sum_bits = carry
        sum_bits += 1 if x[i] == '1' else 0
        sum_bits += 1 if y[i] == '1' else 0
        result = ('1' if sum_bits % 2 else '0') + result
        carry = 1 if sum_bits > 1 else 0
    return result


def subtract_binary(x: str, y: str, bits=8) -> str:
    """Вычитание через дополнительный код."""
    y_complement = to_additional_binary(-additional_binary_to_dec(y), bits)
    return add_binary(x, y_complement, bits)


def multiply_binary(a: str, b: str, bits=16) -> str:
    """
    Умножение двух двоичных чисел, представленных в виде строк.
    Результат ограничен `bits` битами.
    """
    # Определение знака результата
    sign = '1' if a[0] != b[0] else '0'  # Знак '-' если знаки разные, иначе '+'

    # Работа с модулями чисел
    a_magnitude = a[1:]
    b_magnitude = b[1:]

    # Функция для сложения двух двоичных чисел
    def add_binary(x: str, y: str) -> str:
        result = []
        carry = 0
        max_len = max(len(x), len(y))
        x = x.zfill(max_len)
        y = y.zfill(max_len)

        for i in range(max_len - 1, -1, -1):
            sum_bits = carry
            sum_bits += 1 if x[i] == '1' else 0
            sum_bits += 1 if y[i] == '1' else 0
            result.insert(0, '1' if sum_bits % 2 else '0')
            carry = 1 if sum_bits > 1 else 0

        if carry:
            result.insert(0, '1')

        return ''.join(result)

    # Функция для умножения двоичных чисел
    result = '0'
    for i in range(len(b_magnitude) - 1, -1, -1):
        if b_magnitude[i] == '1':
            temp = a_magnitude + '0' * (len(b_magnitude) - 1 - i)
            result = add_binary(result, temp)

    # Ограничиваем результат `bits - 1` битами (без учета знакового бита)
    if len(result) > bits - 1:
        result = result[-(bits - 1):]

    # Добавляем знаковый бит
    return sign + result


def divide_binary_code(dividend: str, divisor: str, bits=16) -> tuple:
    """Деление двух двоичных чисел."""
    # Определение знака результата
    sign_quotient = '1' if dividend[0] != divisor[0] else '0'  # Знак '-' если знаки разные, иначе '+'
    sign_remainder = dividend[0]  # Остаток имеет тот же знак, что и делимое

    # Работа с модулями чисел
    dividend_magnitude = dividend[1:]
    divisor_magnitude = divisor[1:]

    # Переводим модули в десятичные числа вручную
    def binary_to_dec(binary: str) -> int:
        decimal = 0
        power = 1
        for bit in reversed(binary):
            if bit == '1':
                decimal += power
            power *= 2
        return decimal

    dividend_dec = binary_to_dec(dividend_magnitude)
    divisor_dec = binary_to_dec(divisor_magnitude)

    # Проверка деления на ноль
    if divisor_dec == 0:
        return "Ошибка: деление на ноль", ""

    # Выполняем деление
    quotient_dec = dividend_dec // divisor_dec
    remainder_dec = dividend_dec % divisor_dec

    # Переводим результат обратно в двоичный формат вручную
    def dec_to_binary(decimal: int, bits: int) -> str:
        binary = ''
        for _ in range(bits):
            binary = str(decimal % 2) + binary
            decimal = decimal // 2
        return binary

    quotient_binary = dec_to_binary(abs(quotient_dec), bits - 1)  # Оставляем место для знакового бита
    remainder_binary = dec_to_binary(abs(remainder_dec), bits - 1)

    # Добавляем знаковые биты
    quotient_binary = sign_quotient + quotient_binary
    remainder_binary = sign_remainder + remainder_binary

    # Возвращаем частное и остаток
    return quotient_binary, remainder_binary


def print_binary_codes(a: int, bits=8):
    """Вывод прямого, обратного и дополнительного кодов числа."""
    print(f"Число введено: {a}")
    print(f"Прямой код: {to_direct_binary(a, bits)}")
    print(f"Обратный код: {to_reverse_binary(a, bits)}")
    print(f"Дополнительный код: {to_additional_binary(a, bits)}")

BIT_COUNT = 32

def convert_to_binary(value):
    """Преобразование числа с плавающей точкой в формат IEEE 754 (32 бита)."""
    if value == 0.0:
        return 0

    sign_bit = 1 if value < 0 else 0
    if sign_bit:
        value = -value

    exponent_field = 0
    while value >= 2.0:
        value /= 2
        exponent_field += 1
    while value < 1.0 and value > 0.0:
        value *= 2
        exponent_field -= 1

    exponent_field += EXPONENT_BIAS
    value -= 1.0

    fraction_part = 0
    for shift in range(MANTISSA_BITS):
        value *= 2
        if value >= 1.0:
            fraction_part |= (1 << (MANTISSA_MAX_SHIFT - shift))
            value -= 1.0

    encoded = (sign_bit << (BIT_COUNT - 1)) | (exponent_field << MANTISSA_BITS) | fraction_part
    display_binary(encoded)
    return encoded


def display_binary(num):
    """Отображение бинарного представления числа с плавающей точкой."""
    sign_bit = (num >> (BIT_COUNT - 1)) & 1
    exponent = (num >> MANTISSA_BITS) & 0xFF
    fraction = num & 0x7FFFFF

    print(f"{sign_bit}  ", end="")
    for pos in range(BIT_COUNT - 2, MANTISSA_MAX_SHIFT, -1):
        print((num >> pos) & 1, end="")
    print("  ", end="")
    for pos in range(MANTISSA_MAX_SHIFT, -1, -1):
        print((num >> pos) & 1, end="")
    print()


def decode_binary(binary_value):
    """Декодирование бинарного представления в число с плавающей точкой."""
    if binary_value == 0:
        return 0.0

    sign_bit = (binary_value >> (BIT_COUNT - 1)) & 1
    exponent_stored = ((binary_value >> MANTISSA_BITS) & 0xFF) - EXPONENT_BIAS
    mantissa_part = binary_value & 0x7FFFFF

    reconstructed_value = 1.0
    for pos in range(MANTISSA_BITS):
        if mantissa_part & (1 << (MANTISSA_MAX_SHIFT - pos)):
            reconstructed_value += (1.0 / (1 << (pos + 1)))

    final_value = reconstructed_value * (2 ** exponent_stored)
    return -final_value if sign_bit else final_value


def binary_addition(num1, num2):
    """Сложение двух чисел с плавающей точкой в формате IEEE 754."""
    exp1 = (num1 >> MANTISSA_BITS) & 0xFF
    exp2 = (num2 >> MANTISSA_BITS) & 0xFF
    frac1 = (num1 & 0x7FFFFF) | (1 << MANTISSA_BITS)
    frac2 = (num2 & 0x7FFFFF) | (1 << MANTISSA_BITS)

    if exp1 > exp2:
        frac2 >>= (exp1 - exp2)
        exp2 = exp1
    elif exp2 > exp1:
        frac1 >>= (exp2 - exp1)
        exp1 = exp2

    result_fraction = frac1 + frac2

    if result_fraction & (1 << (MANTISSA_BITS + 1)):
        result_fraction >>= 1
        exp1 += 1

    result_fraction &= 0x7FFFFF
    result = (exp1 << MANTISSA_BITS) | result_fraction
    display_binary(result)
    return result