# Final Project (Mix between science and engineering methodologies)
For my final project I primarily performed the engineering approach, as stated in the rubric. However, I had already collected some data about evolution types so I thought it would be cool and worthwhile to report these findings and make a science-format claim at the same time. 
![image](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjA1NGRlYWNiNDIyNDE4NjMxMzJhN2Y3M2QwZjNhNzg0NjJmNWQxMiZjdD1n/UrjNykSB77JEvbF1yp/giphy.gif)

## 2-Minute Youtube Video Summary
https://youtu.be/bT5L_RmkHKQ

## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/

## Background/Hypothesis
In this final project, I wanted to iterate off of Assignment 8 and find out whether we can get better evolution by investigating which types of mutations were most effective. As a refresher the following is how I set up my code and mutations I created the diagrams below:

## Initial Generation Diagrams
![image](https://i.imgur.com/s5yTNch.png)
![image](https://i.imgur.com/j1hBYcD.png)
![image](https://i.imgur.com/j5GcmSO.png)
![image](https://i.imgur.com/WVQ18Xn.png)

![image](https://i.imgur.com/woX5Uhx.png)

## Possible Mutations
### Change One Link to Sensor/Not Sensor
This changes a random link on the robot into a sensor if it already was not a sensor and vice versa.

![image](https://i.imgur.com/ytscQg1.png)

### Change the Size of the Link
Selects a random link and change its size. Note: This may change the organization of the robot as certain links may no longer fit or joints are not connected

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
I first started by running 20 iterations of 10-population 500-generation tests (20x10x500 = 100000 sims)

We can look at the fitness functions of the following: 
![image](https://user-images.githubusercontent.com/15034808/224853826-788551fc-0e3e-4a7f-9918-de8a9fe5f118.png)

This yielded a final average fitness of **-6.903325734489094**. This got me thinking: "What mutations were the most prominent in order to get to the final evolution states per iteration? I kept track of the counts of mutations per final robot and plotted them in this bar chart:

![image](https://user-images.githubusercontent.com/15034808/224854122-7aaa2b00-79d3-4c17-8b2a-5caa13055f51.png)

As we can see, based on our robot creation, maybe **every robot structure is functional** you just need to change sensors and weights in order to make it work. Thus, I wanted to set weights to the "random" mutation so that the changing of sensors and weights occurred more often. My hypothesis is that successful evolution will occur more often with mutation types that appear more often in successful generations

![image](https://user-images.githubusercontent.com/15034808/224855109-72c95915-6e72-47f8-ae3d-28cef9af1174.png)

| Evolution Type | Weighted Percentage |
| ------------- | ------------- |
| Change to a Sensor/Nonsensor  | 0.38  |
| Change Size  | 0.11  |
| Move  | 0.06  |
| Add or Remove  | 0.10  |
| Change Weights  | 0.36  |


## Results
Using the new weighted assignment of evolution I was able to generate the following fitness plots
![image](https://user-images.githubusercontent.com/15034808/225074233-1a166fc3-064b-4d1a-9c46-2a5efd9961d6.png)
Unlike in the control experiment, I only was able to run 10 iterations of 10-population 500-generation tests (10x10x500 = 50000 sims) due to time constraints. The average final fitness of this new weighted method was only **-5.772688401317849** which is a whole point lower than when mutation choices were completely random. Looking into how the final products evolved it's very odd looking at the distribution

![image](https://user-images.githubusercontent.com/15034808/225075685-edcad64f-84b9-478b-a9e1-8f8f59afe2d8.png)
![image](https://user-images.githubusercontent.com/15034808/225075809-8dd04285-08ac-4633-ad2c-ad7275c315b8.png)

First of all, the move and change size evolutions don't show up at all. In addition, despite changing to a nonsensor/sensor having the same probability of showing up as a weight change, from this experiment, weight changes happened almost 8 times as often. 

## Conclusion/Future Work
If I had more time, I would firstly run more iterations with weighted mutation. I think intuitively, my hypothesis made sense: "If certain evolutions were proven to be more effective in the random environment if we were to focus on them then robots could evolve faster". However, this proved not to be the case. I guess this happened because the evolution methods that showed up less are still important. Maybe even though they were less frequent they had more of an impact on the robot whereas weight changing and sensor changing were rather small and thus only improved the robot by a few decimal fitness points.

## Run the Code + Saved Robots
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify the number of generations. In this Github repo there is also a weight_constants.py and several files named "train **#**" or "untrain **#**" These files represent the pickling and seeds used to generate robots. To implement these you have to change the specific files in robot.py and choose the corresponding weights in solution.py
