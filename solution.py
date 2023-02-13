import random

import numpy

import pyrosim.pyrosim
import pyrosim.pyrosim as pyrosim
import os
import time
import constants

class SOLUTION:
    def __init__(self, myID):
        self.weights = (numpy.random.rand(constants.numSensorNeurons, constants.numMotorNeurons)*2)-1
        self.myID = myID

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python3 simulate.py " + directOrGUI + " " + str(self.myID))
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.05)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        # self.Start_Simulation(directOrGUI)
        # self.Wait_For_Simulation_To_End()

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python3 simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.02)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("del " + "fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        if self.myID == 0:
            pyrosim.Start_SDF("world.sdf")
            pyrosim.Send_Cube(name="Box", pos=[0, 2, 0.5], size=[1, 1, 1])
            pyrosim.End()

    def Create_Body(self):
        if self.myID == 0:
            self.numLinks = random.randint(5, 10)
            self.sensors = []
            pyrosim.Start_URDF("body.urdf")
            jointList = ["0 1 0", "1 0 0", "0 0 1"]

            max_z = 0.0
            ctr = 0
            linkList = []

            for i in range(self.numLinks):
                rand_x = random.random()
                rand_y = random.random()
                rand_z = random.random()
                if rand_z > max_z:
                    max_z = rand_z
                linkList.append([rand_x, rand_y, rand_z])

            sensorCheck = random.random()
            if sensorCheck > 0.5:
                pyrosim.Send_Cube(name="Link"+str(ctr), pos=[0, 0, max_z/2.0], size=linkList[ctr], material_name="Green",
                                  rgba="0 1.0 0 1.0")
                self.sensors.append(ctr)
            else:
                pyrosim.Send_Cube(name="Link"+str(ctr), pos=[0, 0, max_z / 2.0], size=linkList[ctr])
            jointName = "Link" + str(ctr) + "_Link" + str(ctr+1)
            pyrosim.Send_Joint(name=jointName, parent="Link"+str(ctr), child="Link"+str(ctr+1), type="revolute",
                               position=[linkList[ctr][0]/2.0, 0, max_z/2.0], jointAxis=random.choice(jointList))
            ctr += 1
            while ctr < self.numLinks - 1:
                sensorCheck = random.random()
                if sensorCheck > 0.5:
                    pyrosim.Send_Cube(name="Link"+str(ctr), pos=[linkList[ctr][0]/2.0, 0, 0], size=linkList[ctr], material_name="Green",
                                      rgba="0 1.0 0 1.0")
                    self.sensors.append(ctr)
                else:
                    pyrosim.Send_Cube(name="Link"+str(ctr), pos=[linkList[ctr][0]/2.0, 0, 0], size=linkList[ctr])
                jointName = "Link"+str(ctr) + "_Link" + str(ctr + 1)
                pyrosim.Send_Joint(name=jointName, parent="Link"+str(ctr), child="Link"+str(ctr + 1), type="revolute",
                                   position=[linkList[ctr][0], 0, 0], jointAxis=random.choice(jointList))
                ctr += 1

            sensorCheck = random.random()
            if sensorCheck > 0.5:
                pyrosim.Send_Cube(name="Link"+str(ctr), pos=[linkList[ctr][0]/2.0, 0, 0], size=linkList[ctr], material_name="Green",
                                  rgba="0 1.0 0 1.0")
                self.sensors.append(ctr)
            else:
                pyrosim.Send_Cube(name="Link"+str(ctr), pos=[linkList[ctr][0] / 2.0, 0, 0], size=linkList[ctr])

            pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        ctr = 0
        self.numMotors = 0
        self.numSensors = 0
        for i in self.sensors:
            pyrosim.Send_Sensor_Neuron(name=ctr, linkName="Link"+str(i))
            ctr += 1
            self.numSensors += 1

        for i in range(self.numLinks-1):
            pyrosim.Send_Motor_Neuron(name=ctr, jointName="Link"+str(i)+"_Link"+str(i+1))
            self.numMotors += 1
            ctr+=1

        self.weights = (numpy.random.rand(self.numSensors, self.numMotors) * 2) - 1

        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numMotors):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+self.numSensors, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, self.numSensors-1)
        randomColumn = random.randint(0, self.numMotors-1)
        self.weights[randomRow][randomColumn] = random.random()*2 - 1

    def Set_ID(self, newID):
        self.myID = newID
