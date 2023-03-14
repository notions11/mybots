# Final Project (Mix between science and engineer methodologies)
![image](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjA1NGRlYWNiNDIyNDE4NjMxMzJhN2Y3M2QwZjNhNzg0NjJmNWQxMiZjdD1n/UrjNykSB77JEvbF1yp/giphy.gif)

## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/

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

## Experimental Design
I first started by running 20 iterations of 10-population 500-generation tests

We can look at the fitness functions of the following: 
![image](https://user-images.githubusercontent.com/15034808/224853826-788551fc-0e3e-4a7f-9918-de8a9fe5f118.png)

This yielded a final average fitness of **-6.903325734489094**. This got me thinking: "What evolutions were the most prominent in order to get to the final evolution states per iteration? I kept track of the counts of evolutions per final robot and plotted them in this bar chart:

![image](https://user-images.githubusercontent.com/15034808/224854122-7aaa2b00-79d3-4c17-8b2a-5caa13055f51.png)

As we can see, based off our robot creation, maybe **every robot structure is functional** you just need to change sensors and weights in order to make it work. Thus, I wanted to set weights to the "random" evolution so that the changing of sensors and weights occurred more often. My hypothesis is that successful evolution will occur more often with evolution types that appear more often in successful generations

![image](https://user-images.githubusercontent.com/15034808/224855109-72c95915-6e72-47f8-ae3d-28cef9af1174.png)

| Evolution Type | Weighted Percentage |
| ------------- | ------------- |
| Change to a Sensor/Nonsensor  | 0.38  |
| Change Size  | 0.11  |
| Move  | 0.06  |
| Add or Remove  | 0.10  |
| Change Weights  | 0.36  |


# Fitness Function
Just like Assignment 4, the fitness function in this 3d evolution model was for the robot to move along the negative x-axis -- away from the user (White block for reference and orientation)


## YouTube
This video can be found https://youtu.be/saK9kx8cg8k

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
