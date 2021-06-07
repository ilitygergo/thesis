import os
import cv2
import copy
import numpy
import files.input as pic_folder


def get_image_by_name(name):
    return flip(imreadgray(
        f'{os.path.dirname(pic_folder.__file__)}{os.path.sep}{name}'
    ))

# IMAGE FUNCTIONS


# Reads a colored picture in gray
def imreadgray(img):
    image = cv2.imread(img)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img


# Flips the values of a gray image to have 0 as white and 255 as black
def flip(img):
    size = img.shape
    for row in range(0, size[0]):
        for col in range(0, (size[1])):
            img[row, col] = 255 - img[row, col]
    return img


# Checks wether a matrix is equal to another one
def equalmatrix(mat1, mat2, size):
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if mat1[row][col] != mat2[row][col]:
                return False
    return True


# Makes matrix1 equal to matrix2
def makeequalmatrix(mat1, mat2, size):
    for row in range(0, size[0]):
        for col in range(0, size[1]):
            mat1[row][col] = mat2[row][col]


# DYER ROSENFELD SPECIFIC FUNCTIONS

# Calculates the value of R'
def rvalue(b, d, e, f, h):
    minimum = 0
    maximum = 0
    index = 0
    neighbour = [b, d, e, f, h]
    while index < 4:
        if minimum > neighbour[index + 1]:
            minimum = neighbour[index + 1]
        index += 1
    index = 0
    while index < 4:
        if maximum < neighbour[index + 1]:
            maximum = neighbour[index + 1]
        index += 1
    r = maximum - minimum + 1
    return r


# Minimizes the given e point by itself and its neighbours
def minimize(b, d, h, f, e):
    ret = b
    index = 0
    neighbour = [b, d, h, f, e]
    while index < 4:
        if ret > neighbour[index+1]:
            ret = neighbour[index+1]
        index += 1
    return ret


# For the given e point check the neighbours if they have a value bigger than (e-R')
def notendpoint(b, d, h, f, r):
    szam = 0
    if b >= r:
        szam += 1
    if d >= r:
        szam += 1
    if h >= r:
        szam += 1
    if f >= r:
        szam += 1
    if szam >= 2:
        return True
    else:
        return False


def connected(a, b, c, d, e, f, g, h, i, r):
    connect = [b, d, f, h]
    szam = 0
    ret = 0
    con = 0
    if b-r >= e:
        szam += 1
    if d-r >= e:
        szam += 1
    if f-r >= e:
        szam += 1
    if h-r >= e:
        szam += 1

    for x in range(0, 3):
        for y in range(x + 1, 4):
            if connect[x] < connect[y]:
                m = connect[x]
                if e > (m - r):
                    con += 1
                    continue
                elif findpath(a, b, c, d, f, g, h, i, m, x, y, r):
                    ret += 1
            else:
                m = connect[y]
                if e > (m - r):
                    con += 1
                    continue
                elif findpath(a, b, c, d, f, g, h, i, m, x, y, r):
                    ret += 1
    # print('szam: ', szam)
    # print('con: ', con)
    # print('ret: ', ret)
    if szam == 1:
        print('True')
        return True
    if szam == 2:
        if ret >= 1:
            # print('True')
            # print(ret)
            return True
    elif szam == 3:
        if ret >= 3:
            # print('True')
            return True
    elif szam == 4:
        if ret >= 8:
            # print('True')
            return True
    else:
        # print('False')
        return False


def findpath(a, b, c, d, f, g, h, i, m, x, y, r):
    if x == 0 and y == 1:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r) and g >= (m - r) and d >= (m - r)):
            # b and d
            # print('b and d')
            return True
        else:
            return False
    elif x == 0 and y == 2:
        if (b >= (m - r) and c >= (m - r) and f >= (m - r)) or (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # b and f
            # print('b and f')
            return True
        else:
            return False
    elif x == 0 and y == 3:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # b and h
            # print('b and h')
            return True
        else:
            return False
    elif x == 1 and y == 2:
        if (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r)) or (d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # d and f
            # print('d and f')
            return True
        else:
            return False
    elif x == 1 and y == 3:
        if (d >= (m - r) and g >= (m - r) and h >= (m - r)) or (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # d and h
            # print('d and h')
            return True
        else:
            return False
    elif x == 2 and y == 3:
        if (f >= (m - r) and i >= (m - r) and h >= (m - r)) or (f >= (m - r) and c >= (m - r) and b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)):
            # f and h
            # print('f and h')
            return True
        else:
            return False
    else:
        return False


# ALGORITHM FUNCTIONS


# Prints out the matrix
def printmatrix(matrix):
    if len(matrix) < 15:
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))
        print('\n')


