#!/usr/bin/env python3

import random
from math import gcd


def is_prime(n):
    if n < 2:
        return False

    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def next_prime(start, stop):
    n = random.randint(start, stop)
    while not is_prime(n):
        n += 1
    return n


def prim_root(modulo):
    required_set = {num for num in range(1, modulo) if gcd(num, modulo)}
    for g in range(2, modulo):
        generated_set = {pow(g, powers, modulo) for powers in range(1, modulo)}
        if required_set == generated_set:
            return g


def main():
    n = next_prime(100_000, 500_000)
    g = prim_root(n)

    # generation private key x and public key X
    x = random.randint(1_000_000, 8_000_000)
    X = pow(g, x, n)

    # generation private key y and public key Y
    y = random.randint(1_000_000, 8_000_000)
    Y = pow(g, y, n)

    # calculating k - session key
    k_A = pow(Y, x, n)
    k_B = pow(X, y, n)

    assert k_A == k_B

    print(f"Sekret dzielony: {k_A}")


if __name__ == "__main__":
    main()