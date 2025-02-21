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

    quotient = x_dec / y_dec  # Используем обычное деление для дробных чисел
    return to_direct_binary(int(quotient), bits)

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
