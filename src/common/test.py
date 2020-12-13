import struct
from src.common.functions import converttopicture
from src.common.functions import borderpoint8
from src.common.functions import endpointmodified
from src.common.functions import oneobject
from src.common.functions import simpleafterremove
from src.common.functions import forbidden

binary = 0
matrix = 0
file = open('lookup_index', 'wb')

# 33 554 432
for x in range(33554432):
    print(round(((x+1) / 33554432) * 100, 2), '%')
    binary = format(x, 'b')
    matrix = (converttopicture(list(reversed(binary))))
    if matrix[2][2] == 0 or not borderpoint8(matrix, 2, 2):
        continue
    if endpointmodified(matrix, 2, 2):
        continue
    if not oneobject(matrix, 2, 2) <= 1:
        continue
    if not simpleafterremove(matrix, 2, 2):
        continue
    if forbidden(matrix, 2, 2):
        continue
    file.write(struct.pack('<l', x))
    file.flush()

file.close()
