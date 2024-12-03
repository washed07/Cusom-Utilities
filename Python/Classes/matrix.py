from math import nan, isnan

class Matrix:
    """
    A class to represent a matrix and perform various matrix operations.
    """

    def __init__(self, rows: int = 10, columns: int = 10):
        """
        Initialize the matrix with the given number of rows and columns.

        Args:
            rows (int): Number of rows in the matrix.
            columns (int): Number of columns in the matrix.
        """
        self.rows = rows
        self.columns = columns
        self.empty_index = None
        self.data = {f'r{row}c{col}': self.empty_index for row in range(1, self.rows + 1) for col in range(1, self.columns + 1)}

    def find_index(self, row: int = nan, column: int = nan):
        """
        Find the indices of the matrix elements based on the given row and/or column.

        Args:
            row (int): The row index.
            column (int): The column index.

        Returns:
            list: A list of keys representing the indices.
        """
        if not isnan(row) and isnan(column):
            return [key for key in self.data if key.startswith(f'r{row}')]
        if not isnan(column) and isnan(row):
            return [key for key in self.data if key.endswith(f'c{column}')]
        if not isnan(row) and not isnan(column):
            return [f'r{row}c{column}']
        return list(self.data.keys())

    def middle(self):
        """
        Get the middle index of the matrix.

        Returns:
            tuple: The middle index (row, column).
        """
        return (self.rows + 1) // 2, (self.columns + 1) // 2

    def get_middle(self):
        """
        Get the value of the middle element of the matrix.

        Returns:
            int: The value of the middle element.
        """
        return self.data[f'r{self.middle()[0]}c{self.middle()[1]}']

    def find(self, value) -> list:
        """
        Find the indices of the matrix elements that match the given value.

        Args:
            value: The value to search for.

        Returns:
            list: A list of keys representing the indices of matching elements.
        """
        return [key for key, val in self.data.items() if val == value]

    def get(self, row: int = nan, column: int = nan):
        """
        Get the values of the matrix elements based on the given row and/or column.

        Args:
            row (int): The row index.
            column (int): The column index.

        Returns:
            list: A list of values of the matching elements.
        """
        return [self.data[key] for key in self.find_index(row, column)].pop(0)

    def __setitem__(self, key, value):
        """
        Set the value of a matrix element at the given key.

        Args:
            key: The key representing the index of the element.
            value: The value to set.
        """
        self.data[key] = value

    def insert(self, value, row: int = nan, column: int = nan) -> None:
        """
        Insert a value into the matrix at the specified row and/or column.

        Args:
            value: The value to insert.
            row (int): The row index.
            column (int): The column index.
        """
        for key in self.find_index(row=row, column=column):
            self[key] = value

    def row(self, row: int = nan) -> list:
        """
        Get the values of the elements in the specified row.

        Args:
            row (int): The row index.

        Returns:
            list: A list of values in the specified row.
        """
        return self.get(row=row)

    def column(self, column: int = nan) -> list:
        """
        Get the values of the elements in the specified column.

        Args:
            column (int): The column index.

        Returns:
            list: A list of values in the specified column.
        """
        return self.get(column=column)

    def delete(self, row: int = nan, column: int = nan) -> None:
        """
        Delete the values of the elements in the specified row and/or column by setting them to the empty index.

        Args:
            row (int): The row index.
            column (int): The column index.
        """
        self.insert(self.empty_index, row, column)

    def print(self) -> None:
        """
        Print the matrix row by row.
        """
        for row in range(self.rows):
            print(self.row(row))

    def fill_rect(self, value, pos: tuple = (0, 0), area: tuple = None):
        """
        Fill a rectangular area of the matrix with the specified value.

        Args:
            value: The value to fill.
            pos (tuple): The starting position (row, column) of the rectangle.
            area (tuple): The size (rows, columns) of the rectangle.
        """
        if area is None:
            area = (self.rows, self.columns)
        for row in range(pos[0], pos[0] + area[0]):
            for col in range(pos[1], pos[1] + area[1]):
                if 0 <= row < self.rows and 0 <= col < self.columns:
                    self.insert(value, row, col)

    def fill_circ(self, center, radius, value):
        """
        Fill a circular area of the matrix with the specified value.

        Args:
            center (tuple): The center (row, column) of the circle.
            radius (int): The radius of the circle.
            value: The value to fill.
        """
        for row in range(center[0] - radius, center[0] + radius + 1):
            for col in range(center[1] - radius, center[1] + radius + 1):
                if (row - center[0]) ** 2 + (col - center[1]) ** 2 <= radius ** 2:
                    if 0 <= row < self.rows and 0 <= col < self.columns:
                        self.insert(value, row, col)

    def transpose(self):
        """
        Transpose the matrix by swapping rows and columns.
        """
        transposed_data = {f'r{col}c{row}': self.data[f'r{row}c{col}'] for row in range(self.rows) for col in
                           range(self.columns)}
        self.data = transposed_data
        self.rows, self.columns = self.columns, self.rows

    def determinant(self):
        """
        Calculate the determinant of the matrix.

        Returns:
            float: The determinant of the matrix.

        Raises:
            ValueError: If the matrix is not square.
        """
        if self.rows != self.columns:
            raise ValueError("Determinant is only defined for square matrices")
        return self._determinant_recursive(self._to_2d_list())

    def _determinant_recursive(self, matrix):
        """
        Recursively calculate the determinant of a matrix.

        Args:
            matrix (list): The matrix as a 2D list.

        Returns:
            float: The determinant of the matrix.
        """
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = 0
        for c in range(len(matrix)):
            det += ((-1) ** c) * matrix[0][c] * self._determinant_recursive(self._minor(matrix, 0, c))
        return det

    def _minor(self, matrix, row, col):
        """
        Calculate the minor of a matrix element.

        Args:
            matrix (list): The matrix as a 2D list.
            row (int): The row index of the element.
            col (int): The column index of the element.

        Returns:
            list: The minor matrix as a 2D list.
        """
        return [row[:col] + row[col + 1:] for row in (matrix[:row] + matrix[row + 1:])]

    def _to_2d_list(self):
        """
        Convert the matrix data to a 2D list.

        Returns:
            list: The matrix as a 2D list.
        """
        return [[self.data[f'r{row}c{col}'] for col in range(self.columns)] for row in range(self.rows)]

    def inverse(self):
        """
        Calculate the inverse of the matrix.

        Returns:
            list: The inverse matrix as a 2D list.

        Raises:
            ValueError: If the matrix is not square or is singular.
        """
        if self.rows != self.columns:
            raise ValueError("Inverse is only defined for square matrices")
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular and cannot be inverted")
        return self._inverse_matrix(self._to_2d_list(), det)

    def _inverse_matrix(self, matrix, det):
        """
        Calculate the inverse of a matrix given its determinant.

        Args:
            matrix (list): The matrix as a 2D list.
            det (float): The determinant of the matrix.

        Returns:
            list: The inverse matrix as a 2D list.
        """
        n = len(matrix)
        adjugate = [[self._cofactor(matrix, r, c) for c in range(n)] for r in range(n)]
        adjugate = list(map(list, zip(*adjugate)))  # Transpose
        return [[adjugate[r][c] / det for c in range(n)] for r in range(n)]

    def _cofactor(self, matrix, row, col):
        """
        Calculate the cofactor of a matrix element.

        Args:
            matrix (list): The matrix as a 2D list.
            row (int): The row index of the element.
            col (int): The column index of the element.

        Returns:
            float: The cofactor of the element.
        """
        minor = self._minor(matrix, row, col)
        return ((-1) ** (row + col)) * self._determinant_recursive(minor)

    def add(self, other):
        """
        Add another matrix to this matrix element-wise.

        Args:
            other (Matrix): The matrix to add.

        Raises:
            ValueError: If the matrices have different dimensions.
        """
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError("Matrices must have the same dimensions to be added")
        for row in range(self.rows):
            for col in range(self.columns):
                self.data[f'r{row}c{col}'] += other.data[f'r{row}c{col}']

    def multiply(self, other):
        """
        Multiply this matrix by another matrix or a scalar.

        Args:
            other (Matrix or scalar): The matrix or scalar to multiply by.

        Returns:
            Matrix: The result of the multiplication.

        Raises:
            ValueError: If the matrices cannot be multiplied.
        """
        if isinstance(other, Matrix):
            if self.columns != other.rows:
                raise ValueError("Matrices cannot be multiplied")
            result = Matrix(self.rows, other.columns)
            for i in range(self.rows):
                for j in range(other.columns):
                    result.data[f'r{i}c{j}'] = sum(
                        self.data[f'r{i}c{k}'] * other.data[f'r{k}c{j}'] for k in range(self.columns))
            return result
        else:  # Assume other is a scalar
            for key in self.data:
                self.data[key] *= other

    def trace(self):
        """
        Calculate the trace of the matrix (sum of the diagonal elements).

        Returns:
            float: The trace of the matrix.

        Raises:
            ValueError: If the matrix is not square.
        """
        if self.rows != self.columns:
            raise ValueError("Trace is only defined for square matrices")
        return sum(self.data[f'r{i}c{i}'] for i in range(self.rows))

    def submatrix(self, start_row, start_col, end_row, end_col):
        """
        Extract a submatrix from the matrix.

        Args:
            start_row (int): The starting row index.
            start_col (int): The starting column index.
            end_row (int): The ending row index.
            end_col (int): The ending column index.

        Returns:
            Matrix: The extracted submatrix.
        """
        sub = Matrix(end_row - start_row + 1, end_col - start_col + 1)
        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                sub.data[f'r{row - start_row}c{col - start_col}'] = self.data[f'r{row}c{col}']
        return sub

    def swap_rows(self, row1, row2):
        """
        Swap two rows in the matrix.

        Args:
            row1 (int): The first row index.
            row2 (int): The second row index.
        """
        for col in range(self.columns):
            self.data[f'r{row1}c{col}'], self.data[f'r{row2}c{col}'] = self.data[f'r{row2}c{col}'], self.data[
                f'r{row1}c{col}']

    def swap_columns(self, col1, col2):
        """
        Swap two columns in the matrix.

        Args:
            col1 (int): The first column index.
            col2 (int): The second column index.
        """
        for row in range(self.rows):
            self.data[f'r{row}c{col1}'], self.data[f'r{row}c{col2}'] = self.data[f'r{row}c{col2}'], self.data[
                f'r{row}c{col1}']

    def fill_diagonal(self, value):
        """
        Fill the diagonal of the matrix with the specified value.

        Args:
            value: The value to fill.
        """
        for i in range(min(self.rows, self.columns)):
            self.data[f'r{i}c{i}'] = value

    def power(self, n):
        """
        Raise the matrix to the given power.

        Args:
            n (int): The power to raise the matrix to.

        Returns:
            Matrix: The result of raising the matrix to the power.

        Raises:
            ValueError: If the matrix is not square.
        """
        if self.rows != self.columns:
            raise ValueError("Power is only defined for square matrices")
        result = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            result.data[f'r{i}c{i}'] = 1  # Identity matrix
        for _ in range(n):
            result = result.multiply(self)
        return result

    def hadamard_product(self, other):
        """
        Compute the element-wise product of this matrix and another matrix.

        Args:
            other (Matrix): The matrix to multiply element-wise.

        Returns:
            Matrix: The result of the element-wise multiplication.

        Raises:
            ValueError: If the matrices have different dimensions.
        """
        if self.rows != other.rows or self.columns != other.columns:
            raise ValueError("Matrices must have the same dimensions for Hadamard product")
        result = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                result.data[f'r{row}c{col}'] = self.data[f'r{row}c{col}'] * other.data[f'r{row}c{col}']
        return result

    def norm(self):
        """
        Calculate the Frobenius norm of the matrix.

        Returns:
            float: The Frobenius norm of the matrix.
        """
        return sum(value ** 2 for value in self.data.values()) ** 0.5
