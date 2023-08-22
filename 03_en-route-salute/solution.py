def solution(str):
    rAngle, lAngle, total = 0,0,0
    for char in str:
        if char == ">":
            rAngle += 1
        elif char == "<":
            total += rAngle


    return total * 2



print(solution("<<>><"))
print(solution("><<>><"))
print(solution("<<>><"))
print(solution("--->-><-><-->-"))
print(solution("---<-<>->>-->-"))
print(solution(">------------<"))
print(solution("<------------>"))
