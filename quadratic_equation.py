import math


def quadratic_equation(a, b, c, e):
    discr = b ** 2 - 4 * a * c
    if discr < -e:
        return []
    elif -e < discr < e:
        discr = 0
    x1 = (-b - math.sqrt(discr)) / (2 * a)
    x2 = (-b + math.sqrt(discr)) / (2 * a)
    if x1 == x2:
        return [x1]
    else:
        return [x1, x2]
