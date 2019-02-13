'''
Unitary Equivalence for Tensor Products of Linear Transformations:
Chase M. Peak
01/24/19 revised

This program takes user input to construct a 3x3 upper-triangular matrix, and then checks to
make sure it is irreducible before performing the tensor product. Then, it utilizes the sympy
module to manipulate the matrices.

*Work in progress (more features will be added later on)
'''
import math
from UTMatrix import *
from sympy import *
from sympy.physics.quantum import TensorProduct

def set_tensor(matrix, tensor = None):
    while not tensor in ['T','W']:
        tensor = input("Enter 'T' for T = A {0} I + I {0} A.\nEnter 'W' for W = A {0} A.\n".format(chr(8855)))
    matrix.tensor = tensor #set tensor in given matrix

def create_tensor(mat):
    e1 = Matrix(3,1,[1,0,0]) #initialization of basis vectors
    e2 = Matrix(3,1,[0,1,0])
    e3 = Matrix(3,1,[0,0,1])

    matrix = Matrix(mat.matrix)

    symmetric_vectors = [TensorProduct(e1,e1), TensorProduct(e1,e2) + TensorProduct(e2,e1), 
                         TensorProduct(e1,e3) + TensorProduct(e3,e1), TensorProduct(e2,e2),
                         TensorProduct(e2,e3) + TensorProduct(e3,e2), TensorProduct(e3,e3)]
    asymmetric_vectors = [TensorProduct(e1,e2) - TensorProduct(e2,e1), TensorProduct(e1,e3) - TensorProduct(e3,e1),
                          TensorProduct(e2,e3) - TensorProduct(e3,e2)] 
    if mat.tensor == 'T':
        Tens = TensorProduct(matrix, eye(3)) + TensorProduct(eye(3), matrix)
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
    convert_matrix(Tens_s, 6)
    convert_matrix(Tens_as, 3)

def convert_matrix(matrix, mat_size):
    mat = list(matrix)
    mat_dimension = int(math.sqrt(len(mat)))

    sublist = []
    new_matrix = [] #something is not right here
    for i in mat:
        if len(sublist) < mat_size:
            sublist.append(i)
        else:
            new_matrix.append(sublist)
            sublist = []
    print(new_matrix)
    converted = UTMatrix(mat_size)
    converted.matrix = new_matrix
    print(converted)
