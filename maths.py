import math

def Hipotenuza(vector1, vector2) -> int:
    return math.dist(vector1,vector2)

def Angulo(vector1, vector2) -> float:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    angulo = math.atan2(y,x) * (180.0 / math.pi)
    return angulo if angulo > 0 else 180 + (180+angulo)


def format_size_bits_to_bytes(size) -> list:
    count = 0
    while size > 1024:
        size /= 1024
        count += 1
    return [count, size]


UNIDADES_BYTES = {
    0: 'B',
    1: 'KB',
    2: 'MB',
    3: 'GB',
    4: 'TB',
    5: 'PB',
    6: 'EB',
    7: 'ZB',
    8: 'YB'
}