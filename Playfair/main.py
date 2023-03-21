import os.path
from typing import Tuple, Any

letters = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def build_matrix(k) -> []:
    k_pos = 0  # starting key index
    alf_pos = 65
    m = []  # matrix declaration
    for y in range(5):
        row = []
        while len(row) < 5:
            if k_pos < len(k):
                row.append(k[k_pos])
                k_pos += 1
            else:
                if chr(alf_pos) not in k:
                    row.append(chr(alf_pos))
                alf_pos += 1
                if alf_pos == 74:
                    alf_pos += 1
        m.append(row)
    return m


def find_pos(m, c):
    for i in range(5):
        if c in m[i]:
            list_of_pos = [i, m[i].index(c)]
            return list_of_pos


# if letters in the same row we take the letters on the right
# if letters in the same column we take the letters on the bottom
# if letters not in the same row or column we take letter in the same row
# if letters are the same or one letter left add X behind first
def encryption(m, s) -> str:
    # preparing message to encryption
    # inserting an x bbetween all duplicate letters not necessarily paired
    s_len = len(s)
    pos = 1
    while pos < s_len:
        if s[pos-1] == s[pos]:
            if s[pos] == 'X':
                s = s[:pos] + 'Q' + s[pos:]
            else:
                s = s[:pos] + 'X' + s[pos:]
            s_len = len(s)
        pos += 2
    if len(s) % 2 != 0:
        if s[-1] == 'X':
            s += 'Q'
        else:
            s += 'X'

    # encryption code
    message = ""
    for first in range(0, len(s), 2):
        second = first+1
        list_of_pos = find_pos(m, s[first])
        f_row, f_column = list_of_pos[0], list_of_pos[1]
        list_of_pos = find_pos(m, s[second])
        s_row, s_column = list_of_pos[0], list_of_pos[1]

        if f_row == s_row:
            message += m[f_row][(f_column + 1) % 5]
            message += m[s_row][(s_column + 1) % 5]
        elif f_column == s_column:
            message += m[(f_row + 1) % 5][f_column]
            message += m[(s_row + 1) % 5][s_column]
        else:
            message += m[f_row][s_column]
            message += m[s_row][f_column]

    return message


# if letters in the same row we take the letters on the left
# if letters in the same column we take the letters on the up
# if letters not in the same row or column we take letter in the same column
def decryption(m, s) -> str:
    # decryption code
    message = ""
    for first in range(0, len(s), 2):
        second = first + 1
        f_row, f_column = find_pos(m, s[first])
        s_row, s_column = find_pos(m, s[second])

        if f_row == s_row:
            message += m[f_row][(f_column + 4) % 5]
            message += m[s_row][(s_column + 4) % 5]
        elif f_column == s_column:
            message += m[(f_row + 4) % 5][f_column]
            message += m[(s_row + 4) % 5][s_column]
        else:
            message += m[f_row][s_column]
            message += m[s_row][f_column]

    return message


def check_key(key, alph):
    for k in key:
        if k not in alph:
            return False
    return True


def main():
    # creating simple alphabet to help with algorithm
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    # setting the read from file / keyboard option
    while True:
        answer = input("Want you load data from file? [Y/N]: ").upper()
        if answer in ["Y", "N"]:
            break

    # reading data from user
    if answer == "Y":
        # reading data from file
        # [1] - data
        # [2] - key
        filename = input("Filename: ")
        if os.path.isfile(filename):
            with open(filename) as f:
                lines = f.readlines()
                if len(lines) != 2:
                    print("File has wrong structure!")
                    print("First line should contain the data.")
                    print("Second line should contain the key.")
                    exit()
                data = lines[0].upper()
                key = lines[1].upper()
                if not check_key(key, alphabet) or len(key.split(" ")) != 1:
                    print("The structure of key isn't correct.")
                    print("Key should be one word.")
                    print("Key should contain only letters from english alphabet")
                    exit()
        else:
            print("File doesn't exists")
            exit()
    else:
        data = input("Input data: ").upper()
        while True:
            key = input("Input key: ").upper()
            if check_key(key, alphabet):
                break
            print("Invalid key word. Key word must contains only letters")

    # setting the encryption / decryption option
    while True:
        mode = input("Want you either encrypting [E] or decrypting [D] your data: ").upper()
        if mode in ["E", "D"]:
            break

    # changing J to I in
    data = data.replace('J', 'I')
    key = list(dict.fromkeys(key.replace('J', 'I')).keys())
    tmp = key
    key = ''
    for k in tmp:
        key += k
    print(key)

    # deleting invalid chars from data
    for char in data:
        if char not in alphabet:
            data = data.replace(char, '')

    # creating matrix for playfair algorithm
    matrix = build_matrix(key)

    print(data)
    if mode == 'D':
        print("Encrypted message: ", data)
        data = decryption(matrix, data)
        print("Decrypted message: ", data)
    elif mode == 'E':
        print("Message: ", data)
        data = encryption(matrix, data)
        print("Encrypted message: ", data)

    # setting the save to file option
    while True:
        answer = input("Wanna you save the data in the file? [Y/N]: ").upper()
        if answer in ["Y", "N"]:
            break

    if answer == 'Y':
        filename = input("Filename to save data: ")
        with open(filename, 'w') as f:
            f.write(data + '\n')
            f.write(key)


if __name__ == "__main__":
    main()
