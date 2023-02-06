## Descending a staircase with holes
The goal of my design-your-own-creature was to replicate the swinging of monkeys from bar to bar. Originally, I had positioned the bars parallel, on the same z-axis:

![enter image description here](https://i.imgur.com/LqGLu73.gif)

But found that the robot had trouble fighting against gravity. To combat this, I made it so the bars slightly descend with every iteration so that the robot still has opprotunities to swing/grab but no longer has to try so hard to fight gravity.

## Robot Design
The design behind my robot was greatly inspired by humans/monkeys. I wanted two arms and two legs but contrary to the quadraped, they are in proper places. There are three components to the arms and legs which consist of 2 longer cubes and one shorter one. This closely represents the upper arm, forearm, wrist and thigh, calf, foot, respectively. Unlike humans/monkeys, however, these joints can turn 180 degrees around their joint axis. I implemented this because it was difficult for to make the robot turn around and conceptualize momentum as a human or monkey would to contort their body adaptively.

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
