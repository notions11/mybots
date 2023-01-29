import sys
from simulation import SIMULATION

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(directOrGUI, int(solutionID))
simulation.Run()
simulation.Get_Fitness()

