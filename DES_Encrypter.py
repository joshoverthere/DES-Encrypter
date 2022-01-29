# DES Rules:
# not a fkn clue time to read wikipedia

import os
from bitarray import bitarray
from key_scheduler import KeyScheduler
from operations import permute


def clear_console():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


if __name__ == "__main__":
    key = ""
    plain_text = ""
    while len(key) != 8:
        key = input("insert a 64 bit key: ")
    while len(plain_text) != 8:
        plain_text = input("insert a 64 bit plain text: ")

    # init key scheduler
    scheduler = KeyScheduler(key)

    # initial permutation
    input_bytes = bitarray(endian='big')
    input_bytes.frombytes(plain_text.encode())
    print("input bits:\t\t", input_bytes)
    permuted = permute(input_bytes, "IP")
    print("permuted bits:\t", permuted)
