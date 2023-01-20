import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset

        print(self.jointName)
        if self.jointName == b'Torso_FrontLeg':
            self.frequency /= 2
        self.motorValues = self.amplitude * numpy.sin(self.frequency * numpy.linspace(0, numpy.pi*2, 1000) + self.offset)

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=500)

    def Save_Values(self):
        numpy.save("data/" + self.jointName + "MotorValues", self.motorValues)