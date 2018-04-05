import random
import re


Foods = []       #     /*Foods is the population of food sources. Each row of Foods matrix is a vector holding D parameters to be optimized. The number of rows of Foods matrix equals to the FoodNumber*/
f = []              # /*f is a vector holding objective function values associated with food sources */
fitness = []        # /*fitness is a vector holding fitness (quality) values associated with food sources*/
trial = []          #  /*trial is a vector holding trial numbers through which solutions can not be improved*/
prob = []           #  /*prob is a vector holding probabilities of food sources (solutions) to be chosen*/
solution = []            #/*New solution (neighbour) produced by v_{ij}=x_{ij}+\phi_{ij}*(x_{kj}-x_{ij}) j is a randomly chosen parameter and k is a randomlu chosen solution different from i


def initial_solution(weights, capacity, total):
    randList = random.sample(range(0, len(weights)), len(weights))
    i = 0
    solutionList = []
    while total <= capacity:
        randomIndex = randList[i]
        i+=1
        total += weights[randomIndex]
        solutionList.append(randomIndex)
    
    return sorted(solutionList)




dataset = open("data.txt", "r")

n = int(dataset.readline().strip())
print(n)
weights = list(map(int, dataset.readline().strip().split()))
weights = weights[:len(weights)]
#print(ar)

capacity = int(dataset.readline().strip())

#print(c)
risk_ar = []
for i in range(n-1):
    
    temp_list = list(map(int, dataset.readline().strip().split()))
    risk_ar.append(temp_list)

solution = initial_solution(weights, capacity, 0)
i = 0
l=0

#print(len(risk_ar[1]))


min_risk = 10000000000000000
    