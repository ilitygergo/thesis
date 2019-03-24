from Common.functions import converttopicture
from Common.functions import converttoarray
from Common.functions import arraytonum
from Common.functions import borderpoint8
from Common.functions import numtotext
from Common.functions import endpointmodified
from Common.functions import oneobject
from Common.functions import simpleafterremove
from Common.functions import forbidden

binary = 0
matrix = 0
# 16777216

for x in range(20):
    binary = format(x, 'b')
    matrix = (converttopicture(list(reversed(binary))))
    print(binary)
    print(matrix)
    array = converttoarray(matrix, 2, 2)
    print(arraytonum(array))
    if matrix[2][2] == 0 or not borderpoint8(matrix, 2, 2):
        numtotext('test', 0)
        continue
    if endpointmodified(matrix, 2, 2):
        continue
    if not oneobject(matrix, 2, 2) <= 1:
        numtotext('test', 0)
        continue
    if not simpleafterremove(matrix, 2, 2):
        numtotext('test', 0)
        continue
    if forbidden(matrix, 2, 2):
        numtotext('test', 0)
        continue
    numtotext('test', 1)

# Kiolvasás
with open('test.txt') as file:
    content = file.read().splitlines()

print(int(str(1011), 2))
print(content[int(str(1011), 2)])
