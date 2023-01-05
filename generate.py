import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

#pyrosim.Send_Cube(name="Box", pos=[0,0,0.5], size=[1,1,1])
#pyrosim.Send_Cube(name="Box", pos=[1,0,1.5], size=[1,1,1])

for i in range(-2, 3):
    for j in range(-2, 3):
        for k in range(10):
            pyrosim.Send_Cube(name="Box", pos=[i, j, 0.5+(k)], size=[1*(.9**k), 1*(.9**k), 1*(.9**k)])

pyrosim.End()
