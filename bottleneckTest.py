dataset = open("data.txt", "r")

n = int(dataset.readline().strip())
weights = list(map(int, dataset.readline().strip().split()))
capacity = int(dataset.readline().strip())
risk_ar = []
for i in range(n-1):   
    temp_list = map(int, dataset.readline().strip().split())
    risk_ar += temp_list


risk_ar.sort()
risk_ar = set(risk_ar)
risk_ar = list(risk_ar)
print(risk_ar[198])