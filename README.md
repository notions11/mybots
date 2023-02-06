## Descending a staircase with holes
The goal of my design-your-own-creature was to replicate the swinging of monkeys from bar to bar. Originally, after removing the floor, I had positioned the bars parallel, on the same z-axis:

![enter image description here](https://i.imgur.com/LqGLu73.gif)

But found that the robot had trouble fighting against gravity. To combat this, I made it so the bars slightly descend with every iteration so that the robot still has opportunities to swing/grab but no longer has to try so hard to fight gravity. Check out my final video here in addition to the evolution process: https://youtu.be/6TepzPRrK-8

## Robot Design
Humans/monkeys greatly inspired the design behind my robot. I wanted two arms and two legs but contrary to the quadruped, they are in the proper places. There are three components to the arms and legs which consist of 2 longer cubes and one shorter one. This closely represents the upper arm, forearm, wrist and thigh, calf, and foot, respectively. Unlike humans/monkeys, however, these joints can turn 180 degrees around their joint axis. I implemented this because it was difficult to make the robot turn around and conceptualize momentum as a human or monkey would contort their body adaptively.

## Fitness function
The fitness function of my robot was actually hard to come up with. I wanted to create a function that didn't necessarily punish the robot for falling off the bars, so long as it made some progress descending the staircase. I found that if the robot were to fall off right away or toward the beginning of the simulation, it would have a z-value close to -40. With this in mind, I played around with values and settled on -20 because it was a value which showed that the robot latched on and at least made an attempt to reach for the next step. This value made sure that any robot that fell below a -20 z-axis threshold would be marked as falling too early and thus not have a strong fitness score -- this was done by taking the absolute value of the z-position. After the vertical threshold was established, it was a simple metric of how far the robot progressed toward the negative x-axis. 

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