# SALARI_SIY AND KANG_ET_AL SPECIFIC


# If one of the neighbours of point has a value 0 than it is true
def borderpoint(img, row, col):
    if img[row + 1][col] == 0 or img[row - 1][col] == 0 or img[row][col + 1] == 0 or img[row][col - 1] == 0:
        return True
    return False


# The middle point has the highest grayness
def localmaximum(n0, n1, n2, n3, n4, n5, n6, n7, n8):
    if n0 > n1 and n0 > n2 and n0 > n3 and n0 > n4 and n0 > n5 and n0 > n6 and n0 > n7 and n0 > n8:
        return True
    return False


# Returns true if the img[row][col] has only one 4 neighbour with nonzero value
def endpoint(img, row, col):
    array = []
    array.extend([img[row - 1][col], img[row][col - 1], img[row + 1][col], img[row][col + 1]])

    if numpy.count_nonzero(array) == 1:
        del array[:]

        if img[row - 1][col] != 0:
            array.extend([img[row - 2][col], img[row - 1][col - 1], img[row - 1][col + 1]])

            if numpy.count_nonzero(array) == 1:
                return True

        if img[row][col - 1] != 0:
            array.extend([img[row - 1][col - 1], img[row][col - 2], img[row + 1][col - 1]])

            if numpy.count_nonzero(array) == 1:
                return True

        if img[row + 1][col] != 0:
            array.extend([img[row + 1][col - 1], img[row + 2][col], img[row + 1][col + 1]])

            if numpy.count_nonzero(array) == 1:
                return True

        if img[row][col + 1] != 0:
            array.extend([img[row - 1][col + 1], img[row][col + 2], img[row + 1][col + 1]])

            if numpy.count_nonzero(array) == 1:
                return True

    return False


# Returns True if the point can be deleted so the path is not weakened in the corner
def connectedcorner(img, row, col):
    num = 0
    if min(img[row][col + 1], img[row - 1][col]) == 0 or img[row - 1][col + 1] >= img[row][col]:
        num += 1
    if min(img[row - 1][col], img[row][col - 1]) == 0 or img[row - 1][col - 1] >= img[row][col]:
        num += 1
    if min(img[row][col - 1], img[row + 1][col]) == 0 or img[row + 1][col - 1] >= img[row][col]:
        num += 1
    if min(img[row + 1][col], img[row][col + 1]) == 0 or img[row + 1][col + 1] >= img[row][col]:
        num += 1
    if num == 4:
        return True
    return False


# Returns True if the point can be deleted so tha path is not weakened
def connectedpath(img, row, col):
    if min(img[row][col + 1], img[row][col - 1]) > 0:
        if img[row + 1][col] < img[row][col] and img[row - 1][col] < img[row][col]:
            return False
    if min(img[row - 1][col], img[row + 1][col]) > 0:
        if img[row][col - 1] < img[row][col] and img[row][col + 1] < img[row][col]:
            return False
    return True


# KANG_ET_AL SPECIFIC


# If two neighbours has a value grater than 0 than returns true
def countnotzero(img, row, col):
    lst = [int(img[row][col + 1]), int(img[row - 1][col + 1]), int(img[row - 1][col]), int(img[row - 1][col - 1]),
           int(img[row][col - 1]), int(img[row + 1][col - 1]), int(img[row + 1][col]), int(img[row + 1][col + 1])]
    if sum(x is not 0 for x in lst) == 2:
        return True
    return False


# SALARI_SIY AND KANG_ET_AL AND COUPRIE_ET_AL SPECIFIC


