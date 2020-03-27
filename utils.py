import math

def round_well(n):
    if n-math.floor(n)<0.5:
        return math.floor(n)
    return math.ceil(n)