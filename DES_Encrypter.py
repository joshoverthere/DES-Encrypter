import os
from bitarray import bitarray
from key_scheduler import KeyScheduler
from operations import permute, s_box


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
    print("input bytes:\t\t", input_bytes.tobytes().hex())
    permuted = permute(input_bytes, "IP")

    # split in two halves
    left = permuted[:32]
    right = permuted[32:]

    # 16 rounds
    for i in range(16):
        expandedRight = permute(right, "EXP")
        # xor it with the round key
        expandedRight ^= scheduler.getkey()
        # 8 S-boxes
        mixedRight = bitarray(endian='big')
        for s in range(8):
            # s = [0,7]
            # s = 0 => chunk = [0:6]
            # s = 7 => chunk = [42:48]
            mixedRight += s_box(expandedRight[s * 6: s * 6 + 6], s)
        # here mixedRight is 32 bit
        mixedRight = permute(mixedRight, "STRAIGHT")

        # now xor with "clean" left part
        left ^= mixedRight

        # swap chunks only if it's not the last round
        if i != 15:
            left, right = right, left

    # we're done. now the final permutation
    output = permute(left + right, "FP")
    print("result:", output.tobytes().hex(" "))
