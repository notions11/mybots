"""
import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import constants as c

amplitude_FrontLeg = c.amplitude_FrontLeg
frequency_FrontLeg = c.frequency_FrontLeg
phaseOffset_FrontLeg = c.phaseOffset_FrontLeg

amplitude_BackLeg = c.amplitude_BackLeg
frequency_BackLeg = c.frequency_BackLeg
phaseOffset_BackLeg = c.phaseOffset_BackLeg

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)
targetAngles_FrontLeg = amplitude_FrontLeg * numpy.sin(frequency_FrontLeg * numpy.linspace(0, numpy.pi*2, 1000) + phaseOffset_FrontLeg)
targetAngles_BackLeg = amplitude_BackLeg * numpy.sin(frequency_BackLeg * numpy.linspace(0, numpy.pi*2, 1000) + phaseOffset_BackLeg)
print(numpy.linspace(0, 999, 1000))

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_BackLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_BackLeg[i],
        maxForce=500)

    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_FrontLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_FrontLeg[i],
        maxForce=500)

    time.sleep(1/240)


p.disconnect()

numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/frontLegTargetAngles", targetAngles_FrontLeg)
numpy.save("data/backLegTargetAngles", targetAngles_BackLeg)
"""
from simulation import SIMULATION

simulation = SIMULATION()
simulation.Run()

