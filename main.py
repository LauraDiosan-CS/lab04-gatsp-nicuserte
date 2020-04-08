from math import sqrt
from GA import GA
import matplotlib.pyplot as plt

def read(filename):
    f = open(filename, "r")
    n = [int(x) for x in f.readline().split()][0]
    mat = []
    for i in range(n):
        line = f.readline().split(',')
        mat.append([int(x) for x in line])
    data = {}
    data['noNodes'] = n
    data['graph'] = mat
    return data

def readTSP(filename):
    f = open(filename, "r")
    n = [int(x) for x in f.readline().split()][0]
    positions={}
    for i in range(n):
        line=f.readline().split(' ')
        positions[int(line[0])-1]=[float(line[1]), float(line[2])]
    f.close()
    data = {}
    data['noNodes'] = n
    data['graph'] = positions
    return data

def dist(a, b):
    return sqrt(abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2)

def fitnessFuncMatrix(cities, problParam):
    mat = problParam['graph']
    dist = float(0)
    for i in range(len(cities)-1):
        dist = dist + mat[cities[i]][cities[i+1]]
    return 1/dist       # if the cost is high, then the fitness is low

def fitnessFunctDistance(cities, problParam):
    cost = float(0)
    positions=problParam['graph']
    for i in range(len(cities) - 1):
        cost = cost + dist(positions[cities[i]], positions[cities[i + 1]])
    return 1 / cost


options={'1':'easy1.txt', '2':'easy2.txt', '3':'easy3.txt', '4':'mediumF.txt', '5':'hardE.txt', '6':'berlin.txt'}
print("Choose input file:")
print("1)easy1.txt")
print("2)easy2.txt")
print("3)easy3.txt")
print("4)mediumF.txt")
print("5)hardE.txt")
print("6)berlin.txt")
c=input()
filename=options[c]
print("Number of generations:")
noGen=int(input())
if int(c)==5 or int(c)==6:
    data = readTSP(filename)
    problParams = {'noNodes': data['noNodes'], 'graph': data['graph'], 'function': fitnessFunctDistance}
else:
    data = read(filename)
    problParams = {'noNodes': data['noNodes'], 'graph': data['graph'], 'function': fitnessFuncMatrix}
gaParams = {'popSize': 100, 'noGenerations': noGen}

ga = GA(gaParams, problParams)
ga.initialisation()
ga.evaluation()

res=[]
for i in range(gaParams['noGenerations']):
    ga.oneGenerationSteadyState()
    best = ga.bestChromosome()
    fitnesses = [c.fitness for c in ga.population]
    avgFitness = sum(fitnesses) / len(fitnesses)
    res.append(avgFitness)
    print('Generation: ' + str(i) + '\nBest chromosome: ' + str(best.repres) + '\nLocal best fitness: ' + str(best.fitness)
         +'\nAverage fitness: '+ str(avgFitness)+'\n')

plt.plot(res)
plt.ylabel('Best Fit/Generation')
plt.xlabel('Generation')
plt.show()
