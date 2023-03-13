# Final Project (Mix between science and engineer methodologies)
## Background/Hypothesis
In this final project, I wanted to iterate off of Assignment 8 and find out whether we can get better evolution by investigating which types of evolution were most effective. As a refresher the following is how I set up my code and evolutions I created diagrams below:

## Initial Generation Diagrams
![image](https://i.imgur.com/s5yTNch.png)
![image](https://i.imgur.com/j1hBYcD.png)
![image](https://i.imgur.com/j5GcmSO.png)
![image](https://i.imgur.com/WVQ18Xn.png)

![image](https://i.imgur.com/woX5Uhx.png)

## Possible Evolutions
### Change One Link to Sensor/Not Sensor
This changes a random link on the robot into a sensor if it already was not a sensor and vice versa.

![image](https://i.imgur.com/ytscQg1.png)

### Change Size of Link
Selects a random link and changes its size. Note: This may change the organization of the robot as certain links may no longer fit or joints are not connected

![image](https://i.imgur.com/DvQ2bB3.png)

### Move Links
Moves the links on the robot

![image](https://i.imgur.com/1XNHqYq.png)

### Add or Remove Link
Randomly removes a link from the robot (if there are more than 3 links) or add a link to the robot

![image](https://user-images.githubusercontent.com/15034808/221498424-fb1d00d1-be00-4bd6-9651-fa72435ac87f.png)

### Change a random sensor weight
Exact change as we have seen in the past where weight is changed

## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/

## 3D creature morphologies
For this assignment, I initially created randomly generated creatures with a random # of body components from 3-5. These body components had randomly selected sizes from 0-1 (inclusive) for all three dimensions (x, y, and z). In addition, the joint axes were randomly chosen from a set of (0 0 1, 0 1 0, 1 0 0). These creatures evolved in a population size of 100 across 100 generations. Possible evolutions are below. 

![image](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjYxNjIxOWIxYjg2YmFlNDM1ZDMyNmE3MzM4ODFkYzgyYTkzMGI3MCZjdD1n/xuqKCivjzUZhD8kNNt/giphy.gif)

# Fitness Function
Just like Assignment 4, the fitness function in this 3d evolution model was for the robot to move along the negative x-axis -- away from the user (White block for reference and orientation)

## Fitness Curve
![image](https://user-images.githubusercontent.com/15034808/221745020-71a28f8a-7b89-466e-b2b3-3cb9a558fa4e.png)



## YouTube
This video can be found https://youtu.be/saK9kx8cg8k

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
