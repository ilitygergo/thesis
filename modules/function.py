import cv2


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


# Calculates the value of R'
def rvalue(b, d, e, f, h):
    min = 0
    max = 0
    index = 0
    neighbour = [b, d, e, f, h]
    while index < 4:
        if min > neighbour[index + 1]:
            min = neighbour[index + 1]
        index += 1
    index = 0
    while index < 4:
        if max < neighbour[index + 1]:
            max = neighbour[index + 1]
        index += 1
    r = max - min + 1
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


# Minimize the given e point by itself and its neighbours if they are not zero
def minimizenotnull(b, d, h, f, e):
    ret = b
    index = 0
    neighbour = [b, d, h, f, e]
    while index < 4:
        if ret > neighbour[index+1] != 0:
            ret = neighbour[index+1]
        index += 1
    return ret


# Maximize the given e point by itself and its neighbours if they are not zero
def maximizenotnull(a, b, c, d, e, f, g, h, i):
    ret = a
    index = 0
    neighbour = [a, b, c, d, e, f, g, h, i]
    while index < 4:
        if ret < neighbour[index+1] != 0:
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
        # print('True')
        return True
    else:
        # print('False')
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
    print('szam: ', szam)
    print('con: ', con)
    print('ret: ', ret)
    if szam == 1:
        print('True')
        return True
    if szam == 2:
        if ret >= 1:
            print('True')
            print(ret)
            return True
    elif szam == 3:
        if ret >= 3:
            print('True')
            return True
    elif szam == 4:
        if ret >= 8:
            print('True')
            return True
    else:
        print('False')
        return False


def findpath(a, b, c, d, f, g, h, i, m, x, y, r):
    if x == 0 and y == 1:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r) and g >= (m - r) and d >= (m - r)):
            # b and d
            print('b and d')
            return True
        else:
            return False
    elif x == 0 and y == 2:
        if (b >= (m - r) and c >= (m - r) and f >= (m - r)) or (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # b and f
            print('b and f')
            return True
        else:
            return False
    elif x == 0 and y == 3:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # b and h
            print('b and h')
            return True
        else:
            return False
    elif x == 1 and y == 2:
        if (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r)) or (d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # d and f
            print('d and f')
            return True
        else:
            return False
    elif x == 1 and y == 3:
        if (d >= (m - r) and g >= (m - r) and h >= (m - r)) or (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # d and h
            print('d and h')
            return True
        else:
            return False
    elif x == 2 and y == 3:
        if (f >= (m - r) and i >= (m - r) and h >= (m - r)) or (f >= (m - r) and c >= (m - r) and b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)):
            # f and h
            print('f and h')
            return True
        else:
            return False
    else:
        return False


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
