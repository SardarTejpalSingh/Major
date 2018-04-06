import random
import re
import time

beeCount = 50
onlookersCount = beeCount//2
employedCount = beeCount//2
scout = 1
iterCount = 30
maxForagingCount = 20
cycles = 2500

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


def bestSolutionSelector(finalSolutions):
    index, i  = 0, 0
    minRisk = 100000000000000000000
    for everySolution in finalSolutions:
        risk = risk_calculator(everySolution)
        if risk < minRisk:
            minRisk = risk
            index = i
        i += 1
    return finalSolutions[index]


def minRisk(solution1, solution2):
    '''Returns solution with minimum risk'''
    

def init():
    '''Algorithm begins here'''
    for algIteration in range(iterCount):     #Algorithm repeater loop
        employedSolutions = risksOfEmployedBee = [] #Solutions list
        start = time.clock()     

        count = 0
        #Employed Bee Phase
        while count < employedCount:
            employedBee = initial_solution()       #Generate the initial solution            
            if employedBee not in employedSolutions:
                employedSolutions.append(employedBee)
                employedRisk = risk_calculator(employedBee)    #Calculate the risk of initial solution
                risksOfEmployedBee.append(employedRisk)
                count += 1
            

        #Onlooker Bee Phase
        globalBest = bestSolutionSelector(employedSolutions)
        globalRisk = risk_calculator(globalBest)

        onlookerBees = 0
        while onlookerBees < onlookersCount:
            trials = 0
            for cycleCount in range(cycles):
                onlookerBee = neighbouring_solution(employedSolutions[onlookerBees])
                onlookerRisk = risk_calculator(onlookerBee)

                #Returns the solution with minimum risk when compared two risks
                if risksOfEmployedBee[onlookerBees] < onlookerRisk:
                    betterSolution = employedSolutions[onlookerBees]
                    trials += 1
                else:
                    betterSolution = onlookerBee    
                    trials = 0
                employedSolutions[onlookerBees] = betterSolution
                risksOfEmployedBee[onlookerBees] = risk_calculator(betterSolution)

                #Returns the solution with minimum risk when compared two risks
                betterSolution = globalBest if globalRisk < onlookerRisk else onlookerBee

                globalBest = betterSolution
                globalRisk = risk_calculator(globalBest)

                #Scout Bee Phase
                if trials == 50:
                    employedSolutions[onlookerBees] = launch_scout_bee(employedSolutions)
                    onlookerBees -= 1
                    break

            onlookerBees += 1
            
        
        print("Iteration: ",algIteration)
        printbestSolution(employedSolutions)
        print("Time taken: ",time.clock() - start)

init()
