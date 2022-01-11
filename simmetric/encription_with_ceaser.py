def encrypt(text, sdvig):
    encrypted = ""
    for every in text:
        if every.isupper():  # проверка на прописные
            symbol_index = ord(every) - ord('A')
            # сдвиг текущего символа на позицию sdvig
            symbol_shifted = (symbol_index + sdvig) % 26 + ord('A')
            symbol_new = chr(symbol_shifted)
            encrypted += symbol_new
        elif every.islower():  # проверка на нижний регистр
            # вычетаем 'a' для получения нужного диапазона индексов (0-25)
            symbol_index = ord(every) - ord('a')
            symbol_shifted = (symbol_index + sdvig) % 26 + ord('a')
            symbol_new = chr(symbol_shifted)
            encrypted += symbol_new
        elif every.isdigit():
            # верка на число
            symbol_new = (int(every) + sdvig) % 10
            encrypted += str(symbol_new)
        else:
            encrypted += every
    return encrypted


def decrypt(text, sdvig):
    decrypted = ""
    for every in text:
        if every.isupper():
            symbol_dec_index = ord(every) - ord('A')
            # sсдвинуть текущий символ влево на позицию клавиши, чтобы получить его исходное положение
            symbol_dec_pos = (symbol_dec_index - sdvig) % 26 + ord('A')
            symbol_dec_og = chr(symbol_dec_pos)
            decrypted += symbol_dec_og
        elif every.islower():
            symbol_dec_index = ord(every) - ord('a')
            symbol_dec_pos = (symbol_dec_index - sdvig) % 26 + ord('a')
            symbol_dec_og = chr(symbol_dec_pos)
            decrypted += symbol_dec_og
        elif every.isdigit():
            symbol_dec = (int(every) - sdvig) % 10
            decrypted += str(symbol_dec)
        else:
            decrypted += every
    return decrypted


def decrypt_without_key(text):
    for k in range(1, 27):
        decrypted = ""
        for every in text:
            if every.isupper():
                symbol_dec_index = ord(every) - ord('A')
                # sсдвинуть текущий символ влево на позицию клавиши, чтобы получить его исходное положение
                symbol_dec_pos = (symbol_dec_index - k) % 26 + ord('A')
                symbol_dec_og = chr(symbol_dec_pos)
                decrypted += symbol_dec_og
            elif every.islower():
                symbol_dec_index = ord(every) - ord('a')
                symbol_dec_pos = (symbol_dec_index - k) % 26 + ord('a')
                symbol_dec_og = chr(symbol_dec_pos)
                decrypted += symbol_dec_og
            elif every.isdigit():
                symbol_dec = (int(every) - k) % 10
                decrypted += str(symbol_dec)
            else:
                decrypted += every
        print(decrypted)
        if input('Расшифровка верна?\nY/N\n') == 'Y':
            return

while True:
    text = input('Введите текст или exit: ')

    if text=="exit":
        break

    sdvig = int(input('Введите сдвиг: '))
    ch = input('1 - Зашифровать текст \n2 - Расшифровать текст \n3 - Расшифровать подбором\n')
    if ch == '1':
        print(encrypt(text, sdvig))
    elif ch == '2':
        print(decrypt(text, sdvig))
    else:
        decrypt_without_key(text)
