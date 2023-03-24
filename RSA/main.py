#!usr/bin/python3

import random
import math


def is_prime(number):
    i = 2
    if number < 2:
        return False
    while i*i <= number:
        if number % i == 0:
            return False
        i += 1
    return True


def random_prime(fr, to):
    n = random.randint(fr, to)
    while not is_prime(n):
        n += 1

    return n


def find_e(phi):
    while True:
        e = 113
        if is_prime(e) and math.gcd(e, phi) == 1:
            return e
        e += 2


def encrypt(t, e, n):
    encrypted_message = ""
    for letter in t:
        e_letter = str(pow(ord(letter), e, n))
        for i in e_letter:
            encrypted_message += chr(int(i))
        encrypted_message += " "
    return encrypted_message[:len(encrypted_message)-1].encode('utf-8')


def decrypt(t, d, n):
    # decoding encrypted message and preparing list of encrypted chars
    t = t.decode().split(" ")

    # decryption
    decrypted_text = ""
    for e_letter in t:
        e_code = ""
        for e_frag in e_letter:
            e_code += str(ord(e_frag))

        e_code = pow(int(e_code), d, n)
        decrypted_text += chr(e_code)
    return decrypted_text


def main():
    # generating p, q, n and phi
    p = random_prime(1_000, 9_973)
    q = random_prime(1_000, 9_973)
    n = p * q
    phi = (p - 1) * (q - 1)
    del p, q    # deleting p and q

    # calculating public and private key
    e = find_e(phi)
    d = pow(e, -1, phi)

    # example
    text = "He found his art never progressed when he literally used his sweat and tears."
    print("Text before encryption:", text)
    encrypted_text = encrypt(text, e, n)
    print("Text after encryption:", encrypted_text)
    decrypted_text = decrypt(encrypted_text, d, n)
    print("Text after decryption:", decrypted_text)


if __name__ == "__main__":
    main()
