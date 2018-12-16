'''
Unitary Equivalence for Tensor Products of Linear Transformations:
Chase M. Peak
12/16/18 revised

This program takes user input to construct a 3x3 upper-triangular matrix, and then checks to
make sure it is irreducible before performing the tensor product. Then, it utilizes the sympy
module to manipulate the matrices.

*Work in progress (more features will be added later on)
'''

from math import sqrt
from sympy import *
from sympy.physics.quantum import TensorProduct

class ReducibilityError(Exception):
    pass

def main():
    matrix = [['l1','a','b'],['0','l2','c'],['0','0','l3']]
    matrix_dim = len(matrix)
    nonzero_entries = []
    matrix_rep(matrix, matrix_dim)
    print("When prompted, enter '0' to cancel a value, or '1' for it to remain unchanged.")
    for row in range(matrix_dim):
        for col in range(matrix_dim):
            if not matrix[row][col] == '0':
                new_val = input('Enter "0" or "1" for spot: {} <- ' .format(matrix[row][col]))
                if new_val == '0':
                    matrix[row][col] = '0'
                elif new_val == '1':
                    nonzero_entries.append(matrix[row][col])
                else:
                    raise ValueError('please enter a valid input 0 or 1')

    scaler = input("Enter the value from the matrix you wish to scale to 1, or enter 'None': ")
    while scaler not in nonzero_entries and scaler == 'none': #this makes sure a valid input is entered
        matrix_rep(matrix, matrix_dim)
        print('Error: please enter a value present in the given matrix')
        scaler = input('Enter the value from the matrix you wish to scale to 1: ')
    for i in range(matrix_dim):
        for j in range(matrix_dim):
            if matrix[i][j] == scaler:
                matrix[i][j] = '1'
                break

    check_irreducibility(matrix)
    matrix_rep(matrix, matrix_dim)

    tensor = None
    while not tensor in ['T','W']: #this makes sure a valid input is entered
        tensor = input("Enter 'T' for T = A x I + I x A.\nEnter 'W' for W = A x A.\n")
        try:
            tensor = tensor.upper()
        except:
            tensor = None

    mat = Matrix(matrix)

    e1 = Matrix(3,1,[1,0,0]) #initialization of basis vectors
    e2 = Matrix(3,1,[0,1,0])
    e3 = Matrix(3,1,[0,0,1])
    symmetric_vectors = [TensorProduct(e1,e1), TensorProduct(e1,e2) + TensorProduct(e2,e1), 
                         TensorProduct(e1,e3) + TensorProduct(e3,e1), TensorProduct(e2,e2),
                         TensorProduct(e2,e3) + TensorProduct(e3,e2), TensorProduct(e3,e3)]
    #asymmetric_vectors = [TensorProduct(e1,e2) - TensorProduct(e2,e1), TensorProduct(e1,e3) - TensorProduct(e3,e1),
    #                      TensorProduct(e2,e3) - TensorProduct(e3,e2)] #later implementation

    if tensor == 'T': 
        T = TensorProduct(mat,eye(3)) + TensorProduct(eye(3),mat)
        for i in range(len(symmetric_vectors)): #performs the computations
            symmetric_vectors[i] = list(T * symmetric_vectors[i])
        T_s = Matrix(symmetric_vectors).T
        matrix_rep(T_s, sqrt(6))
    else:
        W = TensorProduct(mat,mat)
        for i in range(len(symmetric_vectors)):
            symmetric_vectors[i] = list(W * symmetric_vectors[i])
        W_s = Matrix(symmetric_vectors).T
        matrix_rep(W_s, sqrt(6))


def check_irreducibility(matrix): #runs through the conditions of reducibility (see Lemma 2.4)
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


def matrix_rep(matrix, matrix_dim):
    if type(matrix) == list:
        mat = ''
        for i in matrix:
            mat += '{}\n'.format(i)
        print(mat.strip())
    else: #be careful with edge cases
            mat = ''
            for i in range(int(matrix_dim ** 2 + 0.5)):
                mat += '{}\n' .format(list(matrix.row(i)))
            print(mat.strip())


if __name__ == "__main__":
    main()
