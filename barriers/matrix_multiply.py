import time
from random import Random
from threading import Barrier, Thread

matrix_size = 200

# matrix_a = [
#     [3,1,-4],
#     [2,-3,1],
#     [5,-2,0]
# ]
#
# matrix_b = [
#     [1,-2,-1],
#     [0,5,4],
#     [-1,-2,3]
# ]

random = Random()

matrix_a = [[0] * matrix_size for r in range(matrix_size)]
matrix_b = [[0] * matrix_size for r in range(matrix_size)]
result = [[0] * matrix_size for r in range(matrix_size)]

work_start = Barrier(matrix_size + 1)
work_complete = Barrier(matrix_size + 1)


def generate_random_matrix(matrix):
    for row in range(matrix_size):
        for col in range(matrix_size):
            matrix[row][col] = random.randint(-5, 5)


def work_out_row(row):
    while True:
        work_start.wait()
        for col in range(matrix_size):
            for i in range(matrix_size):
                result[row][col] += matrix_a[row][i] * matrix_b[i][col]
        work_complete.wait()


for row in range(matrix_size):
    Thread(target=work_out_row,args=([row])).start()


start = time.time()

for t in range(10):
    generate_random_matrix(matrix_a)
    generate_random_matrix(matrix_b)
    result = [[0] * matrix_size for r in range(matrix_size)]
    work_start.wait()

    # for row in range(matrix_size):
    #     print(matrix_a[row],matrix_b[row],result[row])
end = time.time()
print("Done, ", end - start)
