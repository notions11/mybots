import random

import numpy

import pyrosim.pyrosim
import pyrosim.pyrosim as pyrosim
import os
import time
import constants
import copy

class SOLUTION:
    def __init__(self, myID):
        self.weights = (numpy.random.rand(constants.numSensorNeurons, constants.numMotorNeurons)*2)-1
        self.myID = myID
        self.created = False
        self.mutations = []

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
        while not os.path.exists("body" + str(self.myID) + ".urdf"):
            time.sleep(0.05)
        self.Create_Brain()
        os.system("start /B python3 simulate.py " + directOrGUI + " " + str(self.myID))

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.05)
        time.sleep(0.05)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("del " + "fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        if self.myID == 0:
            pyrosim.Start_SDF("world.sdf")
            pyrosim.Send_Cube(name="Box", pos=[0, 2, 0.5], size=[1, 1, 1])
            pyrosim.End()

    def Create_Body(self, option=None):
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

        def returnDirection(parent_direction):
            position = []
            if parent_direction == 0:
                position = [-current_block[0] / 2.0, 0, 0]
            elif parent_direction == 1:
                position = [current_block[0] / 2.0, 0, 0]
            elif parent_direction == 2:
                position = [0, -current_block[1] / 2.0, 0]
            elif parent_direction == 3:
                position = [0, current_block[1] / 2.0, 0]
            elif parent_direction == 4:
                position = [0, 0, -current_block[2] / 2.0]
            elif parent_direction == 5:
                position = [0, 0, current_block[2] / 2.0]
            return position

        def getJointPositionForRoot(idx, x , y, z):
            jointPosition = []
            if idx == 0:
                jointPosition = [x / 2, randomValueWithSideLength(y), randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 1:
                jointPosition = [-x / 2, randomValueWithSideLength(y),
                                 randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 2:
                jointPosition = [randomValueWithSideLength(x), y / 2, randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 3:
                jointPosition = [randomValueWithSideLength(x), -y / 2,
                                 randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 4:
                jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y),
                                 (z / 2) + (self.track_z / 2)]
            elif idx == 5:
                jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y),
                                 (-z / 2) + (self.track_z / 2)]
            return jointPosition
        if not self.created:
            self.created = True
            self.numLinks = random.randint(3, 5)
            self.sensors = []
            self.motors = []
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

            self.area_dict = dict()
            self.side_dict = dict()
            self.edge_graph = dict()
            self.parent_dict = dict()
            self.label_dict = dict()

            self.joint_parent_child = dict()
            self.joint_positions = dict()
            self.joint_axis = dict()

            self.link_sensor_check = dict()
            self.link_positions = dict()
            self.link_sizes = dict()

            #generate sizes
            for i in range(self.numLinks):
                rand_x = random.random()
                rand_y = random.random()
                rand_z = random.random()
                area = rand_x*rand_y*rand_z
                self.area_dict[(rand_x, rand_y, rand_z)] = area
                self.side_dict[(rand_x, rand_y, rand_z)] = [None, None, None, None, None, None] #+x -x +y -y +z -z
                self.edge_graph[(rand_x, rand_y, rand_z)] = []
            self.sorted_areas = sorted(self.area_dict, key=self.area_dict.get, reverse=True)
            label = 0
            for s in self.sorted_areas:
                self.label_dict[s] = label
                label += 1

            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    continue
                larger_blocks = self.sorted_areas[:idx]
                while True:
                    choose_block = random.choice(larger_blocks)
                    if len(self.edge_graph[choose_block]) < 6:
                        self.edge_graph[choose_block].append(current_block)
                        break
                    larger_blocks.remove(choose_block)

            # create connections
            self.track_z = (len(self.sorted_areas)*3/2)
            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    self.parent_dict[current_block] = None
                connected_blocks = self.edge_graph[current_block]
                available_indices = [i for i, x in enumerate(self.side_dict[current_block]) if x is None]
                for connected_block in connected_blocks:
                    chosen_side = random.choice(available_indices)
                    self.side_dict[current_block][chosen_side] = connected_block
                    if chosen_side % 2 == 0:
                        self.side_dict[connected_block][chosen_side+1] = []
                        self.parent_dict[connected_block] = chosen_side+1
                    else:
                        self.side_dict[connected_block][chosen_side-1] = []
                        self.parent_dict[connected_block] = chosen_side-1
                    available_indices.remove(chosen_side)


            #draw blocks
            for current_block_idx, current_block in enumerate(self.sorted_areas):
                if current_block in self.parent_dict:
                    parent_direction = self.parent_dict[current_block]
                else:
                    parent_direction = None
                if current_block_idx == 0:
                    sensorCheck = random.random()
                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]

                else:
                    sensorCheck = random.random()
                    position = returnDirection(parent_direction)

                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position

                connected_blocks = self.side_dict[current_block]

                for idx, connected_block in enumerate(connected_blocks):
                    if connected_block == None or connected_block == []:
                        continue
                    jointName = "Link" + str(self.label_dict[current_block]) + "_Link" + str(self.label_dict[connected_block])
                    randomjoint = getJoint()
                    jointPosition = []
                    x = current_block[0]
                    y = current_block[1]
                    z = current_block[2]
                    if self.label_dict[current_block] == 0:
                        jointPosition = getJointPositionForRoot(idx, x, y, z)
                    else:
                        jointPosition = getJointPosition(parent_direction, idx, current_block)

                    pyrosim.Send_Joint(name=jointName, parent="Link" + str(self.label_dict[current_block]),
                                       child="Link" + str(self.label_dict[connected_block]),
                                       type="revolute",
                                       position=jointPosition,
                                       jointAxis=randomjoint)
                    self.motors.append(jointName)
                    self.joint_parent_child[jointName] = {'parent':"Link" + str(self.label_dict[current_block]),
                                                          'child':"Link" + str(self.label_dict[connected_block])}
                    self.joint_positions[jointName] = jointPosition
                    self.joint_axis[jointName] = randomjoint
            pyrosim.End()

    def Create_Mutated_Body(self, option=None):
        def getJoint(ignoreJoint=None):
            jointList = ["0 1 0", "1 0 0", "0 0 1"]
            result = random.choice(jointList)
            while result == ignoreJoint:
                result = random.choice(jointList)
            return result

        def additionalJointCheck():
            return random.random() > 0.5

        def randomValueWithSideLength(size):
            return ((random.random() * 2) - 1) * size / 2

        def getJointPosition(parent, goal, size):
            x = size[0]
            y = size[1]
            z = size[2]
            random_x = randomValueWithSideLength(x)
            random_y = randomValueWithSideLength(y)
            random_z = randomValueWithSideLength(z)
            result = [random_x, random_y, random_z]
            if parent == 0:
                result[0] -= x / 2
            elif parent == 1:
                result[0] += x / 2
            elif parent == 2:
                result[1] -= y / 2
            elif parent == 3:
                result[1] += y / 2
            elif parent == 4:
                result[2] -= z / 2
            elif parent == 5:
                result[2] += z / 2

            if goal == 0:
                result[0] += x / 2 - random_x
            elif goal == 1:
                result[0] += -x / 2 - random_x
            elif goal == 2:
                result[1] += y / 2 - random_y
            elif goal == 3:
                result[1] += -y / 2 - random_y
            elif goal == 4:
                result[2] += z / 2 - random_z
            elif goal == 5:
                result[2] += -z / 2 - random_z

            return result

        def returnDirection(parent_direction, current_block):
            position = []
            if parent_direction == 0:
                position = [-current_block[0] / 2.0, 0, 0]
            elif parent_direction == 1:
                position = [current_block[0] / 2.0, 0, 0]
            elif parent_direction == 2:
                position = [0, -current_block[1] / 2.0, 0]
            elif parent_direction == 3:
                position = [0, current_block[1] / 2.0, 0]
            elif parent_direction == 4:
                position = [0, 0, -current_block[2] / 2.0]
            elif parent_direction == 5:
                position = [0, 0, current_block[2] / 2.0]
            if position == []:
                print(parent_direction)
                print(current_block)
            return position

        def getJointPositionForRoot(idx, x , y, z):
            jointPosition = []
            if idx == 0:
                jointPosition = [x / 2, randomValueWithSideLength(y), randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 1:
                jointPosition = [-x / 2, randomValueWithSideLength(y),
                                 randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 2:
                jointPosition = [randomValueWithSideLength(x), y / 2, randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 3:
                jointPosition = [randomValueWithSideLength(x), -y / 2,
                                 randomValueWithSideLength(z) + (self.track_z / 2)]
            elif idx == 4:
                jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y),
                                 (z / 2) + (self.track_z / 2)]
            elif idx == 5:
                jointPosition = [randomValueWithSideLength(x), randomValueWithSideLength(y),
                                 (-z / 2) + (self.track_z / 2)]
            return jointPosition

        # 0 - change one link to sensor/not sensor
        # 1 - change size
        # 2 - move link
        # 3 - add or remove a link
        # 4 - change random weight
        if option == 0:
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            self.sensors = []

            link_to_change = random.choice(list(self.link_sensor_check))
            self.link_sensor_check[link_to_change] = not self.link_sensor_check[link_to_change]
            for current_block in self.sorted_areas:
                if self.link_sensor_check[self.label_dict[current_block]]:
                    pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                      pos=self.link_positions[self.label_dict[current_block]],
                                      size=self.link_sizes[self.label_dict[current_block]],
                                      material_name="Green",
                                      rgba="0 1.0 0 1.0")
                    self.sensors.append(self.label_dict[current_block])
                else:
                    pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                      pos=self.link_positions[self.label_dict[current_block]],
                                      size=self.link_sizes[self.label_dict[current_block]])
            for current_joint in self.motors:
                pyrosim.Send_Joint(name=current_joint, parent=self.joint_parent_child[current_joint]['parent'],
                                   child=self.joint_parent_child[current_joint]['child'],
                                   type="revolute",
                                   position=self.joint_positions[current_joint],
                                   jointAxis=self.joint_axis[current_joint])
            pyrosim.End()
        elif option == 1:
            self.sensors = []
            self.motors = []
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            self.parent_dict = dict()
            self.label_dict = dict()

            self.joint_parent_child = dict()
            self.joint_positions = dict()
            self.joint_axis = dict()

            self.link_sensor_check = dict()
            self.link_positions = dict()
            self.link_sizes = dict()

            rand_x = random.random()
            rand_y = random.random()
            rand_z = random.random()
            area = rand_x * rand_y * rand_z
            link_to_change = random.choice(self.sorted_areas)
            new_link = (rand_x, rand_y, rand_z)
            self.sorted_areas.remove(link_to_change)
            self.sorted_areas.append(new_link)
            self.area_dict[new_link] = area
            self.area_dict.pop(link_to_change)
            self.side_dict.pop(link_to_change)
            self.edge_graph.pop(link_to_change)

            for current_block in self.sorted_areas:
                self.side_dict[current_block] = [None, None, None, None, None, None]  # +x -x +y -y +z -z
                self.edge_graph[current_block] = []

            self.sorted_areas = sorted(self.area_dict, key=self.area_dict.get, reverse=True)
            label = 0
            for s in self.sorted_areas:
                self.label_dict[s] = label
                label += 1

            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    continue
                larger_blocks = self.sorted_areas[:idx]
                while True:
                    choose_block = random.choice(larger_blocks)
                    if len(self.edge_graph[choose_block]) < 6:
                        self.edge_graph[choose_block].append(current_block)
                        break
                    larger_blocks.remove(choose_block)

            self.track_z = (len(self.sorted_areas) / 2) + 1
            for idx, current_block in enumerate(self.sorted_areas):
                connected_blocks = self.edge_graph[current_block]
                available_indices = [i for i, x in enumerate(self.side_dict[current_block]) if x is None]
                for connected_block in connected_blocks:
                    chosen_side = random.choice(available_indices)
                    self.side_dict[current_block][chosen_side] = connected_block
                    if chosen_side % 2 == 0:
                        self.side_dict[connected_block][chosen_side + 1] = []
                        self.parent_dict[connected_block] = chosen_side + 1
                    else:
                        self.side_dict[connected_block][chosen_side - 1] = []
                        self.parent_dict[connected_block] = chosen_side - 1
                    available_indices.remove(chosen_side)

            for current_block_idx, current_block in enumerate(self.sorted_areas):
                if current_block in self.parent_dict:
                    parent_direction = self.parent_dict[current_block]
                else:
                    parent_direction = None
                if current_block_idx == 0:
                    sensorCheck = random.random()
                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]

                else:
                    sensorCheck = random.random()
                    position = returnDirection(parent_direction, current_block)

                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position

                connected_blocks = self.side_dict[current_block]

                for idx, connected_block in enumerate(connected_blocks):
                    if connected_block == None or connected_block == []:
                        continue
                    jointName = "Link" + str(self.label_dict[current_block]) + "_Link" + str(
                        self.label_dict[connected_block])
                    randomjoint = getJoint()
                    jointPosition = []
                    x = current_block[0]
                    y = current_block[1]
                    z = current_block[2]
                    if self.label_dict[current_block] == 0:
                        jointPosition = getJointPositionForRoot(idx, x, y, z)
                    else:
                        jointPosition = getJointPosition(parent_direction, idx, current_block)

                    pyrosim.Send_Joint(name=jointName, parent="Link" + str(self.label_dict[current_block]),
                                       child="Link" + str(self.label_dict[connected_block]),
                                       type="revolute",
                                       position=jointPosition,
                                       jointAxis=randomjoint)
                    self.motors.append(jointName)
                    self.joint_parent_child[jointName] = {'parent': "Link" + str(self.label_dict[current_block]),
                                                          'child': "Link" + str(self.label_dict[connected_block])}
                    self.joint_positions[jointName] = jointPosition
                    self.joint_axis[jointName] = randomjoint

            pyrosim.End()
        elif option == 2:
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            self.sensors = []
            self.motors = []
            self.sorted_areas = sorted(self.area_dict, key=self.area_dict.get, reverse=True)
            self.side_dict = dict()
            self.edge_graph = dict()
            self.parent_dict = dict()
            for current_block in self.sorted_areas:
                self.side_dict[current_block] = [None, None, None, None, None, None]  # +x -x +y -y +z -z
                self.edge_graph[current_block] = []

            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    continue
                larger_blocks = self.sorted_areas[:idx]
                while True:
                    choose_block = random.choice(larger_blocks)
                    if len(self.edge_graph[choose_block]) < 6:
                        self.edge_graph[choose_block].append(current_block)
                        break
                    larger_blocks.remove(choose_block)

            temp_label_dict = copy.deepcopy(self.label_dict)
            self.label_dict = dict()
            for s in self.sorted_areas:
                self.label_dict[s] = temp_label_dict[s]

            self.track_z = (len(self.sorted_areas) / 2) + 1
            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    self.parent_dict[current_block] = None
                connected_blocks = self.edge_graph[current_block]
                available_indices = [i for i, x in enumerate(self.side_dict[current_block]) if x is None]
                for connected_block in connected_blocks:
                    chosen_side = random.choice(available_indices)
                    self.side_dict[current_block][chosen_side] = connected_block
                    if chosen_side % 2 == 0:
                        self.side_dict[connected_block][chosen_side + 1] = []
                        self.parent_dict[connected_block] = chosen_side + 1
                    else:
                        self.side_dict[connected_block][chosen_side - 1] = []
                        self.parent_dict[connected_block] = chosen_side - 1
                    available_indices.remove(chosen_side)

            self.joint_parent_child = dict()
            self.joint_positions = dict()
            self.joint_axis = dict()
            self.link_positions = dict()
            self.link_sizes = dict()

            for current_block_idx, current_block in enumerate(self.sorted_areas):
                if current_block in self.parent_dict:
                    parent_direction = self.parent_dict[current_block]
                else:
                    parent_direction = None
                if current_block_idx == 0:
                    if self.link_sensor_check[self.label_dict[current_block]]:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]

                else:
                    sensorCheck = random.random()
                    position = returnDirection(parent_direction, current_block)

                    if self.link_sensor_check[self.label_dict[current_block]]:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block))
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position

                connected_blocks = self.side_dict[current_block]

                for idx, connected_block in enumerate(connected_blocks):
                    if connected_block == None or connected_block == []:
                        continue
                    jointName = "Link" + str(self.label_dict[current_block]) + "_Link" + str(
                        self.label_dict[connected_block])
                    randomjoint = getJoint()
                    jointPosition = []
                    x = current_block[0]
                    y = current_block[1]
                    z = current_block[2]
                    if self.label_dict[current_block] == 0:
                        jointPosition = getJointPositionForRoot(idx, x, y, z)
                    else:
                        jointPosition = getJointPosition(parent_direction, idx, current_block)

                    pyrosim.Send_Joint(name=jointName, parent="Link" + str(self.label_dict[current_block]),
                                       child="Link" + str(self.label_dict[connected_block]),
                                       type="revolute",
                                       position=jointPosition,
                                       jointAxis=randomjoint)
                    self.motors.append(jointName)
                    self.joint_parent_child[jointName] = {'parent': "Link" + str(self.label_dict[current_block]),
                                                          'child': "Link" + str(self.label_dict[connected_block])}
                    self.joint_positions[jointName] = jointPosition
                    self.joint_axis[jointName] = randomjoint

            pyrosim.End()
        elif option == 3:
            addorsubtract = random.random()
            if addorsubtract < 0.5 and len(self.sorted_areas) > 2:
                link_to_remove = random.choice(list(self.sorted_areas))
                self.sorted_areas.remove(link_to_remove)
                self.area_dict.pop(link_to_remove)
                self.side_dict.pop(link_to_remove)
                self.edge_graph.pop(link_to_remove)
            else:
                rand_x = random.random()
                rand_y = random.random()
                rand_z = random.random()
                area = rand_x * rand_y * rand_z

                new_link = (rand_x, rand_y, rand_z)
                self.area_dict[new_link] = area
                self.side_dict[new_link] = [None, None, None, None, None, None]  # +x -x +y -y +z -z
                self.edge_graph[new_link] = []

            self.sensors = []
            self.motors = []
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            self.parent_dict = dict()
            self.label_dict = dict()

            self.joint_parent_child = dict()
            self.joint_positions = dict()
            self.joint_axis = dict()

            self.link_sensor_check = dict()
            self.link_positions = dict()
            self.link_sizes = dict()
            for current_block in self.sorted_areas:
                self.side_dict[current_block] = [None, None, None, None, None, None]  # +x -x +y -y +z -z
                self.edge_graph[current_block] = []

            self.sorted_areas = sorted(self.area_dict, key=self.area_dict.get, reverse=True)
            label = 0
            for s in self.sorted_areas:
                self.label_dict[s] = label
                label += 1

            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    continue
                larger_blocks = self.sorted_areas[:idx]
                while True:
                    choose_block = random.choice(larger_blocks)
                    if len(self.edge_graph[choose_block]) < 6:
                        self.edge_graph[choose_block].append(current_block)
                        break
                    larger_blocks.remove(choose_block)

            # create connections
            self.track_z = (len(self.sorted_areas) / 2) + 1
            for idx, current_block in enumerate(self.sorted_areas):
                if idx == 0:
                    self.parent_dict[current_block] = None
                connected_blocks = self.edge_graph[current_block]
                available_indices = [i for i, x in enumerate(self.side_dict[current_block]) if x is None]
                for connected_block in connected_blocks:
                    chosen_side = random.choice(available_indices)
                    self.side_dict[current_block][chosen_side] = connected_block
                    if chosen_side % 2 == 0:
                        self.side_dict[connected_block][chosen_side + 1] = []
                        self.parent_dict[connected_block] = chosen_side + 1
                    else:
                        self.side_dict[connected_block][chosen_side - 1] = []
                        self.parent_dict[connected_block] = chosen_side - 1
                    available_indices.remove(chosen_side)

            # draw blocks
            for current_block_idx, current_block in enumerate(self.sorted_areas):
                if current_block in self.parent_dict:
                    parent_direction = self.parent_dict[current_block]
                else:
                    parent_direction = None
                if current_block_idx == 0:
                    sensorCheck = random.random()
                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                          pos=[0, 0, self.track_z / 2.0],
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = [0, 0, self.track_z / 2.0]

                else:
                    sensorCheck = random.random()
                    position = returnDirection(parent_direction, current_block)

                    if sensorCheck > 0.5:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block),
                                          material_name="Green",
                                          rgba="0 1.0 0 1.0")
                        self.sensors.append(self.label_dict[current_block])
                        self.link_sensor_check[self.label_dict[current_block]] = True
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position
                    else:
                        pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]), pos=position,
                                          size=list(current_block))
                        self.link_sensor_check[self.label_dict[current_block]] = False
                        self.link_sizes[self.label_dict[current_block]] = list(current_block)
                        self.link_positions[self.label_dict[current_block]] = position

                connected_blocks = self.side_dict[current_block]

                for idx, connected_block in enumerate(connected_blocks):
                    if connected_block == None or connected_block == []:
                        continue
                    jointName = "Link" + str(self.label_dict[current_block]) + "_Link" + str(
                        self.label_dict[connected_block])
                    randomjoint = getJoint()
                    jointPosition = []
                    x = current_block[0]
                    y = current_block[1]
                    z = current_block[2]
                    if self.label_dict[current_block] == 0:
                        jointPosition = getJointPositionForRoot(idx, x, y, z)
                    else:
                        jointPosition = getJointPosition(parent_direction, idx, current_block)

                    pyrosim.Send_Joint(name=jointName, parent="Link" + str(self.label_dict[current_block]),
                                       child="Link" + str(self.label_dict[connected_block]),
                                       type="revolute",
                                       position=jointPosition,
                                       jointAxis=randomjoint)
                    self.motors.append(jointName)
                    self.joint_parent_child[jointName] = {'parent': "Link" + str(self.label_dict[current_block]),
                                                          'child': "Link" + str(self.label_dict[connected_block])}
                    self.joint_positions[jointName] = jointPosition
                    self.joint_axis[jointName] = randomjoint

            pyrosim.End()
        elif option == 4:
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            for current_block in self.sorted_areas:
                if self.link_sensor_check[self.label_dict[current_block]]:
                    pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                      pos=self.link_positions[self.label_dict[current_block]],
                                      size=self.link_sizes[self.label_dict[current_block]],
                                      material_name="Green",
                                      rgba="0 1.0 0 1.0")
                    self.sensors.append(self.label_dict[current_block])
                else:
                    pyrosim.Send_Cube(name="Link" + str(self.label_dict[current_block]),
                                      pos=self.link_positions[self.label_dict[current_block]],
                                      size=self.link_sizes[self.label_dict[current_block]])
            for current_joint in self.motors:
                pyrosim.Send_Joint(name=current_joint, parent=self.joint_parent_child[current_joint]['parent'],
                                   child=self.joint_parent_child[current_joint]['child'],
                                   type="revolute",
                                   position=self.joint_positions[current_joint],
                                   jointAxis=self.joint_axis[current_joint])
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
            self.numMotors += 1
            ctr+=1

        self.weights = (numpy.random.rand(self.numSensors, self.numMotors) * 2) - 1

        for currentRow in range(self.numSensors):
            for currentColumn in range(self.numMotors):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+self.numSensors, weight=self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        #possible changes
        # 0 - change one link to sensor/not sensor
        # 1 - change size also changes the link
        # 2 - move links
        # 3 - add or remove a link
        # 4 - change random weight

        evolve_option = random.randint(0, 4)
        self.mutations.append(evolve_option)
        if evolve_option == 0:
            os.system("del body" + str(self.myID)+ ".urdf")
            self.Create_Mutated_Body(0)
            os.system("del brain" + str(self.myID)+ ".nndf")
            self.Create_Brain()
        elif evolve_option == 1:
            os.system("del body" + str(self.myID) + ".urdf")
            self.Create_Mutated_Body(1)
            os.system("del brain" + str(self.myID) + ".nndf")
            self.Create_Brain()
        elif evolve_option == 2:
            os.system("del body" + str(self.myID) + ".urdf")
            self.Create_Mutated_Body(2)
            os.system("del brain" + str(self.myID) + ".nndf")
            self.Create_Brain()
        elif evolve_option == 3:
            os.system("del body" + str(self.myID) + ".urdf")
            self.Create_Mutated_Body(3)
            os.system("del brain" + str(self.myID) + ".nndf")
            self.Create_Brain()
        else:
            os.system("del body" + str(self.myID) + ".urdf")
            self.Create_Mutated_Body(4)
            os.system("del brain" + str(self.myID) + ".nndf")
            self.Create_Brain()
            if self.numSensors == 0:
                return
            randomRow = random.randint(0, self.numSensors-1)
            randomColumn = random.randint(0, self.numMotors-1)
            self.weights[randomRow][randomColumn] = random.random()*2 - 1

    def Set_ID(self, newID):
        self.myID = newID

    def Get_ID(self):
        return self.myID