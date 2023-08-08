import itertools

values_p_a_h = [(26, 2, 2, 2), (27, 2, 2, 3), (80, 2, 2, 4)]

values_1d = list(itertools.chain(*values_p_a_h))

print(values_p_a_h)

print(values_1d)
print(type(values_1d))
print(type(values_1d[0]))
