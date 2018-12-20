from function import connected
from function import findpath
from function import rvalue

grayness = rvalue(31, 0, 145, 18, 30) * 0
connected(0, 0, 0, 0, 255, 255, 0, 255, 0, grayness)

# print(findpath(0, 0, 0, 0, 255, 0, 255, 0, 0, 0, 2, grayness))