# Returns true if the img[row][col] has only one 4 neighbour with nonzero value or only one 8 neighbour with zero value
def endpointmodified(img, row, col):
    four = [img[row - 1][col], img[row][col - 1], img[row][col + 1], img[row + 1][col]]
    eight = [img[row - 1][col - 1], img[row - 1][col + 1], img[row + 1][col - 1], img[row + 1][col + 1]]
    if numpy.count_nonzero(four) == 1 or numpy.count_nonzero(eight) == 1:
        return True
    return False


# KIM SPECIFIC FUNCTIONS


# Count the value differences in the 8 neighbourhood
def countf(img, row, col):
    # l = 1
    if img[row][col + 1] < img[row][col] and \
            (img[row][col + 1] < img[row - 1][col + 1] or img[row][col + 1] < img[row - 1][col]):
        f1 = -1
    elif img[row][col + 1] > img[row - 1][col] and img[row - 1][col] < img[row][col]:
        f1 = 1
    else:
        f1 = 0
    # l = 2
    if img[row - 1][col] < img[row][col] and \
            (img[row - 1][col] < img[row - 1][col - 1] or img[row - 1][col] < img[row][col - 1]):
        f3 = -1
    elif img[row - 1][col] > img[row][col - 1] and img[row][col - 1] < img[row][col]:
        f3 = 1
    else:
        f3 = 0
    # l = 3
    if img[row][col - 1] < img[row][col] and \
            (img[row][col - 1] < img[row + 1][col - 1] or img[row][col - 1] < img[row + 1][col]):
        f5 = -1
    elif img[row][col - 1] > img[row + 1][col] and img[row + 1][col] < img[row][col]:
        f5 = 1
    else:
        f5 = 0
    # l = 4
    if img[row + 1][col] < img[row][col] and \
            (img[row + 1][col] < img[row + 1][col + 1] or img[row + 1][col] < img[row][col + 1]):
        f7 = -1
    elif img[row + 1][col] > img[row][col + 1] and img[row][col + 1] < img[row][col]:
        f7 = 1
    else:
        f7 = 0
    # l = 1
    if img[row - 1][col + 1] > img[row - 1][col] and img[row - 1][col] < img[row][col]:
        f2 = 1
    else:
        f2 = 0
    # l = 2
    if img[row - 1][col - 1] > img[row][col - 1] and img[row][col - 1] < img[row][col]:
        f4 = 1
    else:
        f4 = 0
    # l = 3
    if img[row + 1][col - 1] > img[row + 1][col] and img[row + 1][col] < img[row][col]:
        f6 = 1
    else:
        f6 = 0
    # l = 4
    if img[row + 1][col + 1] > img[row][col + 1] and img[row][col + 1] < img[row][col]:
        f8 = 1
    else:
        f8 = 0
    clockwise = [f1, f2, f3, f4, f5, f6, f7, f8, f1]
    last_sign = 0
    sign_changes = 0

    for x in clockwise:
        if x == 0:
            continue
        elif x == 1:
            if last_sign == -1:
                sign_changes += 1
        last_sign = x

    return sign_changes


#COUPRIE_ET_AL SPECIFIC


# If one of the 8 neighbours of point has a value 0 than it is true
def borderpoint8(img, row, col):
    if img[row + 1][col] == 0 or img[row + 1][col + 1] == 0 or img[row][col + 1] == 0 or img[row - 1][col + 1] == 0 or \
      img[row - 1][col] == 0 or img[row - 1][col - 1] == 0 or img[row][col - 1] == 0 or img[row + 1][col - 1] == 0:
        return True
    return False


# Checks the neighbourhood of a point and returns the number of objects in the neighbourhood
def oneobject(img, row, col):
    objects = 0
    if img[row - 1][col] == 0 and (img[row - 1][col + 1] != 0 or img[row][col + 1] != 0):
        objects += 1
    if img[row][col + 1] == 0 and (img[row + 1][col + 1] != 0 or img[row + 1][col] != 0):
        objects += 1
    if img[row + 1][col] == 0 and (img[row + 1][col - 1] != 0 or img[row][col - 1] != 0):
        objects += 1
    if img[row][col - 1] == 0 and (img[row - 1][col - 1] != 0 or img[row - 1][col] != 0):
        objects += 1
    return objects


