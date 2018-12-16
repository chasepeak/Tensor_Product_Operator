#Tensor Product Computations
#Chase Peak
#12/15/18

import math
from sympy import *
#from sympy import I, Matrix
from sympy.physics.quantum import TensorProduct

class ReducibilityError(Exception):
    pass

def main():
    matrix = [['l1','a','b'],['0','l2','c'],['0','0','l3']]
    matrix_dim = len(matrix)
    nonzero_entries = []
    matrix_rep(matrix)
    print("When prompted, enter '0' to cancel a value, or '1' for it to remain unchanged.")
    for row in range(matrix_dim):
        for i in range(matrix_dim):
            if not matrix[row][i] == '0':
                new_val = input('Enter "0" or "1" for spot: {} <- ' .format(matrix[row][i]))
                if new_val == '0':
                    matrix[row][i] = '0'
                elif new_val == '1':
                    matrix[row][i] = matrix[row][i]
                    nonzero_entries.append(matrix[row][i])
                else:
                    raise ValueError('please enter a valid input 0 or 1')

    scaler = input("Enter the value from the matrix you wish to scale to 1, or enter 'None': ")
    while scaler not in nonzero_entries and scaler == 'none':
        matrix_rep(matrix)
        print('Error: please enter a value present in the given matrix')
        scaler = input('Enter the value from the matrix you wish to scale to 1: ')
    for i in range(matrix_dim):
        for j in range(matrix_dim):
            matrix[i][j] = '1' if matrix[i][j] == scaler else matrix[i][j]

    check_irreducibility(matrix)
    matrix_rep(matrix)

    tensor = None
    while not tensor in ['T','W']:
        tensor = input("Enter 'T' for T = A x I + I x A.\nEnter 'W' for W = A x A.\n")
        try:
            tensor = tensor.upper()
        except:
            tensor = None

    mat = Matrix(matrix)
    if tensor == 'T':
        T = TensorProduct(mat,eye(3)) + TensorProduct(eye(3),mat)
        for i in range(matrix_dim ** 2):
            print(list(T.row(i)))
    else:
        W = TensorProduct(mat,mat)
        for i in range(matrix_dim ** 2):
            print(list(W.row(i)))


def check_irreducibility(matrix):
    diagonal = []
    for i in matrix:
        for j in i:
            if i == j:
                diagonal.append(matrix[i][j])
    reducible = False
    if not '0' in diagonal:
        if (matrix[0][1] == '0' and (matrix[0][2] == '0' or matrix[1][2] == '0') or 
            matrix[0][2] == '0' and (matrix[0][1] == '0' or matrix[1][2] == '0')):
            reducible = True
    elif diagonal == ['0','0','0'] or diagonal == ['l1','0','l3']:
        if matrix[0][1] == '0' or matrix[1][2] == '0':
            reducible = True
    else:
        if diagonal == ['0','0','l3']:
            if matrix[0][1] == '0' and (matrix[0][2] == '0' or matrix[1][2] == '0'):
                reducible = True
        elif diagonal == ['l1','0','0']:
            if matrix[1][2] == '0' and (matrix[0][1] == '0' or matrix[0][2] == '0'):
                reducible = True
    if reducible:
        raise ReducibilityError('Matrix is reducible')
    pass


def matrix_rep(matrix):
    if type(matrix) == list:
        mat = ''
        for i in matrix:
            mat += '{}\n'.format(i)
        print(mat)


if __name__ == "__main__":
    main()
