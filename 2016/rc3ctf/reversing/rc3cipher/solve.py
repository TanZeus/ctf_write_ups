#!/usr/bin/env python3

from itertools import cycle, permutations
from binascii import unhexlify, hexlify

xor_key = 'rc3cipherbestcipher'

flag = '1b65380f084b59016875513c6373131d2a6a327172753a2918243d7b181a051e5f1e104c32331c0842777b375f100113'

def build_smaller_chars(biggest_char):

    smaller_chars = [smaller_char for smaller_char in range(biggest_char - 1, -1, -1)]

    v8 = 0
    xor_key_cycle = cycle(xor_key[::-1])

    for smaller_char_index in range(len(smaller_chars)):
        v3 = smaller_chars[smaller_char_index] + v8
        v8 = (v3 + ord(next(xor_key_cycle))) % biggest_char
        v5 = smaller_chars[smaller_char_index]

        smaller_chars[smaller_char_index] = smaller_chars[v8]
        smaller_chars[v8] = v5

    return smaller_chars

def xor_with_smaller_chars(smaller_chars, flag_chars, biggest_char):
    v6 = 0
    v7 = 0

    for flag_char_index in range(len(flag_chars)):
        v6 = (v6 + 1) % biggest_char
        v7 = (smaller_chars[v6] + v7) % biggest_char
        v4 = smaller_chars[v6]

        smaller_chars[v6] = smaller_chars[v7]
        smaller_chars[v7] = v4

        flag_chars[flag_char_index] ^=  smaller_chars[(smaller_chars[v6] + smaller_chars[v7]) % biggest_char]


    return flag_chars


def xor_with_xor_key(flag_chars):
    xor_key_cycle = cycle(xor_key)

    return [flag_char ^ ord(next(xor_key_cycle)) for flag_char in flag_chars]




for biggest_char in range(1, 255):

    smaller_chars = build_smaller_chars(biggest_char)

    # unhex
    xored_with_key = xor_with_xor_key([flag_char for flag_char in unhexlify(flag)])

    xored = xor_with_smaller_chars(smaller_chars, xored_with_key, biggest_char)

    result = ''.join(chr(xor) for xor in xored)

    if 'RC3' in result: print(result)


# RC3-2016-Y0UR-KSA-IS-BAD-@ND-Y0U-SH0ULD-F33L-BAD
