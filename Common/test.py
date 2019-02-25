from Common.functions import converttopicture
from Common.functions import simple
from Common.functions import simpleafterremove
from Common.functions import forbidden
from Common.functions import borderpoint8
from Common.functions import numtotext

binary = 0
matrix = 0
# 16777216

for x in range(20):
    binary = format(x, 'b')
    matrix = (converttopicture(list(reversed(binary))))
    if matrix[2][2] == 0 or not borderpoint8(matrix, 2, 2):
        numtotext('test', 0)
        continue
    if simple(matrix, 2, 2):
        numtotext('test', 0)
        continue
    if not simpleafterremove(matrix, 2, 2):
        numtotext('test', 0)
        continue
    if forbidden(matrix, 2, 2):
        numtotext('test', 0)
        continue
    numtotext('test', 1)
    print(x)

print(matrix)

# Kiolvasás
with open('test.txt') as file:
    content = file.read().splitlines()

print(int(str(1011), 2))
print(content[int(str(1011), 2)])
