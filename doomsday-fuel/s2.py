import copy
import fractions


def number_of_transients(matrix):
    """Get number of transients states.

    Assume absorbing states follow transient states
    without interlieveing."""

    for r, row in enumerate(matrix):
        for col in row:
            if col != 0:
                break  # This is not an all-zero row, try next one
        else:
            return r  # Has just finished looping over an empty row


def decompose(matrix):
    """Decompose input matrix on Q and R components."""

    transients = number_of_transients(matrix)

    q_matrix = [matrix[i][:transients] for i in range(transients)]
    r_matrix = [matrix[i][transients:] for i in range(transients)]

    return q_matrix, r_matrix


def identity(size):
    """Return identity matrix of given size."""

    matrix = []

    for i in range(size):
        row = []

        for j in range(size):
            row.append(int(i == j))

        matrix.append(row)

    return matrix


def is_zero(matrix):
    """Check if the matrix is zero."""

    for row in matrix:
        for col in row:
            if col != 0:
                return False

    return True


def swap(matrix, i, j):
    """Swap i, j rows/columns of a square matrix."""

    swapped = copy.deepcopy(matrix)
    swapped[i], swapped[j] = swapped[j], swapped[i]

    for row in swapped:
        row[i], row[j] = row[j], row[i]

    return swapped


def sort_matrix(matrix):
    """Reorder matrix so zero-rows go last."""

    size = len(matrix)
    zero_row = -1

    for r in range(size):
        row_sum = 0

        for c in range(size):
            row_sum += matrix[r][c]

        if row_sum == 0:
            zero_row = r  # Save the found zero-row
        elif row_sum != 0 and zero_row > -1:
            # We have found non-zero row after all-zero row:
            # swap these rows and repeat from the begining.

            sorted_matrix = swap(matrix, r, zero_row)
            return sort_matrix(sorted_matrix)

    return matrix  # Nothing to sort, return original matrix


def normalize(matrix):
    """Normalize matrix."""

    normalized = copy.deepcopy(matrix)

    for r, row in enumerate(matrix):
        row_sum = sum(row) or 1

        for c, col in enumerate(row):
            normalized[r][c] = fractions.Fraction(col, row_sum)

    return normalized


def subtract(matrix_a, matrix_b):
    """Subtract two matrices."""

    subtracted_matrix = copy.deepcopy(matrix_a)

    for r, row in enumerate(matrix_a):
        subtracted_matrix[r] = [
            col - matrix_b[r][c] for c, col in enumerate(row)]

    return subtracted_matrix


def multiply(matrix_a, matrix_b):
    """Multiply two matrices."""

    multiplied_matrix = []

    cols = len(matrix_b[0])
    iters = len(matrix_a[0])

    for r, row in enumerate(matrix_a):
        multiplied_row = []

        for c in range(cols):
            col_sum = 0

            for i in range(iters):
                col_sum += row[i] * matrix_b[i][c]

            multiplied_row.append(col_sum)

        multiplied_matrix.append(multiplied_row)

    return multiplied_matrix


def transpose_matrix(matrix):
    """Transpose matrix."""

    return [list(row) for row in zip(*matrix)]


def get_matrix_minor(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def get_matrix_determinant(matrix):
    """Get matrix determinant."""

    # Base case for 2x2 matrix
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0

    for c in range(len(matrix)):
        determinant += ((-1) ** c) * matrix[0][c] * get_matrix_determinant(
            get_matrix_minor(matrix, 0, c))

    return determinant


def get_matrix_inverse(matrix):
    """Get matrix inversion."""

    determinant = get_matrix_determinant(matrix)

    # Special case for 2x2 matrix
    if len(matrix) == 2:
        return [
            [matrix[1][1] / determinant, -1 * matrix[0][1] / determinant],
            [-1 * matrix[1][0] / determinant, matrix[0][0] / determinant],
        ]

    # Find matrix of cofactors
    cofactors = []

    for r in range(len(matrix)):
        cofactorRow = []

        for c in range(len(matrix)):
            minor = get_matrix_minor(matrix, r, c)
            cofactorRow.append(
                ((-1) ** (r + c)) * get_matrix_determinant(minor))

        cofactors.append(cofactorRow)

    cofactors = transpose_matrix(cofactors)

    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant

    return cofactors


def format_output(probabilities):
    def lcm(a, b):
        return abs(a * b) // fractions.gcd(a, b)

    res = []

    denominator = probabilities[0]._denominator

    for probability in probabilities[1:]:
        denominator = lcm(denominator, probability._denominator)

    for probability in probabilities:
        res.append(
            probability._numerator * (denominator / probability._denominator))

    res.append(denominator)
    return res


# Updated solution function to handle the single-state scenario
def solution(matrix):
    num_states = len(matrix)
    
    # Special case: single state
    if num_states == 1:
        return [1 - matrix[0][0], 1]
    
    num_transients = number_of_transients(matrix)
    
    # Special case: all states are terminal
    if num_transients == 0:
        result = [0] * (num_states - 1)
        result.insert(0, 1)  # Initial state
        result.append(1)  # Denominator
        return result
    
    m = sort_matrix(matrix)
    n = normalize(m)
    q, r = decompose(n)
    i = identity(len(q))
    s = subtract(i, q)
    v = get_matrix_inverse(s)
    b = multiply(v, r)
    return format_output(b[0])


print(solution([
[0,1,0,0,0,1], # s0, the initial state, goes to s1 and s5 with equal probability
[4,0,0,3,2,0], # s1 can become s0, s3, or s4, but with different probabilities
[0,0,0,0,0,0], # s2 is terminal, and unreachable (never observed in practice)
[0,0,0,0,0,0], # s3 is terminal
[0,0,0,0,0,0], # s4 is terminal
[0,0,0,0,0,0], # s5 is terminal
]))

print(solution([
    [0, 2, 1, 0, 0], 
    [0, 0, 0, 3, 4], 
    [0, 0, 0, 0, 0], 
    [0, 0, 0, 0,0], 
    [0, 0, 0, 0, 0]
    ]))
#print(solution([
#    [1, 0, 0, 0, 0], 
#    [1, 0, 0, 0, 1], 
#    [0, 0, 0, 0, 0], 
#    [0, 0, 0, 0,0], 
#    [0, 0, 0, 0, 0]
#    ]))
#print(solution([
    #    [1, 0, 0, 0, 1], 
    #    [0, 0, 0, 0, 0], 
    #    [0, 0, 0, 0, 0], 
    #    [0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0]
    #    ]))
#
print(solution([[1]]))
print(solution([[0]]))
print(solution([[100]]))
#print(solution([[1, 1, 1, 1, 1,],
#                [0, 0, 0, 0, 0,], 
#                [1, 1, 1, 1, 1,], 
#                [0, 0, 0, 0, 0,], 
#                [1, 1, 1, 1, 1,]
#                ]))
##
#print(solution(
#    [[10, 1, 1, 1, 1,],
#                [0, 0, 0, 0, 0,], 
#                [1, 1, 1, 1, 1,], 
#                [0, 0, 0, 0, 0,], 
#                [1, 1, 1, 1, 1,]
#                ]
#    ))
print(solution([[10, 1, 1, 1, 1,],
                [1, 1, 0, 0, 0,], 
                [1, 0, 0, 0, 0,], 
                [1, 0, 0, 0, 0,], 
                [1, 0, 0, 0, 0,]
                ]))



