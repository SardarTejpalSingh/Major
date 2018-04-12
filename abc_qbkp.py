import random
import re
import time

beeCount = 50
onlookersCount = beeCount//2
employedCount = beeCount//2
scout = 1
iterCount = 10
cycles = 300
limit = 299

dataset = open("data.txt", "r")

n = int(dataset.readline().strip())
weights = list(map(int, dataset.readline().strip().split()))
capacity = int(dataset.readline().strip())
risk_ar = []
for i in range(n-1):   
    temp_list = [0]*(i+1)
    temp_list += map(int, dataset.readline().strip().split())
    risk_ar.append(temp_list)


def risk_calculator(solution):
    '''Returns the risk value of the solution'''
    risk_value = -1
    for i in range(len(solution)-2):
        for j in range(i+1, len(solution)-1):
            if solution[i]==99:
                break
            risk_value = max(risk_value, risk_ar[solution[i]][solution[j]])
    
    return risk_value

def extract_max(solution):
    '''Returns the max risk value of the solution'''
    risk_value = -1
    for i in range(n-1):
        for j in range(n-1):
            if i in solution and j in solution:
                risk_value = max(risk_value, risk_ar[i][j])
    
    return risk_value

def initial_solution():
    '''Returns a list containing indices of initial solution'''
    randList = random.sample(range(0, len(weights)-1), len(weights)-1)
    i, total = 0, 0
    solution = []
    total += weights[randList[0]]
    solution.append(randList[0])
    flag = 0
    while total < capacity and i < len(randList)-1:
        i += 1
        i1, i2 = 0, 0
        for j in solution:
            flag = 0
            if j > randList[i]:
                i1 = randList[i]
                i2 = j-1
            else:
                i1 = j
                i2 = randList[i]-1
            if risk_ar[i1][i2] == 0:
                flag = 1
        if flag == 1:
            continue
        else:
            total += weights[randList[i]]
            solution.append(randList[i])
    return sorted(solution)


def neighbouring_solution(solution):
    '''Returns a list containing indices of a neighbouring solution by updating 3 elements randomly'''
    #Generate 3 random indices within the solution list
    removeList = random.sample(range(0, len(solution)), 3)
    #Remove the elements at that specific indices
    for indexToRemove in removeList:
        solution.pop(indexToRemove%len(solution))
    newEleList = random.sample(range(0,len(weights)-1), len(weights)-1)
    total = 0

    for i in solution:
        total += weights[i]
    i = 0
    while total < capacity and i < len(newEleList):
        if newEleList[i] not in solution:
            solution.append(newEleList[i])
            total += weights[newEleList[i]]
        i+=1

    
    return sorted(solution)


def launch_scout_bee(employedSolutions):
    '''Returns a new unique solution'''
    while True:
        newSolution = initial_solution()
        if newSolution not in employedSolutions:
            return newSolution


def print_best_solution(finalSolutions):
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


def best_solution_selector(finalSolutions):
    index, i  = 0, 0
    minRisk = 100000000000000000000
    for everySolution in finalSolutions:
        risk = risk_calculator(everySolution)
        if risk < minRisk:
            minRisk = risk
            index = i
        i += 1
    return finalSolutions[index]
    

def pick_a_solution(employedSolutions, risksOfEmployedBee):
    '''Returns the index of single solution selected by binary tournament method'''
    twoRandomIndices = random.sample(range(0, len(employedSolutions)-1), 2)
    risk1 = risksOfEmployedBee[twoRandomIndices[0]]
    risk2 = risksOfEmployedBee[twoRandomIndices[1]]
    probability = (random.randrange(0,100,1))/100
    if probability < 0.6:
        return (twoRandomIndices[0] if risk1 < risk2 else twoRandomIndices[1])
    else:
        return (twoRandomIndices[0] if risk1 > risk2 else twoRandomIndices[1])


def init():
    '''Algorithm begins here'''
    #Algorithm repeater loop
    for algIteration in range(iterCount):    
        #Solutions list 
        employedSolutions = []
        risksOfEmployedBee = [] 
        start = time.clock()     

        count = 0
        #Initial solution genration
        while count < employedCount:
            #Generate the initial solution  
            employedBee = initial_solution()                 
            if employedBee not in employedSolutions:
                employedSolutions.append(employedBee)
                 #Calculate the risk of initial solution
                employedRisk = risk_calculator(employedBee)   
                risksOfEmployedBee.append(employedRisk)
                count += 1
            
        print("Employed Bee Phase")
        """
        Employed Bee Phase
        """
        globalBest = best_solution_selector(employedSolutions)
        globalRisk = risk_calculator(globalBest)

        onlookerBees = 0
        while onlookerBees < onlookersCount:
            trials = 0
            for cycleCount in range(cycles):
                #print(cycleCount, end=" ")
                onlookerBee = neighbouring_solution(employedSolutions[onlookerBees])
                onlookerRisk = risk_calculator(onlookerBee)

                #Returns the solution with minimum risk when compared two risks
                if risksOfEmployedBee[onlookerBees] < onlookerRisk:
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

            onlookerBees += 1

        print("Onlooker Bee phase")
        """
        Onlooker Bee phase
        """
        onlookerBees = 0
        while onlookerBees < onlookersCount:

            #Binary Tournament method
            pickedSolutionIndex = pick_a_solution(employedSolutions, risksOfEmployedBee)
            trials, cycleCount = 0, 0
            while cycleCount < cycles:

                cycleCount += 1

                onlookerBee = neighbouring_solution(employedSolutions[pickedSolutionIndex])
                onlookerRisk = risk_calculator(onlookerBee)

                #Returns the solution with minimum risk when compared two risks
                if risksOfEmployedBee[pickedSolutionIndex] < onlookerRisk:
                    trials += 1
                else:
                    betterSolution = onlookerBee    
                    trials = 0
                    employedSolutions[pickedSolutionIndex] = betterSolution
                    risksOfEmployedBee[pickedSolutionIndex] = risk_calculator(betterSolution)

                globalBest, globalRisk = (globalBest,globalRisk) if globalRisk < onlookerRisk else (onlookerBee,onlookerRisk)              
                
                # Food source exhausted. Launch scout bee!
                if trials == limit:
                    '''Scout bee phase'''
                    print("Scout Bee Delpoyed")
                    print(onlookerRisk)
                    employedSolutions[pickedSolutionIndex] = launch_scout_bee(employedSolutions)
                    cycleCount = 0
                    trials = 0

            onlookerBees += 1

        bottleNeck = risk_calculator(globalBest)
        print("Iteration: ",algIteration)
        print(globalBest, globalRisk, bottleNeck)
        print("Time taken: ",time.clock() - start)
        print(risksOfEmployedBee)

print(risk_ar)
init()