from UTMatrix import *
from tensor_operator import *

def main():
    matrix = UTMatrix()
    matrix.create_matrix()
    set_tensor(matrix)
    create_tensor(matrix)

if __name__ == "__main__":
    main()
