import math

def solution(src, dest):
    fm = findMove(src, dest) 
    return fm.minMoves(src, dest)

class findMove:

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.visited = [[-1]* 8 for i in range(8)]


    def minMoves(self, src, dst):
        steps = 0
        self.q = [src]
        
        while len(self.q):
            qn = len(self.q)
            if any(item == dst for item in self.q):
                return steps
            else: 
                steps += 1
                for item in self.q:
                    self.q = self.q + self.nextDst(item)

            self.q = self.q[qn:]

        return steps 


    def toCoords(self, d):
        i = math.trunc(d / 8)
        j = d % 8
        return (i, j)

    def nextDst(self, src):
        dsts = []
        i, j = self.toCoords(src)
        #print(i,j, self.visited[i][j])

        if self.visited[i][j] != -1:
            return []

        self.visited[i][j] = 1
        if i > 0 and j > 1: dsts.append((i-1) * 8 + j - 2) 
        if i > 0 and j < 6: dsts.append((i-1) * 8 + j + 2) 

        if i < 7 and j > 1: dsts.append((i+1) * 8 + j - 2) 
        if i < 7 and j < 6: dsts.append((i+1) * 8 + j + 2) 

        if i > 1 and j > 0: dsts.append((i-2) * 8 + j - 1) 
        if i > 1 and j < 7: dsts.append((i-2) * 8 + j + 1) 

        if i < 6 and j > 0: dsts.append((i+2) * 8 + j - 1) 
        if i < 6 and j < 7: dsts.append((i+2) * 8 + j + 1) 

        return dsts

#print("0, 1:", solution(0,1))
#print("19, 36:", solution(19,36))
#print("0,63", solution(0,63))
print("0,63", solution(0,29))
print("0,63", solution(0,20))
print("0,63", solution(0,14))
print("0,63", solution(0,7))
print("0,63", solution(0,15))


"""
-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------
"""
