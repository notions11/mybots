## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/

## 3D creature morphologies
For this assignment, I created randomly generated creatures with a random # of body components from 5-10. These body components each had randomly selected sizes from 0-1 (inclusive) for all three of its dimensions (x, y, and z). In addition, the joint axes were randomly chosen from a set of (0 0 1, 0 1 0, 1 0 0). As per the assignment instructions, links with sensors are colored green, and the ones without are colored blue. The decision as to whether a link was a sensor or not was up to a 50/50 coin flip. 

![image](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjYxNjIxOWIxYjg2YmFlNDM1ZDMyNmE3MzM4ODFkYzgyYTkzMGI3MCZjdD1n/xuqKCivjzUZhD8kNNt/giphy.gif)

# Fitness Function
Just like Assignment 4, the fitness function in this 3d evolution model was for the robot to move along the negative x-axis -- away from the user (White block for reference and orientation)

## Fitness Curve
![image](https://user-images.githubusercontent.com/15034808/221500968-42b2709e-7f15-4029-90cc-cc1a33446e1c.png)

## Process Diagrams
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
Randomly removes a link from the robot (if there are more than 3 links) or adds a link to the robot

![image](https://user-images.githubusercontent.com/15034808/221498424-fb1d00d1-be00-4bd6-9651-fa72435ac87f.png)

### Change a random sensor weight
Same change as we have seen in the past where a weight is changed

## YouTube
This video can be found https://youtu.be/saK9kx8cg8k

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
