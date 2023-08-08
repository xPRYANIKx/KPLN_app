l = [0, 10, 20, 30, 40, 50]
xxx = 6
for i in range(len(l)):
    if l[i] == 20 and l[i] in [0, 20, 30]:
        print(i, id(i), '-', len(l), '-', l)
    print(i, id(i))

print(l)
print('TYPE', type(l))