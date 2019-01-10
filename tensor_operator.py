'''
Unitary Equivalence for Tensor Products of Linear Transformations:
Chase M. Peak
01/10/19 revised

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
    nonzero_entries = ['l1','a','b','l2','c','l3']
    matrix_rep(matrix)
    for row in range(matrix_dim):
        for col in range(matrix_dim):
            if not matrix[row][col] == '0':
                new_val = input('Enter "0" or press "Enter" for spot: {} <- ' .format(matrix[row][col]))
                if new_val == '0':
                    nonzero_entries.remove(matrix[row][col])
                    matrix[row][col] = '0'
                elif new_val:
                    raise ValueError('please enter a valid input 0 or press "Enter"')

    scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
    while scaler not in nonzero_entries and scaler: #this makes sure a valid input is entered
        matrix_rep(matrix)
        print('Error: please enter a value present in the given matrix')
        scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
    for i in range(matrix_dim):
        for j in range(matrix_dim):
            if i <= j and matrix[i][j] == scaler: #speeds up the search process by comparing rows and columns
                matrix[i][j] = '1'
                break

    check_irreducibility(matrix)
    matrix_rep(matrix)

    tensor = None
    while not tensor in ['T','W']: #this makes sure a valid input is entered
        tensor = input("Enter 'T' for T = A x I + I x A.\nEnter 'W' for W = A x A.\n")
        try:
            tensor = tensor.upper()
        except:
            tensor = None

    mat = Matrix(matrix)
    create_tensor(mat, tensor)

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


def matrix_rep(matrix):
    if type(matrix) == list:
        mat = ''
        for i in matrix:
            mat += '{}\n'.format(i)
        print(mat.strip())
    else: #be careful with edge cases
            mat = ''
            for i in range(matrix.shape[0]):
                mat += '{}\n' .format(list(matrix.row(i)))
            print(mat)


def create_tensor(matrix, tensor):
    e1 = Matrix(3,1,[1,0,0]) #initialization of basis vectors
    e2 = Matrix(3,1,[0,1,0])
    e3 = Matrix(3,1,[0,0,1])

    symmetric_vectors = [TensorProduct(e1,e1), TensorProduct(e1,e2) + TensorProduct(e2,e1), 
                         TensorProduct(e1,e3) + TensorProduct(e3,e1), TensorProduct(e2,e2),
                         TensorProduct(e2,e3) + TensorProduct(e3,e2), TensorProduct(e3,e3)]
    asymmetric_vectors = [TensorProduct(e1,e2) - TensorProduct(e2,e1), TensorProduct(e1,e3) - TensorProduct(e3,e1),
                          TensorProduct(e2,e3) - TensorProduct(e3,e2)] 
    if tensor == 'T':
        Tens = TensorProduct(matrix,eye(3)) + TensorProduct(eye(3),matrix)
    else:
        Tens = TensorProduct(matrix,matrix)
    for i in range(len(symmetric_vectors)): #performs the computations
        symmetric_vectors[i] = list(Tens * symmetric_vectors[i])
        if i < 3:
            asymmetric_vectors[i] = list(Tens * asymmetric_vectors[i])
    Tens_s = Matrix(symmetric_vectors).T
    Tens_as = Matrix(asymmetric_vectors).T

    for j in [7,6,3]: #deletes the repeated rows (correction due to change in basis)
        Tens_s.row_del(j)
    for k in [8,7,6,4,3,0]:
        Tens_as.row_del(k)
    matrix_rep(Tens_s)
    matrix_rep(Tens_as)

if __name__ == "__main__":
    main()
