import json
from multiprocessing import Pool, cpu_count


def summMatrix(params):
    row, line, place = params
    if len(row) - len(line):
        raise ValueError
    return place, sum([row[i] * line[i] for i in range(len(row))])


if __name__ == '__main__':
    with open('matrix.json') as j_file:
        ourMatrix = json.load(j_file)
    First_matrix, Second_matrix = ourMatrix['one'], ourMatrix['two']

    resulting = []
    for i in range(len(First_matrix)):
        for j in range(len(Second_matrix[0])):
            resulting.append((First_matrix[i], [Second_matrix[x][j] for x in range(len(Second_matrix))], (i, j)))

    res = [[[] for _ in range(len(First_matrix))] for __ in range(len(First_matrix))]

    processes_pool = Pool(cpu_count())
    results = processes_pool.map(summMatrix, resulting)
    for i in results:
        place, res_c = i
        res[place[0]][place[1]] = res_c

    print(res)