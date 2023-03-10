from solution import SOLUTION
import constants
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del body*.urdf")
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.fitnessPlot = open("fitnessPlot.txt", "w")
        self.iteration = 0
        self.parents = dict()
        self.nextAvailableID = 0
        for i in range(0, constants.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(constants.numberOfGenerations):
            self.Evolve_For_One_Generation()
            print(currentGeneration)
        self.fitnessPlot.close()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        self.WriteBest()
        self.iteration += 1
        """
        self.Mutate()
        self.child.Evaluate('DIRECT')
        self.Print()
        self.Select()
        """

    def Spawn(self):
        self.children = dict()
        for parent in self.parents.keys():
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.keys():
            self.children[child].Mutate()

    def Select(self):
        for parent in self.parents.keys():
            if self.parents[parent].fitness > self.children[parent].fitness:
                self.parents[parent] = self.children[parent]

    def Print(self):
        print()
        for parent in self.parents.keys():
            print(self.parents[parent].fitness, self.children[parent].fitness)
        print()

    def Show_Best(self):
        fittest_parent = None
        fittest_score = None
        fittest_number = 0
        for parent in self.parents.keys():
            if fittest_parent is None:
                fittest_parent = self.parents[parent]
                fittest_score = self.parents[parent].fitness
            if self.parents[parent].fitness < fittest_score:
                fittest_parent = self.parents[parent]
                fittest_score = self.parents[parent].fitness
                fittest_number = self.parents[parent].Get_ID()

        print(fittest_parent.weights)
        print(fittest_score)
        print(fittest_number)
        fittest_parent.Start_Simulation('GUI')

    def WriteBest(self):
        fittest_parent = None
        fittest_score = None
        fittest_number = 0
        for parent in self.parents.keys():
            if fittest_parent is None:
                fittest_parent = self.parents[parent]
                fittest_score = self.parents[parent].fitness
            if self.parents[parent].fitness < fittest_score:
                fittest_parent = self.parents[parent]
                fittest_score = self.parents[parent].fitness
                fittest_number = self.parents[parent].Get_ID()

        self.fitnessPlot.write(str(self.iteration) + ", " + str(fittest_score) + "\n")

    def Evaluate(self, solutions):
        for parent in solutions:
            solutions[parent].Start_Simulation('DIRECT')

        for parent in solutions:
            solutions[parent].Wait_For_Simulation_To_End()