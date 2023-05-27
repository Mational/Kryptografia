#!/usr/bin/env python3

import time
from Cryptodome.Cipher import AES


def padding(data):
    length = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([length] * length)


def unpadding(data):
    length = data[-1]
    return data[:-length]


def e_ecb(key, _, mess):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(padding(mess))


def d_ecb(key, _, encrypted_mess):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpadding(cipher.decrypt(encrypted_mess))


def e_cbc(key, init_vec, mess):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_mess = b''
    prev_block = init_vec

    for i in range(0, len(mess), AES.block_size):
        block = mess[i:i + AES.block_size]

        if len(block) < AES.block_size:
            block = block.ljust(AES.block_size, b'\x00')

        block = bytes([block[j] ^ prev_block[j] for j in range(AES.block_size)])
        encrypted_block = cipher.encrypt(block)
        encrypted_mess += encrypted_block
        prev_block = encrypted_block

    return encrypted_mess


def d_cbc(key, init_vec, encrypted_mess):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_mess = b''
    prev_block = init_vec

    for i in range(0, len(encrypted_mess), AES.block_size):
        block = encrypted_mess[i:i+AES.block_size]
        decrypted_block = cipher.decrypt(block)
        plaintext_block = bytes([decrypted_block[j] ^ prev_block[j] for j in range(AES.block_size)])
        decrypted_mess += plaintext_block
        prev_block = block
    decrypted_mess = decrypted_mess.rstrip(b'\x00')
    return decrypted_mess


def e_ofb(key, init_vec, mess):
    cipher = AES.new(key, AES.MODE_OFB, iv=init_vec)
    return cipher.encrypt(padding(mess))


def d_ofb(key, init_vec, encrypted_mess):
    cipher = AES.new(key, AES.MODE_OFB, iv=init_vec)
    return unpadding(cipher.decrypt(encrypted_mess))


def e_cfb(key, init_vec, mess):
    cipher = AES.new(key, AES.MODE_CFB, iv=init_vec, segment_size=128)
    return cipher.encrypt(padding(mess))


def d_cfb(key, init_vec, encrypted_mess):
    cipher = AES.new(key, AES.MODE_CFB, iv=init_vec, segment_size=128)
    return unpadding(cipher.decrypt(encrypted_mess))


def e_ctr(key, init_vec, mess):
    cipher = AES.new(key, AES.MODE_CTR, nonce=init_vec[:8])
    return cipher.encrypt(padding(mess))


def d_ctr(key, init_vec, encrypted_mess):
    cipher = AES.new(key, AES.MODE_CTR, nonce=init_vec[:8])
    return unpadding(cipher.decrypt(encrypted_mess))


def main():
    key = b"my 32 bytes key used to ciphered"
    init_vec = b"0123456789abcdef"

    for mode in [[AES.MODE_ECB, "ecb"], [AES.MODE_CBC, "cbc"],
                 [AES.MODE_OFB, "ofb"], [AES.MODE_CFB, "cfb"],
                 [AES.MODE_CTR, "ctr"]]:
        print("Tryb: " + str(mode[1]))
        for file in ["file_s.txt", "file_m.txt", "file_l.txt"]:
            with open(file, "rb") as f:
                message = f.read()
                print("\tPlik: " + file)

                # encrypted
                enc_times = []
                for _ in range(100):
                    time_start = time.perf_counter()
                    encrypted_mess = globals()["e_" + mode[1]](key, init_vec, message)
                    time_stop = time.perf_counter()
                    time_exec = time_stop - time_start
                    enc_times.append(time_exec)
                avg_exec_time = sum(enc_times) / len(enc_times)

                print("\t\tCzas szyfrowania: " + str(avg_exec_time) + " sek")

                # decrypted
                dec_times = []
                for _ in range(100):
                    time_start = time.perf_counter()
                    decrypted_mess = globals()["d_" + mode[1]](key, init_vec, encrypted_mess)
                    time_stop = time.perf_counter()
                    time_exec = time_stop - time_start
                    dec_times.append(time_exec)
                avg_exec_time = sum(dec_times) / len(dec_times)
                print("\t\tCzas deszyfrowania: " + str(avg_exec_time) + " sek")

                # verifying correctness of encryption and decryption
                assert message == decrypted_mess


if __name__ == "__main__":
    main()
