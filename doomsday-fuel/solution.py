from fractions import Fraction
import copy

def solution(matrix):
    try:
        return OreTransition(matrix).getTransitionProbabilities()
    except Exception as ins:
        res = [ 0 for _ in range(len(matrix ))]
        res[0] = 1
        if len(matrix) == 1:
            res[0] = 1 - matrix[0][0]
        return res + [1]


class OreTransition:
    def __init__(self, matrix):
        self.__matrix = matrix
        return None

    def p(self, mat):
        print("--------")
        for row in mat:
            print(row)
        print("--------")

    def getTransitionProbabilities(self):
        transitions = self.__getLimitingMatrix(self.__matrix)

        # we want only the transition from s0 to terminal states
        interestedTransition = transitions[0]

        #since all of them have been reduced to simple forms the max deno is the common one
        commonDeno = max(list(map(lambda x: x[1], interestedTransition)))
        #multiply the numerators to satify the scale up to commonDeno
        result = list(map(lambda x: (commonDeno/x[1]) * x[0], interestedTransition))
        return result + [commonDeno] 


    def __getLimitingMatrix(self, mat):
        sfMatrixTuple = self.__toStandardForm(mat)

        nonterminalProb = self.__getNonTerminalProbabilities(sfMatrixTuple)
        
        terminalProb = self.__getTerminalProbabilities(sfMatrixTuple)
        self.p(terminalProb)
        self.p(nonterminalProb)

        f = self.__getF(terminalProb)
        t = self.__mulMatrices(f, nonterminalProb)

        #convert to simple fractions
        result = []
        for row in t:
            rowRes = []
            for col in row:
                n,d  = self.simplifyFract(col)
                rowRes.append((n, d))
            result.append(rowRes)
        return result
    
    def __toStandardForm(self, mat):
        result = []
        terminalStates = self.__getTerminalStatesIdx(mat)
        if len(terminalStates) == len(mat):
            raise Exception("irreducible chain detected")

        if 0 in terminalStates:
            raise Exception("s0 is a terminal state")
        self.__toProbabilityFractions()

        idenRowLen = len(self.__matrix[0])
        # get all the terminal states and make it top rows, additionally make the itentity matrix
        for i in range(len(terminalStates)):
            idenRow = [1 if j == i else 0 for j in range(idenRowLen)]
            result.append(idenRow)

        # remainin non-terminal states are placed at bottom
        nonTerminals = sorted(list(filter(lambda x: x not in terminalStates, range(len(self.__matrix)))))
        for i in nonTerminals:
            #rearrage to match the new order
            row = []
            for j in terminalStates + nonTerminals:
                row.append(self.__matrix[i][j]) 
            result.append(row)
        
        return (len(terminalStates), result)
    

    def __getNonTerminalProbabilities(self, sfMatrixTuple):
        #we need the submatrix R(non-terminal probs), which are located at the bottom of the sfMatrix
        start = sfMatrixTuple[0]
        sfMatrix = sfMatrixTuple[1]
        end = len(sfMatrix)
        result = [[]for _ in range(end-start)]
        for i in range(start, end):
            result[i - start] = copy.deepcopy(sfMatrix[i][0: start])

        return result

    def __getTerminalProbabilities(self, sfMatrixTuple):
        start = sfMatrixTuple[0]
        sfMatrix = sfMatrixTuple[1]
        end = len(sfMatrix)
        result = [[] for _ in range(start, end)]
        
        for i in range(start, end):
            result[i - start] = sfMatrix[i][start: end]

        return result



    def __getTerminalStatesIdx(self, mat):
        return list(
                filter(
                    lambda x: x >=0, 
                    [
                        i if row[i] >= 1 or sum(row) == 0 else -1 
                        for i, row in enumerate(mat)
                        ]
                    )
                )
            
    def __toProbabilityFractions(self):
        for i, row in enumerate(self.__matrix):
            rowSum = sum(row)
            self.__matrix[i] = [(row[j], rowSum) if rowSum > 0 else 0 for j in range(len(row))]
                
        return None

    #gets F, the inverse of I-Q, where I is identity mat of Q
    def __getF(self, terminalProb):
        iden = [[(1, 1) if i == j else (0,1) for i,_ in enumerate(row)] for j, row in enumerate(terminalProb)]
        iSubQ = self.__subtractMatrices(iden, terminalProb)
        return self.__invertMatrix(iSubQ)

    
    def __subtractMatrices(self,a, b):
        result = []
        for i, row in enumerate(a):
            result.append([0 for _ in range(len(row))])
            for j, _ in enumerate(row):

                result[i][j] = self.subFract(a[i][j], b[i][j]) 

        return result

    def __mulMatrices(self,a, b):
        result = []
        for i, row in enumerate(a): #for each row
            rowRes = []
            for j in range(len(b[i])): #for each col
                sum = (0,0)
                for k in range(len(b)):
                    sum = self.addFract(sum, self.mulFract(row[k], b[k][j]))
                rowRes.append(sum)
            result.append(rowRes)

        return result

    def __getSubMatrix(self, mat, exI, exJ):
        result = []
        for i in range(len(mat)):
            if i != exI:
                result.append(copy.deepcopy(mat[i][0:exJ]) + copy.deepcopy(mat[i][exJ+1:]))

        return result


    def __invertMatrix(self, mat):
        det = self.__getDeterminant(mat)
        cofact = self.__getCofactorMatrix(mat)
        n, d = self.simplifyFract(det)

        for i in range(len(cofact)):
            for j in range(len(cofact[i])):
                v =  self.mulFract((d,n), cofact[i][j])
                cofact[i][j] = self.simplifyFract(v) 

        return cofact

    def __getDeterminant(self, mat = [[0]]):
        if len(mat) < 2:
            return mat[0][0]
        if len(mat) == 2:
            return self.subFract(
                        self.mulFract(mat[0][0], mat[1][1]), self.mulFract(mat[0][1], mat[1][0])
                    )

        det = (0, 0)
        for i, cell in enumerate(mat[0]):
            d = self.mulFract(
                    self.mulFract(((1,1) if i%2 == 0 else (-1,1)), cell), 
                    self.__getDeterminant(self.__getSubMatrix(mat, 0, i))
                    )
            det = self.addFract(det, d)
        return det


    def __getCofactorMatrix(self, mat):
        if len(mat) < 2:
            return [[(1, 1)]]

        result = []
        for i, row in enumerate(mat):
            resultRow = []
            rowSign = 1 if i%2==0 else -1
            for j, _ in enumerate(row):
                cellSign = 1 if j%2==0 else -1
                resultRow.append(self.mulFract(
                    (rowSign * cellSign, 1),
                    self.__getDeterminant(self.__getSubMatrix(mat, i, j))
                    ))
            result.append(resultRow)
        return self.transpose(result)

    def transpose(self, mat):
        result = [[0 for _ in range(len(mat))] for _ in range(len(mat))]

        for i, row in enumerate(mat):
            for j in range(len(mat[i])):
                result[j][i] = row[j]

        return result

    #fraction utilities
    def addFract(self, a,b):
        if a[0] == 0:
            return b

        if b[0] == 0:
            return a

        return self.simplifyFract((a[0]*b[1] + a[1]*b[0], a[1] * b[1]))


    def subFract(self, a,b):
        if a[0] == 0:
            return self.mulFract((-1,1), b)
        if b[0] == 0:
            return a
        return self.simplifyFract((a[0]*b[1] - a[1]*b[0], a[1] * b[1]))


    def mulFract(self, a,b):
        return (a[0]*b[0], a[1] * b[1])

    def simplifyFract(self, a):
        if a[1] == 0:
            return a
        fa = Fraction(a[0], a[1])
        return (fa.numerator, fa.denominator)
#
#print(solution([
#[0,1,0,0,0,1], # s0, the initial state, goes to s1 and s5 with equal probability
#[4,0,0,3,2,0], # s1 can become s0, s3, or s4, but with different probabilities
#[0,0,0,0,0,0], # s2 is terminal, and unreachable (never observed in practice)
#[0,0,0,0,0,0], # s3 is terminal
#[0,0,0,0,0,0], # s4 is terminal
#[0,0,0,0,0,0], # s5 is terminal
#]))
#
#print(solution([
#    [0, 2, 1, 0, 0], 
#    [0, 0, 0, 3, 4], 
#    [0, 0, 0, 0, 0], 
#    [0, 0, 0, 0,0], 
#    [0, 0, 0, 0, 0]
#    ]))
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
#print(solution([[1]]))
#print(solution([[0]]))
#print(solution([[100]]))
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
print(solution([[0, 1, 1, 1, 1,],
                [1, 1, 0, 0, 0,], 
                [1, 0, 1, 0, 0,], 
                [1, 0, 0, 1, 0,], 
                [1, 0, 0, 0, 1,]
                ]))


