
from processor.sorm.constants import Const



def printableBytes(b):
    '''
    Perpesent bytes stream as hex-encoded bytes string.

    b: byte stream

    Example:
        >>> a = b'abc123\x10\x00\xaa\xcf'
        >>> printableBytes(a)
        '61 62 63 31 32 33 10 00 AA CF'
    '''
    return ' '.join(['{:02X}'.format(x) for x in bytes(b)])

def strBytes(b):
    '''
    Perpesent bytes stream as string.

    b: byte stream

    Example:
        >>> a = b'abc123\x10\x00\xaa\xcf'
        >>> printableBytes(a)
        '61 62 63 31 32 33 10 00 AA CF'
    '''
    return str(b)


def bcd2int(b):
    '''
    Convert BCD encoded number to standard integer number

    Used LE notation from order 268:
    | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    |   Cipher 2    |   Cipher 1    |

    Args:   byte(b) - BCD encoded byte
    Return: int(i) - integer number
    '''
    #~ return ((b >> 4) * 10) + (b & 0x0F) # [C1, C2] decode variant
    return ((b & 0x0F) * 10) + (b >> 4) # [C2, C1] decode variant by order 268


def int2bcd(i):
    '''
    Convert integer number to BCD encoded

    Used LE notation from order 268:
    | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    |   Cipher 2    |   Cipher 1    |

    Args:   int(i) - integer number
    Return: byte(b) - BCD encoded byte
    '''
    #~ return ((i // 10) << 4) + (i % 10) # [C1, C2] encode variant
    return ((i % 10) << 4) + (i // 10) # [C2, C1] encode variant by order 268


def bcd2phone(b):
    '''
    Convert BCD to phone number

    Used LE notation from order 268:
    | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    |   Cipher 2    |   Cipher 1    |
    |   Cipher 4    |   Cipher 3    |
    ...
    |   Cipher N    |   Cipher N-1  |

    where unused ciphers encoded as 0xFF

    Args:   bytes(b) - BCD encoded phone number
    Return: str(b) - phone number
    '''
    r = ''
    for x in b:
        if x & 0xF0 != 0xF0: # Full byte with C1 and C2
            xi = ((x & 0x0F) * 10) + (x >> 4)
            sx = str(xi)
            r += sx if len(sx) == 2 else '0' + sx
        elif x & 0xF0 == 0xF0 and x != 0xFF: # Half byte only with C1
            xi = x & 0x0F
            r += str(xi)
    return r


def phone2bcd(s):
    '''
    Convert phone number to BCD encoded

    Used LE notation from order 268:
    | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
    |   Cipher 2    |   Cipher 1    |
    |   Cipher 4    |   Cipher 3    |
    ...
    |   Cipher N    |   Cipher N-1  |

    where unused ciphers encoded as 0xFF

    Args:   str(s) - phone number
    Return: bytes(b) - BCD encoded phone number
    '''
    r = []
    for x in range(0, Const.PHONE_LENGTH_IN_BYTES * 2, 2):
        k = s[x:x+2]
        kl = len(k)
        if kl == 2: # No padding
            ik = int(k)
            r.append(((ik % 10) << 4) + (ik // 10))
        elif kl == 1: # Need padding
            ik = int(k)
            r.append(ik + 0xF0)
        elif kl == 0: # Full padded byte
            r.append(0xFF)
        else:
            raise ValueError('What a hell why length of k is {}???'.format(kl))
    return bytes(r)


def splitStreamAndLine(b):
    '''
    Split stream number and control line number from byte field as described in
    order 268 appendix 6 paragraph 4.4.3:

    |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
    |  Stream number  |     Control line number     |

    Args:   byte(b) - encoded byte
    Return: tuple(s, n), where:
            int(s) - stream number;
            int(n) - control line number
    '''
    s = b >> 5
    n = b & 0x1F
    return s, n


def mergeStreamAndLine(s, n):
    '''
    Merge stream number and control line number in one byte field as described in
    order 268 appendix 6 paragraph 4.4.3:

    |  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  |
    |  Stream number  |     Control line number     |

    Args:   int(s) - stream number
            int(n) - control line number
    Return: byte(b)
    '''
    return (s << 5) + n


def int2bitarray(i):
    '''
    Convert one byte integer to bits array

    Args:   int(b) - one byte length integer
    Return: list(l) - bit array list
    '''
    m = 0x01
    l = []
    for _ in range(8):
        if i & m == 0:
            l.insert(0, 0)
        else:
            l.insert(0, 1)
        m = m << 1
    return l
