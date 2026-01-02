class MatrixTransformation:
    @staticmethod
    def randomMatrix(rows, cols, minValue=0, maxValue=10):
        import random
        return [[random.randint(minValue, maxValue) for _ in range(cols)] for _ in range(rows)]
    
    @staticmethod
    def scaleMatrix(matrix, scalar):
        return [[element * scalar for element in row] for row in matrix]
    
    @staticmethod
    def swapRows(matrix, row1, row2):
        matrix[row1], matrix[row2] = matrix[row2], matrix[row1]

    @staticmethod
    def swapColumns(matrix, col1, col2):
        for row in matrix:
            row[col1], row[col2] = row[col2], row[col1]

    @staticmethod
    def transpose_matrix(matrix):
        return [list(row) for row in zip(*matrix)]

    @staticmethod
    def rotate_matrix_90_clockwise(matrix):
        # Transpose, then reverse each row
        return [list(row) for row in zip(*matrix[::-1])]

    @staticmethod
    def rotate_matrix_90_counterclockwise(matrix):
        # Reverse each row, then transpose
        return [list(row) for row in zip(*matrix)][::-1]
    
    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            print(" ".join(map(str, row)))

    @staticmethod
    def multiplyMatrices(matrixA, matrixB):
        if len(matrixA[0]) != len(matrixB):
            raise ValueError("Number of columns in matrix A must equal number of rows in matrix B.")
        result = [[0 for _ in range(len(matrixB[0]))] for _ in range(len(matrixA))]
        for i in range(len(matrixA)):
            for j in range(len(matrixB[0])):
                for k in range(len(matrixB)):
                    result[i][j] += matrixA[i][k] * matrixB[k][j]
        return result
    
    @staticmethod
    def addMatrices(matrixA, matrixB):
        if len(matrixA) != len(matrixB) or len(matrixA[0]) != len(matrixB[0]):
            raise ValueError("Matrices must have the same dimensions for addition.")
        return [[matrixA[i][j] + matrixB[i][j] for j in range(len(matrixA[0]))] for i in range(len(matrixA))]   