# Returns True if the field equals any of the forbidden shapes
def forbidden(img, row, col):
    # a
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0:
        return True
    # b
        # left
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row][col + 2] == 0 and img[row - 1][col + 2] == 0 and \
       img[row - 1][col + 1] == 0 and img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and \
       img[row][col - 1] == 0 and img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and \
       img[row + 1][col + 1] == 0 and img[row + 1][col + 2] == 0:
        return True
        # right
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0:
        return True
    # c
        # up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] == 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0:
        return True
        # down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col - 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col + 1] == 0:
        return True
    # d
        # left up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] != 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0 and \
       img[row + 2][col + 2] == 0 and img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row - 1][col + 2] == 0:
        return True
        # right down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] != 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col - 1] == 0 and \
       img[row - 2][col - 2] == 0 and img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and \
       img[row + 1][col - 2] == 0:
        return True
    # e
        # right up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] != 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0 and \
       img[row + 2][col - 2] == 0 and img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and \
       img[row + 2][col + 1] == 0:
        return True
        # left down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] != 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col - 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col + 1] == 0 and \
       img[row - 2][col + 2] == 0 and img[row - 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row + 1][col + 2] == 0:
        return True
    # f
        # right up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] != 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0 and \
       img[row + 2][col - 2] == 0 and img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and \
       img[row + 2][col + 1] == 0:
        return True
        # right down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col - 1] == 0 and \
       img[row - 2][col - 2] == 0 and img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and \
       img[row + 1][col - 2] == 0:
        return True
        # left down
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] != 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col - 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col + 1] == 0 and \
       img[row - 2][col + 2] == 0 and img[row - 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row + 1][col + 2] == 0:
        return True
    # g
        # left up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] != 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0 and \
       img[row + 2][col + 2] == 0 and img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row - 1][col + 2] == 0:
        return True
        # left down
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and img[row - 1][col + 2] == 0 and \
       img[row - 2][col + 2] == 0 and img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and \
       img[row - 2][col - 1] == 0:
        return True
        # right down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] != 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col - 1] == 0 and \
       img[row - 2][col - 2] == 0 and img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and \
       img[row + 1][col - 2] == 0:
        return True
    # h
        # left up
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] != 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0 and \
       img[row + 2][col + 2] == 0 and img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row - 1][col + 2] == 0:
        return True
        # right up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0 and \
       img[row + 2][col - 2] == 0 and img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and \
       img[row + 2][col + 1] == 0:
        return True
        # right down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] != 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col - 1] == 0 and \
       img[row - 2][col - 2] == 0 and img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and \
       img[row + 1][col - 2] == 0:
        return True
    # i
        # left up
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] == 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0 and \
       img[row + 2][col + 2] == 0 and img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row - 1][col + 2] == 0:
        return True
        # right up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] != 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0 and \
       img[row + 2][col - 2] == 0 and img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and \
       img[row + 2][col + 1] == 0:
        return True
        # left down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] != 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and img[row - 1][col + 2] == 0 and \
       img[row - 2][col + 2] == 0 and img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and \
       img[row - 2][col - 1] == 0:
        return True
    # j
        # left up
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] != 0 and \
       img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and img[row + 2][col + 1] == 0 and \
       img[row + 2][col + 2] == 0 and img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and \
       img[row - 1][col + 2] == 0:
        return True
        # right up
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] == 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] != 0 and img[row + 1][col] != 0 and img[row + 1][col + 1] == 0 and \
       img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and img[row + 1][col - 2] == 0 and \
       img[row + 2][col - 2] == 0 and img[row + 2][col - 1] == 0 and img[row + 2][col] == 0 and \
       img[row + 2][col + 1] == 0:
        return True
        # left down
    if img[row][col] != 0 and img[row][col + 1] != 0 and img[row - 1][col + 1] != 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] == 0 and img[row][col - 1] == 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row + 1][col + 2] == 0 and img[row][col + 2] == 0 and img[row - 1][col + 2] == 0 and \
       img[row - 2][col + 2] == 0 and img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and \
       img[row - 2][col - 1] == 0:
        return True
        # right down
    if img[row][col] != 0 and img[row][col + 1] == 0 and img[row - 1][col + 1] == 0 and \
       img[row - 1][col] != 0 and img[row - 1][col - 1] != 0 and img[row][col - 1] != 0 and \
       img[row + 1][col - 1] == 0 and img[row + 1][col] == 0 and img[row + 1][col + 1] == 0 and \
       img[row - 2][col + 1] == 0 and img[row - 2][col] == 0 and img[row - 2][col - 1] == 0 and \
       img[row - 2][col - 2] == 0 and img[row - 1][col - 2] == 0 and img[row][col - 2] == 0 and \
       img[row + 1][col - 2] == 0:
        return True
    return False


