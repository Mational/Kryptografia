#!/usr/bin/env python3
"""
This module implements the BBS algorithm and tests it.
"""

import random
import math
import pytest


class TestBBS:
    """
    This class performs tests on the result of the BBS algorithm.
    """
    @pytest.fixture(scope="session", autouse=True)
    def result(self) -> str:
        """
        The function generates the result of the BBS algorithm for tests.
        All tests are performed on the same result of the algorithm.
        :return: reuslt of the BBS algorithm
        """
        yield main()

    def test_separated_bits(self, result: str):
        """
        Separated bits test for pseudo-random numbers generator.
        :param result: result of generator
        :return: information whether the generator has passed the test
        """
        assert 9725 <= result.count("1") <= 10275

    def test_zeros_series(self, result: str):
        """
        Zero-series test for pseudo-random numbers generator.
        :param result: result of generator
        :return: information whether the generator has passed the test
        """
        zeros_series_count = count_series(result, "1")

        assert 2315 <= zeros_series_count[0] <= 2685
        assert 1114 <= zeros_series_count[1] <= 1386
        assert 527 <= zeros_series_count[2] <= 723
        assert 240 <= zeros_series_count[3] <= 384
        assert 103 <= zeros_series_count[4] <= 209
        assert 103 <= zeros_series_count[5] <= 209

    def test_ones_series(self, result: str):
        """
        Series of ones test for pseudo-random numbers generator.
        :param result: result of generator
        :return: information whether the generator has passed the test
        """
        ones_series_count = count_series(result, "0")

        assert 2315 <= ones_series_count[0] <= 2685
        assert 1114 <= ones_series_count[1] <= 1386
        assert 527 <= ones_series_count[2] <= 723
        assert 240 <= ones_series_count[3] <= 384
        assert 103 <= ones_series_count[4] <= 209
        assert 103 <= ones_series_count[5] <= 209

    def test_long_series(self, result: str):
        """
        Long series test for pseudo-random numbers generator.
        :param result: result of generator
        :return: information whether the generator has passed the test
        """
        series = result.split("1")
        series += result.split("0")

        count = 0
        for elem in series:
            if len(elem) >= 26:
                count += 1

        assert count == 0

    def test_poker(self, result: str):
        """
        Poker test for pseudo-random numbers generator.
        :param result: result of generator
        :return: information whether the generator has passed the test
        """
        series_list = []
        for i in range(0, 20000, 4):
            series_list.append(result[i:i+4])

        count_list = [0 for _ in range(16)]
        for elem in series_list:
            count_list[bin_to_dec(int(elem))] += 1
        count_sum = 0

        for elem in count_list:
            count_sum += elem * elem

        x_value = (16/5000) * count_sum - 5000
        assert 2.16 < x_value < 46.17


def bin_to_dec(binary: int) -> int:
    """
    The function converts binary number to decimal number.
    :param binary: binary number
    :return: decimal number
    """
    decimal, i = 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def count_series(txt: str, char: chr) -> []:
    """
    This function count the series of zeros or ones in result string.
    :param txt: string generated by BBS algorithm
    :param char: char by which the function splits txt
    :return: a list with numbers of series with length from 1 and 6+
    """
    values_list = txt.split(char)
    while "" in values_list:
        values_list.remove("")

    count_list = [0 for _ in range(6)]
    for elem in values_list:
        count_list[len(elem) - 1 if len(elem) <= 6 else 5] += 1

    return count_list


def is_prime(number: int) -> bool:
    """
    The function checks whether a number is prime.

    :param number: number
    :return: True or False
    """
    i = 2
    sqrt_n = number**(1/2)
    while i*i <= sqrt_n:
        if number % i == 0:
            return False
        i += 1
    return True


def find_next_prime(number: int) -> int:
    """
    This function finds prime number which is greater or equal to param.
    The function increments param by 4 each iteration.

    :param number: The number from which the function starts looking for a prime number
    :return: prime number
    """
    while not is_prime(number):
        number += 4
    return number


def generate_blum_number() -> int:
    """
    This function generates Blum's number which is the product of p and q.
    p and q are the prime numbers which in result of modulo 4 give 3.

    :return: Generated Blum's number
    """
    p = find_next_prime(4 * random.randint(800_000, 1_400_000) - 1)  # pylint: disable=invalid-name
    q = find_next_prime(4 * random.randint(800_000, 1_400_000) - 1)  # pylint: disable=invalid-name
    return p*q


def find_x0(blum: int) -> int:
    """
    The function finds the value of x0 such that param and x are relatively prime.

    :param blum: prime number
    :return: x0
    """
    while True:
        x0 = random.randint(0, 100000)  # pylint: disable=invalid-name
        if not is_prime(x0):
            continue
        if math.gcd(blum, x0) == 1:
            return x0


def main() -> str:
    """
    The function generates a pseudo-random string of zeros.
    and ones by implementing the BBS algorithm.
    """
    blum_number = generate_blum_number()
    x = find_x0(blum_number)    # pylint: disable=invalid-name
    result = ""
    for _ in range(20_000):
        result += "0" if x % 2 == 0 else "1"
        x = (x**2) % blum_number    # pylint: disable=invalid-name
    print(result)
    return result


if __name__ == "__main__":
    main()
