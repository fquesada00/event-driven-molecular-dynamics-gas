import matplotlib.pyplot as plt


def line(x, c): return c*x


def quadratic_error(x: list, y: list, m: list):
    errors = []
    for c in m:
        errors.append(
            sum(
                [
                    (y[i]-line(x[i], c))**2 for i in range(len(x))
                ]
            )
        )
    return errors
