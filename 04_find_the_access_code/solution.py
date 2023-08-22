def solution(l):
    if len(l) <= 2:
        return 0

    count = 0
    soln = [0] * len(l)
    rl = list(reversed(l))
    for i, n in enumerate(rl):
        divCount = 0
        #for each check if it is divisible and if so get its count
        for j, last in enumerate(rl[:i]):
            # print("i: {0}, j:{1}, rl:{2}".format(i, j, rl[:i]))
            if last % n == 0:
                #this is the triplet
                if soln[j] > 0:
                    count += soln[j]
                divCount += 1

        soln[i] = divCount

    return count


print("LT: ", solution([1, 2, 3, 4, 5, 6]))
print("LT: ", solution([1, 2, 3, 4, 5, 6, 8, 9]))
# print("LT: ", solution([2, 8, 6, 7, 5, 3]))
# print("LT: ", solution([2, 8]))
print("LT: ", solution([1, 1, 1]))
# print("LT: ", solution([i for i in range(1, 2000)]))
# print("LT: ", solution([1] * 500))
# print("LT: ", solution([1, 1, 1, 1, 1]))
