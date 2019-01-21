X = [1, 0, -1, 0, 1, 0, -1, 0, 1, -1]
print(X)

last_sign = 0
sign_changes = 0

for x in X:
    if x == 0:
        continue
    elif x == 1:
        if last_sign == -1:
            sign_changes += 1
    last_sign = x

print(sign_changes)