#!usr/bin/env python3

import hashlib as hl
import time
import random


def hash_md5(text):
    text = text.encode("utf-8")
    result = hl.md5(text)
    return result.hexdigest()


def hash_sha_1(text):
    text = text.encode("utf-8")
    result = hl.sha1(text)
    return result.hexdigest()


def hash_sha_224(text):
    text = text.encode("utf-8")
    result = hl.sha224(text)
    return result.hexdigest()


def hash_sha_256(text):
    text = text.encode("utf-8")
    result = hl.sha256(text)
    return result.hexdigest()


def hash_sha_384(text):
    text = text.encode("utf-8")
    result = hl.sha384(text)
    return result.hexdigest()


def hash_sha_512(text):
    text = text.encode("utf-8")
    result = hl.sha512(text)
    return result.hexdigest()


def hash_sha_3_224(text):
    text = text.encode("utf-8")
    result = hl.sha3_224(text)
    return result.hexdigest()


def hash_sha_3_256(text):
    text = text.encode("utf-8")
    result = hl.sha3_256(text)
    return result.hexdigest()


def hash_sha_3_384(text):
    text = text.encode("utf-8")
    result = hl.sha3_384(text)
    return result.hexdigest()


def hash_sha_3_512(text):
    text = text.encode("utf-8")
    result = hl.sha3_512(text)
    return result.hexdigest()


def test_time_of_hash(func, text, info):
    start = time.process_time()
    for _ in range(100_000):
        result = func(text)
    end = time.process_time()

    print("-" * 30, info, "-" * 30)
    print("Długość łańcucha wynikowego:", len(result))
    print("Czas wykonania:", (end - start) * 10 ** 3, "ms")


def print_all_results(text):
    print("-" * 50, "  MD5  ", "-" * 50)
    print("MD5:", hash_md5(text))
    print("-" * 50, " SHA-1 ", "-" * 50)
    print("SHA-1:", hash_sha_1(text))
    print("-" * 50, " SHA-2 ", "-" * 50)
    print("SHA-224:", hash_sha_224(text))
    print("SHA-256:", hash_sha_256(text))
    print("SHA-384:", hash_sha_384(text))
    print("SHA-512:", hash_sha_512(text))
    print("-" * 50, " SHA-3 ", "-" * 50)
    print("SHA-3-224:", hash_sha_3_224(text))
    print("SHA-3-256:", hash_sha_3_256(text))
    print("SHA-3-384:", hash_sha_3_384(text))
    print("SHA-3-512:", hash_sha_3_512(text))
    print('\n')


def test_all_hash(text):
    test_time_of_hash(hash_md5, text, "MD5")
    test_time_of_hash(hash_sha_1, text, "SHA-1")
    test_time_of_hash(hash_sha_224, text, "SHA-224")
    test_time_of_hash(hash_sha_256, text, "SHA-256")
    test_time_of_hash(hash_sha_384, text, "SHA-384")
    test_time_of_hash(hash_sha_512, text, "SHA-512")
    test_time_of_hash(hash_sha_3_224, text, "SHA-3-224")
    test_time_of_hash(hash_sha_3_256, text, "SHA-3-256")
    test_time_of_hash(hash_sha_3_384, text, "SHA-3-384")
    test_time_of_hash(hash_sha_3_512, text, "SHA-3-512")


def find_collisions():
    hash_dict = {}
    bits = 12
    chars = bits // 4

    while True:
        rand_str = str(random.random())
        hash_val = hash_sha_256(rand_str)

        if hash_val[:chars] in hash_dict:
            print("Znaleziono kolizję na pierwszych 12 bitach:", hash_val[:chars])
            print("String 1:", rand_str, "-", hash_sha_256(rand_str))
            print("String 2:", hash_dict[hash_val[:chars]], "-", hash_sha_256(hash_dict[hash_val[:chars]]))
            break
        else:
            hash_dict[hash_val[:chars]] = rand_str


def sac_test():
    input_str = "Hello, world!"
    hash_func = hl.md5
    original_hash = hash_func(input_str.encode()).hexdigest()
    num_tests = 100  # liczba testów
    num_changed_bits = 1  # liczba zmienionych bitów na wejściu
    passed_tests = 0
    for i in range(num_tests):
        modified_input = bytearray(input_str.encode())
        idx = random.randint(0, len(input_str) * 8 - 1)
        modified_input[idx // 8] ^= 1 << (idx % 8)
        modified_hash = hash_func(modified_input).hexdigest()
        original_bits = hash_to_bin(original_hash)
        modified_bits = hash_to_bin(modified_hash)
        counter = 0
        for i in range(len(original_bits)):
            if original_bits[i] != modified_bits[i]:
                counter += 1
        half_len = len(original_bits) / 2
        error = len(original_bits) * 0.1
        if half_len - error <= counter <= half_len + error:
            passed_tests += 1
    print("Spełnione testy SAC [0.4 - 0.6]:", passed_tests, "/", num_tests)


def hash_to_bin(hash):
    result_bin = ""
    for c in hash:
        result_bin += bin(int(str(c), 16))[2:].zfill(4)
    return result_bin


def main():
    # text = input("Podaj tekst do hashowania: ")
    # print_all_results(text)

    # text = "DOM"
    # test_all_hash(text)

    # Test dla pojedynczego zdania.
    text = "KRÓTKOFALÓWKA"
    test_all_hash(text)

    # 3.
    # hash_val = hash_md5("Test")
    # print(hash_val)

    # 5.
    # find_collisions()

    # 6.
    # sac_test()


if __name__ == "__main__":
    main()
