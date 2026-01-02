import pytest
from matrix_transformation import MatrixTransformation


class TestMatrixTransformationRotateClockwise:
    """Test cases for rotate_matrix_90_clockwise method."""

    @pytest.mark.parametrize("input_matrix,expected", [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
        ([[1, 2], [3, 4]], [[3, 1], [4, 2]]),
        ([[1, 2, 3], [4, 5, 6]], [[4, 1], [5, 2], [6, 3]]),
        ([[1]], [[1]]),
        ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], 
         [[9, 5, 1], [10, 6, 2], [11, 7, 3], [12, 8, 4]]),
    ])
    def test_rotate_matrix_90_clockwise(self, input_matrix, expected):
        """Test rotate_matrix_90_clockwise with various matrices."""
        assert MatrixTransformation.rotate_matrix_90_clockwise(input_matrix) == expected

    def test_rotate_matrix_90_clockwise_empty(self):
        """Test rotate_matrix_90_clockwise with empty matrix."""
        assert MatrixTransformation.rotate_matrix_90_clockwise([]) == []


class TestMatrixTransformationRotateCounterclockwise:
    """Test cases for rotate_matrix_90_counterclockwise method."""

    @pytest.mark.parametrize("input_matrix,expected", [
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[3, 6, 9], [2, 5, 8], [1, 4, 7]]),
        ([[1, 2], [3, 4]], [[2, 4], [1, 3]]),
        ([[1]], [[1]]),
    ])
    def test_rotate_matrix_90_counterclockwise(self, input_matrix, expected):
        """Test rotate_matrix_90_counterclockwise with various matrices."""
        assert MatrixTransformation.rotate_matrix_90_counterclockwise(input_matrix) == expected


class TestMatrixTransformationTranspose:
    """Test cases for transpose_matrix method."""

    @pytest.mark.parametrize("input_matrix,expected", [
        ([[1, 2, 3], [4, 5, 6]], [[1, 4], [2, 5], [3, 6]]),
        ([[1, 2], [3, 4], [5, 6]], [[1, 3, 5], [2, 4, 6]]),
        ([[1]], [[1]]),
        ([[1, 2, 3]], [[1], [2], [3]]),
    ])
    def test_transpose_matrix(self, input_matrix, expected):
        """Test transpose_matrix with various matrices."""
        assert MatrixTransformation.transpose_matrix(input_matrix) == expected


class TestMatrixTransformationScale:
    """Test cases for scaleMatrix method."""

    def test_scale_matrix_positive_scalar(self):
        """Test scaleMatrix with positive scalar."""
        matrix = [[1, 2], [3, 4]]
        result = MatrixTransformation.scaleMatrix(matrix, 2)
        assert result == [[2, 4], [6, 8]]

    def test_scale_matrix_zero_scalar(self):
        """Test scaleMatrix with zero scalar."""
        matrix = [[1, 2], [3, 4]]
        result = MatrixTransformation.scaleMatrix(matrix, 0)
        assert result == [[0, 0], [0, 0]]

    def test_scale_matrix_negative_scalar(self):
        """Test scaleMatrix with negative scalar."""
        matrix = [[1, 2], [3, 4]]
        result = MatrixTransformation.scaleMatrix(matrix, -1)
        assert result == [[-1, -2], [-3, -4]]

    def test_scale_matrix_float_scalar(self):
        """Test scaleMatrix with float scalar."""
        matrix = [[1, 2], [4, 6]]
        result = MatrixTransformation.scaleMatrix(matrix, 0.5)
        assert result == [[0.5, 1.0], [2.0, 3.0]]

    @pytest.mark.parametrize("scalar", [1, 3, 5, -2, 0.5])
    def test_scale_matrix_various_scalars(self, scalar):
        """Test scaleMatrix with various scalar values."""
        matrix = [[2, 3], [4, 5]]
        result = MatrixTransformation.scaleMatrix(matrix, scalar)
        expected = [[2 * scalar, 3 * scalar], [4 * scalar, 5 * scalar]]
        assert result == expected


class TestMatrixTransformationSwapRows:
    """Test cases for swapRows method."""

    def test_swap_rows_basic(self):
        """Test swapRows with basic matrix."""
        matrix = [[1, 2], [3, 4], [5, 6]]
        MatrixTransformation.swapRows(matrix, 0, 2)
        assert matrix == [[5, 6], [3, 4], [1, 2]]

    def test_swap_rows_adjacent(self):
        """Test swapRows with adjacent rows."""
        matrix = [[1, 2], [3, 4], [5, 6]]
        MatrixTransformation.swapRows(matrix, 0, 1)
        assert matrix == [[3, 4], [1, 2], [5, 6]]

    def test_swap_rows_same_row(self):
        """Test swapRows with same row index."""
        matrix = [[1, 2], [3, 4]]
        original = [row[:] for row in matrix]
        MatrixTransformation.swapRows(matrix, 0, 0)
        assert matrix == original

    def test_swap_rows_two_by_two(self):
        """Test swapRows on 2x2 matrix."""
        matrix = [[1, 2], [3, 4]]
        MatrixTransformation.swapRows(matrix, 0, 1)
        assert matrix == [[3, 4], [1, 2]]


