class UTMatrix:

    def __init__(self, dimension = None): #upper triangular matrices
        self.dimension = set_dimension() if not dimension else dimension
        self.rows = self.dimension
        self.cols = self.dimension
        self.matrix = [[0 for x in range(self.dimension)] for x in range(self.dimension)]
        self.diagonal = [self.matrix[x][x] for x in range(self.dimension)]
        self.tensor = None

    def __repr__(self):
        str_start = "| "
        str_end = "|\n"
        result = ""
        for i in self.matrix:
            default_str = ""
            for j in range(len(i)):
                default_str += ("{:>10}, ".format(str(i[j])) if (j < len(i) - 1) 
                                else "{:>10}".format(str(i[j])))
            result += str_start + default_str + str_end
        return result.strip()

    def get_dimension(self):
        return self.dimension

    def get_diagonal(self):
        return self.diagonal

    def set_diagonal(self, alist):
        if len(alist) != self.dimension:
            diff = len(alist) - self.dimension
            diff1 = "more" if x < 0 else "less"
            raise Exception("Please enter {} {} values to your inputted list"
                             .format(abs(diff), diff2))
        else:
            for i in range(self.dimension):
                self.matrix[i][i] = alist[i]

    def create_matrix(self):
        letters = [chr(x) for x in range(self.get_num_entries() + 96, 96, -1)]
        diagonal = ['l{}'.format(x) for x in range(1, self.dimension + 1)]
        letter_tracker = len(letters)
        for i in range(self.dimension):
            for j in range(i, self.dimension):
                if i == j:
                    new_val = input("For entry at {}, enter any key to set to 0 or press 'Enter'  for {} to remain: " .format((i, j), diagonal[i]))
                    if not new_val:
                        self.matrix[i][j] = diagonal[i]
                    else:
                        self.matrix[i][j] = '0'
                        diagonal.remove(diagonal[i])
                    self.matrix[i][i] = diagonal[i] if not new_val else "0"
                    if new_val:
                        diagonal[i] = None
                else:
                    letter_tracker -= 1
                    current_letter = letters[letter_tracker]
                    new_val = input("For entry at {}, enter any key to set to 0 or press 'Enter'  for {} to remain: " .format((i, j), current_letter))
                    self.matrix[i][j] = current_letter if not new_val else "0"
                    if new_val:
                        letters[letter_tracker] = None
        self.scale_matrix(letters, diagonal)
        
    def scale_matrix(self, letters, diagonal):
        scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
        while scaler and not (scaler in diagonal or scaler in letters):
            print("Please enter a value present in the given matrix to scale.")
            scaler = input('Enter the value from the matrix you wish to scale to 1, or press "Enter": ')
        for i in range(self.dimension):
            for j in range(i, self.dimension):
                if self.matrix[i][j] == scaler:
                    self.matrix[i][j] = '1'
                    break

    def get_num_entries(self):
        return int(self.dimension * (self.dimension - 1) / 2)

    def check_reducibility(self):
        assert self.dimension == 3
        if not '0' in self.diagonal:
            if (self.matrix[0][1] == '0' and (self.matrix[0][2] == '0' or self.matrix[1][2] == '0') or
                self.matrix[0][2] == '0' and (self.matrix[0][1] == '0' or self.matrix[1][2] == '0')):
                return True
        elif self.diagonal == ['0','0','0'] or self.diagonal == ['l1','0','l3']:
            if self.matrix[0][1] == '0' or self.matrix[1][2] == '0':
                return True
        else:
            if self.diagonal == ['0','0','l3']:
                if self.matrix[0][1] == '0' and (self.matrix[0][2] == '0' or self.matrix[1][2] == '0'):
                    return True
            elif self.diagonal == ['l1','0','0']:
                if self.matrix[1][2] == '0' and (self.matrix[0][1] == '0' or self.matrix[0][2] == '0'):
                    return True
        return False

def set_dimension():
    try:
        dimension = int(input("Enter the dimension of your Matrix: "))
        if dimension > 6 or dimension < 3:
            raise Error
        return dimension
    except:
        print("Please enter a valid integer between 3 and 5")
        exit()
