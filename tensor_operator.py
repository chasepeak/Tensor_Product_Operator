#Tensor Product Computations
#Chase Peak
#12/15/18

import math
#import numpy as np
from matrix import Matrix

class ReducibilityError(Exception):
    pass

def main():
    matrix = [['l1','a','b'],['0','l2','c'],['0','0','l3']]
    mat = Matrix(matrix)
    print(mat)
    print("When prompted, enter '0' for a given value, or '1' for it to remain unchanged")
    for row in range(mat.dim):
        for i in range(mat.dim):
            if not mat.matrix[row][i] == '0':
                new_val = input('Enter "0" or "1" for spot: {} <- ' .format(mat.matrix[row][i]))
                if new_val == '0':
                    mat.matrix[row][i] = '0'
                elif new_val == '1':
                    mat.matrix[row][i] = mat.matrix[row][i]
                else:
                    raise ValueError('please enter a valid input 0 or 1')
    print(mat)
    check_irreducibility(mat)

    scaler = input('Enter the value from the matrix you wish to scale to 1: ')
    non_zeroes = mat.get_nonzero_values()
    while scaler not in non_zeroes:
        print(mat)
        print('Error: please enter a value present in the given matrix')
        scaler = input('Enter the value from the matrix you wish to scale to 1: ')
    for i in range(mat.dim):
        for j in range(mat.dim):
            mat.matrix[i][j] = '1' if mat.matrix[i][j] == scaler else mat.matrix[i][j]
    print('final matrix:\n{}' .format(mat))

    tensor = None
    while not tensor in ['T','W']:
        tensor = input("Enter 'T' for T = A x I + I x A.\nEnter 'W' for W = A x A.\n")
        try:
            tensor = tensor.upper()
        except:
            tensor = None
    sym_tensor_mat = [[None] * (mat.dim * 2)] * (mat.dim * 2)
    asym_tensor_mat = [[None] * (mat.dim)] * (mat.dim)
    sym_tensor = Matrix(sym_tensor_mat)
    a_sym_tensor = Matrix(asym_tensor_mat)
    

def check_irreducibility(mat):
    diagonal = mat.get_diagonal()
    reducible = False
    if not '0' in diagonal:
        if (mat.matrix[0][1] == '0' and (mat.matrix[0][2] == '0' or mat.matrix[1][2] == '0') or 
            mat.matrix[0][2] == '0' and (mat.matrix[0][1] == '0' or mat.matrix[1][2] == '0')):
            reducible = True
    elif diagonal == ['0','0','0'] or diagonal == ['l1','0','l3']:
        if mat.matrix[0][1] == '0' or mat.matrix[1][2] == '0':
            reducible = True
    else:
        if diagonal == ['0','0','l3']:
            if mat.matrix[0][1] == '0' and (mat.matrix[0][2] == '0' or mat.matrix[1][2] == '0'):
                reducible = True
        elif diagonal == ['l1','0','0']:
            if mat.matrix[1][2] == '0' and (mat.matrix[0][1] == '0' or mat.matrix[0][2] == '0'):
                reducible = True
    if reducible:
        raise ReducibilityError('Matrix is reducible')
    pass
"""
 35         if tensor == 1:
 36                 tensor_op1 = [["2*{0}" .format(matrix[0][0]), "2*{0}" .format(matrix[0][1]), "2*{0}" .format(matrix[0][2]), "0", "0", "0"],
 37                               ["0", "{0} + {1}" .format(matrix[0][0], matrix[1][1]), "{0}" .format(matrix[1][2]), "{0}" .format(matrix[0][1]), "{0}" .format(matrix[0][2]), "0"],
 38                               ["0", "0", "{0} + {1}" .format(matrix[0][0], matrix[2][2]), "0", "{0}" .format(matrix[0][1]), "{0}" .format(matrix[0][2]), "0"],
 39                               ["0", "0", "0", "2*{0}" .format(matrix[1][1]), "2*{0}" .format(matrix[1][2]), "0"],
 40                               ["0", "0", "0", "0", "{0} + {1}" .format(matrix[1][1], matrix[2][2]), "{0}" .format(matrix[1][2])],
 41                               ["0", "0", "0", "0", "0", "2*{0}" .format(matrix[2][2])]]
 42                 for i in tensor_op1:#we need for the matrix to now show up as numbers
 43                         print(i)
 44                 print("")
 45         else:   
 46                 print("")
 47         
 48         pass
"""
if __name__ == "__main__":
    main()