# Creates a 5x5 binary matrix
def binmatrix(img, row, col, size):
    matrix = numpy.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
    for x in range(5):
        for y in range(5):
            if (size[0] - 4) > row > 2 and (size[1] - 4) > col > 2:
                if not simpleafterremove(img, x + row - 2, y + col - 2) <= 1:
                    continue
            if img[x + row - 2][y + col - 2] < img[row][col]:
                matrix[x][y] = 0
    return matrix


# Returns true if neighbour remains simple after img[row][col] is deleted
def simpleafterremove(img, row, col):
    if simpleafterhelper(img, row, col, row, col - 1) and \
       simpleafterhelper(img, row, col, row + 1, col) and \
       simpleafterhelper(img, row, col, row - 1, col) and \
       simpleafterhelper(img, row, col, row, col + 1):
        return True
    return False


# Returns True if the neighbour can be deleted
def simpleafterhelper(img, x, y, row, col):
    default = copy.deepcopy(img[x][y])
    if oneobject(img, row, col) <= 1 and img[row][col] != 0:
        img[x][y] = 0
        if oneobject(img, row, col) <= 1 and img[row][col] != 0:
            img[x][y] = default
            return True
        else:
            img[x][y] = default
            return False
    return True


# Returns the biggest 8 neighbour whit a lower intensity than the examined point
def lowneighbour(img, row, col):
    stack = [img[row - 1][col - 1], img[row - 1][col], img[row - 1][col + 1],
             img[row][col - 1], img[row][col + 1],
             img[row + 1][col - 1], img[row + 1][col], img[row + 1][col + 1]]
    values = []

    for x in stack:
        if x < img[row][col]:
            values.append(x)

    highest = values[0]
    for x in values:
        if x > highest:
            highest = x

    return highest


# COUPRIE_ET_AL LOOKUP SPECIFIC


# Converts the picture into an array
def converttoarray(img, row, col):
    array = [img[row + 2][col + 2], img[row + 2][col + 1], img[row + 2][col], img[row + 2][col - 1],img[row + 2][col- 2],
             img[row + 1][col + 2], img[row + 1][col + 1], img[row + 1][col], img[row + 1][col - 1], img[row + 1][col - 2],
             img[row][col + 2], img[row][col + 1], img[row][col], img[row][col - 1], img[row][col - 2],
             img[row - 1][col + 2], img[row - 1][col + 1], img[row - 1][col], img[row - 1][col - 1], img[row - 1][col - 2],
             img[row - 2][col + 2], img[row - 2][col + 1], img[row - 2][col], img[row - 2][col - 1], img[row - 2][col - 2]]
    return array


# Converts the picture into an array
def arraytonum(array):
    num = array[0]*(2**24) + array[1]*(2**23) + array[2]*(2**22) + array[3]*(2**21) + array[4]*(2**20) + \
          array[5]*(2**19) + array[6]*(2**18) + array[7]*(2**17) + array[8]*(2**16) + array[9]*(2**15) + \
          array[10]*(2**14) + array[11]*(2**13) + array[12]*(2**12) + array[13]*(2**11) + array[14]*(2**10) + \
          array[15]*(2 ** 9) + array[16]*(2**8) + array[17]*(2**7) + array[18]*(2**6) + array[19]*(2**5) + \
          array[20]*(2 ** 4) + array[21]*(2**3) + array[22]*(2**2) + array[23]*(2**1) + array[24]
    return num


# Converts an array to a picture matrix
def converttopicture(binary):
    picture = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for x in range(len(binary)):
        picture[x] = int(binary[x])
    return picture.reshape(5, 5)
