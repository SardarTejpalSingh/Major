import random
import re

beeCount = 500
onlookersCount = beeCount//2
employedCount = beeCount//2
scout = 1
iterCount = 1
maxForagingCount = 20

dataset = open("data.txt", "r")

n = int(dataset.readline().strip())
weights = list(map(int, dataset.readline().strip().split()))
capacity = int(dataset.readline().strip())
risk_ar = []
for i in range(n-1):   
    temp_list = [0]*i 
    temp_list += map(int, dataset.readline().strip().split())
    risk_ar.append(temp_list)


def risk_calculator(solution):
    '''Returns the risk value of the solution'''
    risk_value = 0
    for i in range(n-1):
        for j in range(n-1):
            if i in solution and j in solution:
                risk_value += risk_ar[i][j]
    
    return risk_value


def initial_solution():
    '''Returns a list containing indices of initial solution'''
    randList = random.sample(range(0, len(weights)), len(weights))
    i , total = 0, 0
    solution = []
    while total < capacity and i < len(randList):
        randomIndex = randList[i]
        i+=1
        total += weights[randomIndex]
        solution.append(randomIndex)
    return sorted(solution)


def neighbouring_solution(solution):
    '''Returns a list containing indices of a neighbouring solution by updating 3 elements randomly'''
    removeList = random.sample(range(0, len(solution)), 3)      #Generate 3 random indices within the solution list
    for indexToRemove in removeList:            #Remove the elements at that specific indices
        solution.pop(indexToRemove%len(solution)) 
    newEleList = random.sample(range(0,len(weights)), len(weights))
    total = sum(solution)
    i = 0
    while total < capacity and i < len(newEleList):
        if newEleList[i] not in solution:
            solution.append(newEleList[i])
            total+=weights[newEleList[i]]
        i+=1
    return sorted(solution)


def launch_scout_bee(employedSolutions):
    '''Returns a new unique solution'''
    while True:
        newSolution = initial_solution()
        if newSolution not in employedSolutions:
            return newSolution


def printbestSolution(finalSolutions):
    '''Prints the solution with minimum risk and its risk value'''
    index, i  = 0, 0
    minRisk = 100000000000000000000
    for everySolution in finalSolutions:
        risk = risk_calculator(everySolution)
        if risk < minRisk:
            minRisk = risk
            index = i
        i += 1
    for j in finalSolutions[index]:
        print(weights[j], end=" ")
    print(" Risk = ",minRisk)    

def init():
    '''Algorithm begins here'''
    for algIteration in range(iterCount):     #Algorithm repeater loop
        employedSolutions = []      #Solutions list
        for _ in range(employedCount):
            employedBee = initial_solution()       #Generate the initial solution
            employedRisk = risk_calculator(employedBee)    #Calculate the risk of initial solution
            forage =  0                                             #Failed consecutive forage counts
            while True and forage != maxForagingCount:
                onlookerSolution = neighbouring_solution(employedBee)
                onlookerSolutionRisk = risk_calculator(onlookerSolution)
                if onlookerSolutionRisk < employedRisk:
                    employedBee = onlookerSolution                #Employed Bee moves to the onlooker's solution
                    #forage = 0
                else:
                    forage += 1                 
            
            if employedBee not in employedSolutions:
                employedSolutions.append(employedBee)
        
        print("Iteration: ",algIteration)
        printbestSolution(employedSolutions)

init()
