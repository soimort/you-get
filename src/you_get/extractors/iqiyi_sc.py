#!/usr/bin/env python
import binascii
import math
import time

M = [1732584193, -271733879]
M.extend([~M[0], ~M[1]])
I_table = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21]
C_base = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8388608, 432]


def L(n, t):
    if t is None:
        t = 0
    return trunc(((n >> 1) + (t >> 1) << 1) + (n & 1) + (t & 1))


def rshift(val, n):
    return val >> n if val >= 0 else (val+0x100000000) >> n


def trunc(n):
    n = n % 0x100000000
    if n > 0x7fffffff:
        n -= 0x100000000
    return n


def gen_sc(tvid, Z):
    def transform(string, mod):
        num = int(string, 16)
        return (num >> 8 * (i % 4) & 255 ^ i % mod) << ((a & 3) << 3)

    C = list(C_base)
    o = list(M)
    k = str(Z - 7)
    for i in range(13):
        a = i
        C[a >> 2] |= ord(k[a]) << 8 * (a % 4)

    for i in range(16):
        a = i + 13
        start = (i >> 2) * 8
        r = '03967743b643f66763d623d637e30733'
        C[a >> 2] |= transform(''.join(reversed(r[start:start + 8])), 7)

    for i in range(16):
        a = i + 29
        start = (i >> 2) * 8
        r = '7038766939776a32776a32706b337139'
        C[a >> 2] |= transform(r[start:start + 8], 1)

    for i in range(9):
        a = i + 45
        if i < len(tvid):
            C[a >> 2] |= ord(tvid[i]) << 8 * (a % 4)

    for a in range(64):
        i = a
        I = i >> 4
        C_index = [i, 5 * i + 1, 3 * i + 5, 7 * i][I] % 16 + rshift(a, 6)
        m = L(
                L(
                    o[0],
                    [
                        trunc(o[1] & o[2]) | trunc(~o[1] & o[3]),
                        trunc(o[3] & o[1]) | trunc(~o[3] & o[2]),
                        o[1] ^ o[2] ^ o[3],
                        o[2] ^ trunc(o[1] | ~o[3])
                    ][I]
                ),
                L(
                    trunc(int(abs(math.sin(i + 1)) * 4294967296)),
                    C[C_index] if C_index < len(C) else None
                )
            )
        I = I_table[4 * I + i % 4]
        o = [
                o[3],
                L(o[1], trunc(trunc(m << I) | rshift(m, 32 - I))),
                o[1],
                o[2],
            ]

    new_M = [L(o[0], M[0]), L(o[1], M[1]), L(o[2], M[2]), L(o[3], M[3])]
    s = [new_M[a >> 3] >> (1 ^ a & 7) * 4 & 15 for a in range(32)]
    return binascii.hexlify(bytes(s))[1::2]

if __name__ == '__main__':
    print(gen_sc("494496100", 1466495259194))
    print(gen_sc("397768800", 1466795077775))
    print(gen_sc("397768800", 1466796325746))