class TestMatrixTransformationSwapColumns:
    """Test cases for swapColumns method."""

    def test_swap_columns_basic(self):
        """Test swapColumns with basic matrix."""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        MatrixTransformation.swapColumns(matrix, 0, 2)
        assert matrix == [[3, 2, 1], [6, 5, 4], [9, 8, 7]]

    def test_swap_columns_adjacent(self):
        """Test swapColumns with adjacent columns."""
        matrix = [[1, 2, 3], [4, 5, 6]]
        MatrixTransformation.swapColumns(matrix, 0, 1)
        assert matrix == [[2, 1, 3], [5, 4, 6]]

    def test_swap_columns_same_column(self):
        """Test swapColumns with same column index."""
        matrix = [[1, 2], [3, 4]]
        original = [row[:] for row in matrix]
        MatrixTransformation.swapColumns(matrix, 0, 0)
        assert matrix == original

    def test_swap_columns_single_row(self):
        """Test swapColumns on single row matrix."""
        matrix = [[1, 2, 3]]
        MatrixTransformation.swapColumns(matrix, 0, 2)
        assert matrix == [[3, 2, 1]]


class TestMatrixTransformationMultiply:
    """Test cases for multiplyMatrices method."""

    def test_multiply_matrices_basic(self):
        """Test multiplyMatrices with basic matrices."""
        matrixA = [[1, 2], [3, 4]]
        matrixB = [[5, 6], [7, 8]]
        result = MatrixTransformation.multiplyMatrices(matrixA, matrixB)
        expected = [[19, 22], [43, 50]]
        assert result == expected

    def test_multiply_matrices_different_dimensions(self):
        """Test multiplyMatrices with different dimension matrices."""
        matrixA = [[1, 2, 3], [4, 5, 6]]
        matrixB = [[7, 8], [9, 10], [11, 12]]
        result = MatrixTransformation.multiplyMatrices(matrixA, matrixB)
        expected = [[58, 64], [139, 154]]
        assert result == expected

    def test_multiply_matrices_identity(self):
        """Test multiplyMatrices with identity matrix."""
        matrixA = [[1, 2], [3, 4]]
        identity = [[1, 0], [0, 1]]
        result = MatrixTransformation.multiplyMatrices(matrixA, identity)
        assert result == matrixA

    def test_multiply_matrices_incompatible_dimensions(self):
        """Test multiplyMatrices with incompatible dimensions."""
        matrixA = [[1, 2], [3, 4]]
        matrixB = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        with pytest.raises(ValueError, match="Number of columns in matrix A must equal number of rows in matrix B"):
            MatrixTransformation.multiplyMatrices(matrixA, matrixB)

    def test_multiply_matrices_single_element(self):
        """Test multiplyMatrices with single element matrices."""
        matrixA = [[5]]
        matrixB = [[3]]
        result = MatrixTransformation.multiplyMatrices(matrixA, matrixB)
        assert result == [[15]]


class TestMatrixTransformationRandom:
    """Test cases for randomMatrix method."""

    def test_random_matrix_dimensions(self):
        """Test randomMatrix returns correct dimensions."""
        matrix = MatrixTransformation.randomMatrix(3, 4)
        assert len(matrix) == 3
        assert all(len(row) == 4 for row in matrix)

    def test_random_matrix_default_range(self):
        """Test randomMatrix with default value range."""
        matrix = MatrixTransformation.randomMatrix(5, 5)
        for row in matrix:
            for element in row:
                assert 0 <= element <= 10

    def test_random_matrix_custom_range(self):
        """Test randomMatrix with custom value range."""
        matrix = MatrixTransformation.randomMatrix(4, 4, minValue=50, maxValue=100)
        for row in matrix:
            for element in row:
                assert 50 <= element <= 100

    def test_random_matrix_single_row(self):
        """Test randomMatrix with single row."""
        matrix = MatrixTransformation.randomMatrix(1, 5)
        assert len(matrix) == 1
        assert len(matrix[0]) == 5

    def test_random_matrix_single_column(self):
        """Test randomMatrix with single column."""
        matrix = MatrixTransformation.randomMatrix(5, 1)
        assert len(matrix) == 5
        assert all(len(row) == 1 for row in matrix)

    def test_random_matrix_negative_range(self):
        """Test randomMatrix with negative value range."""
        matrix = MatrixTransformation.randomMatrix(3, 3, minValue=-10, maxValue=-1)
        for row in matrix:
            for element in row:
                assert -10 <= element <= -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
