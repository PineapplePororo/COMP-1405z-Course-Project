# Alvina Han (Kayeon)
# 10/08/2022
# Tutorial 4 Problem 1: Matrix Multiplication

import math

# return a new 2D list when a matrix is multiplied by the given scalar
def mult_scalar(matrix, scale):

    # copy of the matrix
    MultipliedM = matrix

    # loop for rows 
    for i in range(len(MultipliedM)):
        # loop for each entry in the row
        for j in range(len(MultipliedM[i])):
            # mulitply each entry by the scale
            MultipliedM[i][j] = MultipliedM[i][j] * scale

    return MultipliedM


# return a new matrix that multiplied the matrix a by the matrix b
def mult_matrix(a, b):

    # check if inputs are valid
    # valid if: number of columns of a = number of rows of b
    if(len(a[0]) != len(b)):
        # not valid 
        return None

    # initializing a new matrix that will be returned
    newM = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]

    # loop for rows of a
    for r in range(len(a)):
        # loop for columns of b
        for c in range(len(b[0])):
            # set total to 0 for all new entries in newM
            total = 0
            # loop for rows of b/ entries of a row of a
            for e in range(len(b)):
                # multiply corresponding entries and add it to total
                total += a[r][e]*b[e][c]

            # add finalized number to matrix that will be returned
            newM[r][c] = total
    
    return newM
	

# calculate the Euclidean distance between these two vectors
def euclidean_dist(a,b):

    # initialize total to floating number
    total = 0.0

    # loop for the number of entries in matrix a and b
    for column in range(len(a[0])):
        # find the sum before the square root
        total += (a[0][column] - b[0][column])**2

    # square root 
    total = math.sqrt(total)

    return total

