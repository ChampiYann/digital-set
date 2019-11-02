from pprint import pprint
from itertools import combinations

general = list(combinations([i for i in range(12)],3))

matrix = [
    [
        [1,2,1,2],
        [2,3,2,2],
        [3,1,1,2]
    ],
    [
        [3,3,3,1],
        [1,3,1,1],
        [1,2,1,3]
    ],
    [
        [3,2,3,1],
        [3,2,2,1],
        [1,1,1,3]
    ],
    [
        [3,3,1,1],
        [1,3,1,2],
        [3,3,3,1]
    ]
]

shapeArray = [matrix[0][j][i] for j in range(3) for i in range(4)]
shapePos = list(combinations(shapeArray,3))
shapeSet = [sum(i)%3==0 for i in shapePos]

numArray = [matrix[1][j][i] for j in range(3) for i in range(4)]
numPos = list(combinations(numArray,3))
numSet = [sum(i)%3==0 for i in numPos]

colorArray = [matrix[2][j][i] for j in range(3) for i in range(4)]
colorPos = list(combinations(colorArray,3))
colorSet = [sum(i)%3==0 for i in colorPos]

fillArray = [matrix[3][j][i] for j in range(3) for i in range(4)]
fillPos = list(combinations(fillArray,3))
fillSet = [sum(i)%3==0 for i in fillPos]

setComb = [shapeSet[i] and numSet[i] and colorSet[i] and fillSet[i] for i in range(220)]

result = [i for i, x in enumerate(setComb) if x]

pprint([general[i] for i in result])