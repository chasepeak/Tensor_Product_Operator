class Matrix(): 
    def __init__(self, matrix):
        self.matrix = matrix
        self.dim = len(matrix) #dimension

    def __repr__(self):
        mat = ''
        for i in self.matrix:
            mat += '{}\n' .format(i)
        return mat.strip()

    def get_diagonal(self):
        diagonal = []
        for i in range(self.dim):
            for j in range(self.dim):
                if j == i:
                    diagonal.append(self.matrix[i][j])
        return diagonal

    def get_nonzero_values(self):
        nonzero_values = []
        for i in range(self.dim):
            for j in range(self.dim):
                if self.matrix[i][j] != '0':
                    nonzero_values.append(self.matrix[i][j])
        return nonzero_values
