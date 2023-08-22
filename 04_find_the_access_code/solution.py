def solution(l):
    if len(l) <= 2:
        return 0

    divisible = {}
    for i, num in enumerate(l):
        key = "{0}_{1}".format(i, num)
        divisible[key] = divisible[key] if key in divisible else {}
        divisible[key].update(getAllDivisible(l[i + 1:], num, i))

    # print(divisible)

    #for all divisible follow the path till tuple length is 3
    luckyTriples = []
    for i, li in enumerate(l):
        for j in divisible["{0}_{1}".format(i, li)]:
            for k in divisible[j]:
                lj = j.split("_")[0]
                lk = k.split("_")[0]
                luckyTriples.append(
                    (li, j[1], k[1])) if li < lj and lj < lk else None
    return len(luckyTriples)


def getAllDivisible(l, num, idx):
    out = {}
    [
        out.update({"{0}_{1}".format(idx + k + 1, v): v}) if v %
        num == 0 else None for k, v in enumerate(l)
    ]
    return out


# TODO: Timeout is the issue
# print("LT: ", solution([1, 2, 3, 4, 5, 6]))
# print("LT: ", solution([1, 2, 3, 4, 5, 6, 8, 9]))
# print("LT: ", solution([2, 8, 6, 7, 5, 3]))
# print("LT: ", solution([2, 8]))
print("LT: ", solution([1, 1, 1]))
print("LT: ", solution([i for i in range(1, 2000)]))
print("LT: ", solution([1] * 500))
# print("LT: ", solution([1, 1, 1, 1, 1]))
