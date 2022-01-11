from random import randint


def encrypt(text):
    many_keys = ''
    result = ''
    for symbol in text:
        every_key = randint(0, 32)
        many_keys += str(every_key) + "/"
        result += chr((ord(symbol) + every_key - 17) % 33 + ord('А'))
    return result,many_keys

def decrypt(many_keys,result):
    text=''
    for i, symbol in enumerate(result):
        if many_keys[i] != '':
            text += chr((ord(symbol) - int(many_keys[i]) - 17) % 33 + ord('А'))
    return text

while True:
    text = input("Введите текст или exit: ")
    if text=='exit':
        break
    text = text.upper()
    many_keys,result = encrypt(text)
    print('Зашифрованный текст: ', result)
    print('Ключ шифрования: ', many_keys)

    print('Введите зашифрованный текст: ')
    result = input()
    print('Введите ключ шифрования: ')
    many_keys = input().split('/')
    print('Расшифрованное сообщение : ', decrypt(many_keys,result))
