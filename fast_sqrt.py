def sqrt(num: float, epsilon: float):
    # f(x) = x^2 - num = 0
    assume = num / 2  # assume that x is somewhat close to sqrt(num)
    tmp = assume**2 - num  # f(x0)
    while abs(tmp) > epsilon:
        k = 2 * assume  # f'(x0)
        assume = assume - tmp / k  # solve x in (x - x0) * f'(x0) + f(x0) = 0
        tmp = assume**2 - num

    return assume


print(sqrt(25, 1e-8))
