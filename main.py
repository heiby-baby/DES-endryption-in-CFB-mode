# Лабораторная работа № 4 (Режимы шифра  DES)
# Задание №4.2
# Реализовать стандарт шифрования данных DES в режиме «Обратная связь по шифру».


AddedSymbol = ''
left_shifts = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

# Таблица для сжатия ключа до 56 бит
PC1 = (57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4)

# # Таблица для сжатия ключей Фейстеля до 48 бит
PC2 = (14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32)

#  Начальная перестановка IP
IP = (58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7)

# Функция расширения r (32 bits) in 48 bits
E = (32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1)

# Преобразования
SBOX = {
    0: ((14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13)),

    1: ((15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9)),

    2: ((10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12)),

    3: ((7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14)),

    4: ((2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3)),

    5: ((12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13)),

    6: ((4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12)),

    7: ((13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11))
}

# Перестановка r_n в фейстеле
P = (16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25)

# Обратная перестановка IP
IP_FINAL = (40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25)


def stoi(s):
    s = s.encode()
    return int(s.hex(), 16)


# Преобразование целого числа в двоичный, сохраняя ведущие нули
def binary(i, length):
    return bin(i)[2:].zfill(length)


def split(block_bin: str):
    middle = len(block_bin) // 2
    first_half = block_bin[:middle]
    second_half = block_bin[middle:]
    return first_half, second_half


def permute(binary_block, table):
    result = ""
    for i in range(len(table)):
        result += str((binary_block[table[i] - 1]))
    return result


def shift_left(lst, shift_by):
    length = len(lst)
    shift_by %= length  # Обработка случая, если сдвиг больше длины списка
    shifted_list = lst[shift_by:] + lst[:shift_by]
    return shifted_list


def strXOR(str1, str2):
    result = ""
    for i, j in zip(str1, str2):
        result += str(int(i) ^ int(j))
    return result


def gen_key(key: str):
    keys = []
    key = binary(stoi(key[:7]), 64)

    # 56 bits
    key = permute(key, PC1)
    #16 keys
    for i in left_shifts:
        l, r = split(key)
        l = shift_left(list(l), i)
        r = shift_left(list(r), i)
        key = "".join(l) + "".join(r)
        # 48 bits
        keys.append(permute(key, PC2))
    return keys


def crypt(m, key, VecInit, encrypt = True):
    global AddedSymbol
    result = ""
    keys = gen_key(key)

    #Приводим вектор инициализации в бинарный вид
    VecInit = VecInit[:8]
    VecInit = binary(stoi(VecInit), 64)

    if(encrypt == True):
        for i in range(0, len(m), 8):
            block = m[i:i + 8]
            if (len(block) != 8):
                AddedSymbol = str(8 - len(block))
                for i in range(len(block), 8):
                    block += AddedSymbol;
            block = binary(stoi(block), 64)
            #шифруем вектор инициализации
            VecInit = des(VecInit, keys)
            #ксорим по модулю 2
            VecInit = strXOR(VecInit, block)
            result += VecInit
    else:
        for i in range(0, len(m), 64):
            block = m[i:i + 64]
            # расшифровываем вектор инициализации
            VecInit = des(VecInit, keys)
            # ксорим по модулю 2
            VecInit = strXOR(VecInit, block)
            # добавляем расшифрованный блок к результату
            result += VecInit
            # обновляем вектор инициализации
            VecInit = block
    return result

#Так же отличие CFB от ECB в том что ключи реверсать не надо
def des(block, keys):
    block = permute(block, IP)
    l, r = split(block)
    for i in keys:
        preR = ""
        r_i_and_key = strXOR(permute(r, E), i)
        # 8 групп по 6 бит
        grups = [list(), list()]
        for j in range(0, len(r_i_and_key), 6):
            grups[0].append(r_i_and_key[j] + r_i_and_key[j + 5])  # row
            grups[1].append(r_i_and_key[j + 1:j + 5])  # col
        # перестановки фейстеля
        for j in range(0, 8):
            row = int(grups[0][j], 2) - 1
            col = int(grups[1][j], 2) - 1
            preR += (bin(SBOX[j][row][col])[2:]).zfill(4)
        preR = permute(preR, P)
        r, l = strXOR(l, preR), r

    block = r + l
    block = permute(block, IP_FINAL)
    return block

if __name__ == "__main__":
    # only askii chars
    text = "world hello"
    #using only 7 first letters (key - 56 bit)
    key = "vfsdfdsfdsfdsf"

    VecInit = "VectorIn"

    encrypted_text = crypt(text, key, VecInit)
    decrypted_text = crypt(encrypted_text, key, VecInit, False)
    print("Зашифрованный текст:", hex(int(encrypted_text,2))[2:])
    print("Расшифрованный текст:",
          bytes.fromhex(hex(int(decrypted_text, 2))[2:]).decode('utf-8') if AddedSymbol == '' else (bytes.fromhex(
              hex(int(decrypted_text, 2))[2:]).decode('utf-8'))[:-int(AddedSymbol)])
