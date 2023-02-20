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
        print("in evaluate")
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
        print("in start_simulation")
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
        def getJoint(ignoreJoint=None):
            jointList = ["0 1 0", "1 0 0", "0 0 1"]
            result = random.choice(jointList)
            while result == ignoreJoint:
                result = random.choice(jointList)
            return result

        def additionalJointCheck():
            return random.random() > 0.5

        def randomValueWithSideLength(size):
            return ((random.random()*2)-1) * size/2

        def getJointPosition(parent, goal, size):
            x = size[0]
            y = size[1]
            z = size[2]
            random_x = randomValueWithSideLength(x)
            random_y = randomValueWithSideLength(y)
            random_z = randomValueWithSideLength(z)
            result = [random_x, random_y, random_z]
            if parent == 0:
                result[0] -= x/2
            elif parent == 1:
                result[0] += x/2
            elif parent == 2:
                result[1] -= y/2
            elif parent == 3:
                result[1] += y/2
            elif parent == 4:
                result[2] -= z/2
            elif parent == 5:
                result[2] += z/2

            if goal == 0:
                result[0] += x/2 - random_x
            elif goal == 1:
                result[0] += -x/2 - random_x
            elif goal == 2:
                result[1] += y/2 - random_y
            elif goal == 3:
                result[1] += -y/2 - random_y
            elif goal == 4:
                result[2] += z/2 - random_z
            elif goal == 5:
                result[2] += -z/2 - random_z

            return result



        if self.myID == 0:
            self.numLinks = random.randint(5, 5)
            self.sensors = []
            self.motors = []
            pyrosim.Start_URDF("body.urdf")

            area_dict = dict()
            side_dict = dict()
            edge_graph = dict()
            parent_dict = dict()
            label_dict = dict()

            #generate sizes
            for i in range(self.numLinks):
                rand_x = random.random()
                rand_y = random.random()
                rand_z = random.random()
                area = rand_x*rand_y*rand_z
                area_dict[(rand_x, rand_y, rand_z)] = area
                side_dict[(rand_x, rand_y, rand_z)] = [None, None, None, None, None, None] #+x -x +y -y +z -z
                edge_graph[(rand_x, rand_y, rand_z)] = []
            sorted_areas = sorted(area_dict, key=area_dict.get, reverse=True)
            label = 0
            for s in sorted_areas:
                label_dict[s] = label
                label += 1

            for idx, current_block in enumerate(sorted_areas):
                if idx == 0:
                    continue
                larger_blocks = sorted_areas[:idx]
                while True:
                    choose_block = random.choice(larger_blocks)
                    if len(edge_graph[choose_block]) < 6:
                        edge_graph[choose_block].append(current_block)
                        break
                    larger_blocks.remove(choose_block)

            # create connections
            track_z = sorted_areas[0][2] + 0.5
            for idx, current_block in enumerate(sorted_areas):
                connected_blocks = edge_graph[current_block]
                available_indices = [i for i, x in enumerate(side_dict[current_block]) if x is None]
                for connected_block in connected_blocks:
                    chosen_side = random.choice(available_indices)
                    side_dict[current_block][chosen_side] = connected_block
                    if chosen_side % 2 == 0:
                        side_dict[connected_block][chosen_side+1] = []
                        parent_dict[connected_block] = chosen_side+1
                    else:
                        side_dict[connected_block][chosen_side-1] = []
                        parent_dict[connected_block] = chosen_side-1
                    available_indices.remove(chosen_side)
                    if chosen_side >= 4:
                        track_z += connected_block[2]


            #draw blocks
            for current_block in sorted_areas:
                if current_block in parent_dict:
                    parent_direction = parent_dict[current_block]
                else:
                    parent_direction = None
                if label_dict[current_block] == 0:
                    sensorCheck = random.random()
                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(label_dict[current_block]), pos=[0, 0, track_z / 2.0],
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(label_dict[current_block])
                    else:
                        pyrosim.Send_Cube(name="Link" + str(label_dict[current_block]), pos=[0, 0, track_z / 2.0],
                                          size=list(current_block))

                    print("parent direction: ", parent_direction)
                    print("position first block: ", [0, 0, track_z / 2.0])
                else:
                    sensorCheck = random.random()
                    position = []
                    if parent_direction == 0:
                        position = [-current_block[0]/2.0, 0, 0]
                    elif parent_direction == 1:
                        position = [current_block[0]/2.0, 0, 0]
                    elif parent_direction == 2:
                        position = [0, -current_block[1]/2.0, 0]
                    elif parent_direction == 3:
                        position = [0, current_block[1]/2.0, 0]
                    elif parent_direction == 4:
                        position = [0, 0, -current_block[2]/2.0]
                    elif parent_direction == 5:
                        position = [0, 0, current_block[2]/2.0]

                    print("parent direction: ", parent_direction)
                    print("position second block: ", position)


                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(label_dict[current_block]), pos=position,
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(label_dict[current_block])
                    else:
                        pyrosim.Send_Cube(name="Link" + str(label_dict[current_block]), pos=position,
                                          size=list(current_block))

                connected_blocks = side_dict[current_block]

                for idx, connected_block in enumerate(connected_blocks):
                    if connected_block == None or connected_block == []:
                        continue
                    jointName = "Link" + str(label_dict[current_block]) + "_Link" + str(label_dict[connected_block])
                    randomjoint = getJoint()
                    jointPosition = []
                    x = current_block[0]
                    y = current_block[1]
                    z = current_block[2]
                    if label_dict[current_block] == 0:
                        if idx == 0:
                            jointPosition = [x/2, randomValueWithSideLength(y), randomValueWithSideLength(z)+(track_z/2)]
                        elif idx == 1:
                            jointPosition = [-x/2, randomValueWithSideLength(y), randomValueWithSideLength(z)+(track_z/2)]
                        elif idx == 2:
                            jointPosition = [randomValueWithSideLength(x), y/2, randomValueWithSideLength(z)+(track_z/2)]
                        elif idx == 3:
                            jointPosition = [randomValueWithSideLength(x), -y/2, randomValueWithSideLength(z)+(track_z/2)]
                        elif idx == 4:
                            jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y), (z/2)+(track_z/2)]
                        elif idx == 5:
                            jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y), (-z/2)+(track_z/2)]
                    else:
                        jointPosition = getJointPosition(parent_direction, idx, current_block)
                    print("index: ", idx)
                    print("joint position: ", jointPosition)

                    pyrosim.Send_Joint(name=jointName, parent="Link" + str(label_dict[current_block]),
                                       child="Link" + str(label_dict[connected_block]),
                                       type="revolute",
                                       position=jointPosition,
                                       jointAxis=randomjoint)
                    self.motors.append(jointName)
                    if False:
                        pyrosim.Send_Joint(name=jointName+"Ball", parent="Link" + str(label_dict[current_block]),
                                           child="Link" + str(label_dict[connected_block]),
                                           type="revolute",
                                           position=jointPosition,
                                           jointAxis=getJoint(randomjoint))
                        self.motors.append(jointName+"Ball")
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

        for i in self.motors:
            pyrosim.Send_Motor_Neuron(name=ctr, jointName=i)
            print(i)
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
