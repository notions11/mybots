from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

class SIMULATION:
    def __init__(self, directOrGUI, simulationID):
        self.directOrGUI = directOrGUI
        if directOrGUI == 'DIRECT':
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT(simulationID)
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()


    def Run(self):
        for i in range(1000):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == 'GUI':
                time.sleep(1 / 1000)

    def Get_Fitness(self):
        self.robot.Get_Fitness()

    def __del__(self):
        p.disconnect()

