from Common.functions import converttopicture
from Common.functions import borderpoint8
from Common.functions import numtotext
from Common.functions import endpointmodified
from Common.functions import oneobject
from Common.functions import simpleafterremove
from Common.functions import forbidden

binary = 0
matrix = 0

# 33 554 432
for x in range(33554432):
    print(round(((x+1) / 33554432) * 100, 5), '%')
    binary = format(x, 'b')
    matrix = (converttopicture(list(reversed(binary))))
    if matrix[2][2] == 0 or not borderpoint8(matrix, 2, 2):
        numtotext('lookup', 0)
        continue
    if endpointmodified(matrix, 2, 2):
        continue
    if not oneobject(matrix, 2, 2) <= 1:
        numtotext('lookup', 0)
        continue
    if not simpleafterremove(matrix, 2, 2):
        numtotext('lookup', 0)
        continue
    if forbidden(matrix, 2, 2):
        numtotext('lookup', 0)
        continue
    numtotext('lookup', 1)
