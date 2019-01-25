'''
Unitary Equivalence for Tensor Products of Linear Transformations:
Chase M. Peak
01/24/19 revised

This program takes user input to construct a 3x3 upper-triangular matrix, and then checks to
make sure it is irreducible before performing the tensor product. Then, it utilizes the sympy
module to manipulate the matrices.

*Work in progress (more features will be added later on)
'''

from sympy import *
from sympy.physics.quantum import TensorProduct

class ReducibilityError(Exception):
    pass

def main():
    try:
        dimension = int(input("Enter the dimension of your matrix (between 2 and 5): "))
        if dimension not in range(2,6):
            raise Error
    except:
        print("Please enter a valid integer between 2 and 5.")
        exit()

    matrix = form_matrix(dimension)
    #check_irreducibility(matrix)
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


def form_matrix(dimension):
    letters = [chr(x) for x in range(num_entries(dimension) + 96, 96, -1)]
    diagonal = ['l{}'.format(x) for x in range(1,dimension + 1)]
    matrix = [[0 for x in range(dimension)] for x in range(dimension)]
    values = diagonal
    for i in range(dimension):
        for j in range(i,dimension):
            if (i == j):
                new_val = input("For entry at {}, enter any key to set to 0 or press 'Enter'  for {} to remain: " .format((i + 1, j + 1), diagonal[i]))
                matrix[i][j] = diagonal[i] if not new_val else '0'
            else:
                current_letter = letters.pop()
                new_val = input("For entry at {}, enter any key to set to 0 or press 'Enter'  for {} to remain: " .format((i + 1, j + 1), current_letter))
                matrix[i][j] = current_letter if not new_val else '0'
    matrix_rep(matrix)
    scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
    while not (scaler in letters or scaler in diagonal) and scaler: #this makes sure a valid input is entered
        matrix_rep(matrix)
        print('Please enter a value present in the given matrix.')
        scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
    for i in range(dimension):
        for j in range(i, dimension):
            if matrix[i][j] == scaler: #speeds up the search process by comparing rows and columns
                matrix[i][j] = '1'
                break
    return matrix

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


def num_entries(dimension):
    assert dimension > 0
    assert type(dimension) == int
    if dimension < 4:
        return dimension - 1 + dimension // 3
    return dimension + num_entries(dimension - 1)


if __name__ == "__main__":
    main()
