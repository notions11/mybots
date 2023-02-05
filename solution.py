import random

import numpy
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
            #pyrosim.Send_Sphere(name="BowlingBall", pos=[-3, +3, 0.5], size=[0.5])
            #pyrosim.Send_Cube(name="Wall_1", pos=[-100, 2, 1], size=[200, 0.1, 0.1], mass=0.0)
            #pyrosim.Send_Cube(name="Wall_2", pos=[-100, -2, 1], size=[200, 0.1, 0.1], mass=0.0)
            #pyrosim.Send_Cube(name="Bar", pos=[-.25, 0, 51], size=[0.1, 10, 99], mass=0.0)
            #pyrosim.Send_Cube(name="Bar2", pos=[-2, 0, -.5], size=[0.1, 4, 0.1], mass=0.0)
            for i in range(0, 15, 1):
                pyrosim.Send_Cube(name="Bar", pos=[-(i*.5)-.25, 0, 1-(i*0.25)], size=[0.1, 10, 0.01], mass=0.0)
            pyrosim.End()

    def Create_Body(self):
        if self.myID == 0:
            pyrosim.Start_URDF("body.urdf")
            pyrosim.Send_Cube(name="Torso", pos=[0, 0, 0.25], size=[0.5, 1, 1])

            #Arms
            pyrosim.Send_Joint(name="Torso_RightArm", parent="Torso", child="RightArm", type="revolute",
                               position=[0, 0.5, 0.5], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightArm", pos=[0, 0, .5], size=[.1, .1, 1])

            pyrosim.Send_Joint(name="Torso_LeftArm", parent="Torso", child="LeftArm", type="revolute",
                               position=[0, -0.5, 0.5], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftArm", pos=[0, 0, .5], size=[.1, .1, 1])

            #Upper Arm
            pyrosim.Send_Joint(name="RightArm_RightUpperArm", parent="RightArm", child="RightUpperArm", type="revolute",
                               position=[0, 0, 1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightUpperArm", pos=[0, 0, 0.5], size=[.1, .1, 1])

            pyrosim.Send_Joint(name="LeftArm_LeftUpperArm", parent="LeftArm", child="LeftUpperArm", type="revolute",
                               position=[0, 0, 1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftUpperArm", pos=[0, 0, 0.5], size=[.1, .1, 1])


            #Wrists
            pyrosim.Send_Joint(name="RightUpperArm_RightWrist", parent="RightUpperArm", child="RightWrist", type="revolute",
                               position=[0, 0, 1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightWrist", pos=[0, 0, .25], size=[.1, .1, .5])

            pyrosim.Send_Joint(name="LeftUpperArm_LeftWrist", parent="LeftUpperArm", child="LeftWrist", type="revolute",
                               position=[0, 0, 1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftWrist", pos=[0, 0, .25], size=[.1, .1, .5])

            # Legs
            pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute",
                               position=[0, 0.5, 0], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightLeg", pos=[0, 0, -.5], size=[.1, .1, 1])

            pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute",
                               position=[0, -0.5, 0], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftLeg", pos=[0, 0, -.5], size=[.1, .1, 1])

            # Lower Leg
            pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute",
                               position=[0, 0, -1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[.1, .1, 1])

            pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute",
                               position=[0, 0, -1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[.1, .1, 1])

            # Ankle
            pyrosim.Send_Joint(name="RightLowerLeg_RightAnkle", parent="RightLowerLeg", child="RightAnkle",
                               type="revolute",
                               position=[0, 0, -1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="RightAnkle", pos=[0, 0, -.25], size=[.1, .1, .5])

            pyrosim.Send_Joint(name="LeftLowerLeg_LeftAnkle", parent="LeftLowerLeg", child="LeftAnkle", type="revolute",
                               position=[0, 0, -1], jointAxis="0 1 0")
            pyrosim.Send_Cube(name="LeftAnkle", pos=[0, 0, -.25], size=[.1, .1, .5])

            pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LeftArm")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="RightArm")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftUpperArm")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightUpperArm")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="LeftWrist")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="RightWrist")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=9, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=10, linkName="RightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=11, linkName="LeftAnkle")
        pyrosim.Send_Sensor_Neuron(name=12, linkName="RightAnkle")

        pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_LeftArm")
        pyrosim.Send_Motor_Neuron(name=14, jointName="Torso_RightArm")
        pyrosim.Send_Motor_Neuron(name=15, jointName="LeftArm_LeftUpperArm")
        pyrosim.Send_Motor_Neuron(name=16, jointName="RightArm_RightUpperArm")
        pyrosim.Send_Motor_Neuron(name=17, jointName="LeftUpperArm_LeftWrist")
        pyrosim.Send_Motor_Neuron(name=18, jointName="RightUpperArm_RightWrist")
        pyrosim.Send_Motor_Neuron(name=19, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=20, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=21, jointName="RightLeg_RightLowerLeg")
        pyrosim.Send_Motor_Neuron(name=22, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=23, jointName="RightLowerLeg_RightAnkle")
        pyrosim.Send_Motor_Neuron(name=24, jointName="LeftLowerLeg_LeftAnkle")

        for currentRow in range(constants.numSensorNeurons):
            for currentColumn in range(constants.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+constants.numSensorNeurons, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, constants.numSensorNeurons-1)
        randomColumn = random.randint(0, constants.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random()*2 - 1

    def Set_ID(self, newID):
        self.myID = newID
