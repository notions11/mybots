# Final Project (Mix between science and engineering methodologies)
To Sam/Donna/Any Other Grader: For my final project I primarily performed the engineering approach, as titled in the rubric. However, I had already collected some data about evolution types so I thought it would be cool to report these findings and make a science-format claim at the same time. I think the requirements of my assignment mainly appeal to the engineer rubric, but I tried my best to add some bits of the Scientist rubric in my work (hypothesis/results/future work). Just wanted to clarify as my claim may seem a bit week, but I thought it would still be worthwhile to give it a shot :)

![image](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjA1NGRlYWNiNDIyNDE4NjMxMzJhN2Y3M2QwZjNhNzg0NjJmNWQxMiZjdD1n/UrjNykSB77JEvbF1yp/giphy.gif)

## 2-Minute Youtube Video Summary
https://youtu.be/bT5L_RmkHKQ

## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/ . Ideas for this project come from Sam Kriegman's work and his Artificial Life class at Northwestern University.

## Background/Hypothesis
In this final project, I wanted to iterate off of Assignment 8. My goal was to find out whether we can get better evolution by investigating which types of mutations were most effective. My fitness function in my final project was still locomotion where the further the robot moves away from the camera (-x axis) the better. As a refresher, the methods in how I set up my code and mutations are shown in the created the diagrams below:

## Initial Generation Diagrams
I thought it would be more clear to use blocks as my genotype diagram. Imagine the blocks in the following diagrams are the circles that are more common in a genotype chart as they more closely resemble our robots.

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
Exact change as we have seen in the past where the weight of a link is changed

## Experimental Design
I first started by running 20 iterations of 10-population 500-generation tests (20x10x500 = 100,000 sims)

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
Unlike in the control experiment, I only was able to run 10 iterations of 10-population 500-generation tests (10x10x500 = 50,000 sims) due to time constraints. The average final fitness of this new weighted method was only **-5.772688401317849** which is a whole point lower in fitness than when mutation choices were completely random. Looking into how the final products evolved it's very odd looking at the distribution

![image](https://user-images.githubusercontent.com/15034808/225075685-edcad64f-84b9-478b-a9e1-8f8f59afe2d8.png)
![image](https://user-images.githubusercontent.com/15034808/225075809-8dd04285-08ac-4633-ad2c-ad7275c315b8.png)

First of all, the move and change size evolutions don't show up at all (out of 10 iterations they showed up 0 times in the final child). In addition, despite changing to a nonsensor/sensor having the same probability of showing up as a weight change, from this experiment, weight changes happened almost 8 times as often. I don't believe evolution "got stuck" either per se. It seems like the fitness plots have the same amount of progression as in random mutation, but the matter of the fact is that they simply didn't climb as high. 

## Conclusion/Future Work
If I had more time, I would firstly run more iterations with weighted mutation. I think intuitively, my hypothesis made sense: "If certain evolutions were proven to be more effective in the random environment if we were to focus on them then robots could evolve faster". However, this proved not to be the case. I guess this happened because the evolution methods that showed up less are still important. Maybe even though they were less frequent they had more of an impact on the robot whereas weight changing and sensor changing were rather small and thus only improved the robot by a few decimal fitness points.

Another thing I would like to test is giving more weight to the less represented mutations. Maybe moving links and/or adding/removing links would actually be more beneficial to evolution. 

## Run the Code + Saved Robots
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify the number of generations. 

In this Github repo there is also a weight_constants.py and several files in folders **randomevolution** and **weightedevolution** named "train **#**" or "untrain **#**" These files represent the pickling and seeds used to generate robots. To implement these and see the robots generated, you have to change the specific files in robot.py and choose the corresponding weights in solution.py.

Fitness plot data for a given run of evolution is stored in **fitnessPlot.txt**

## Extras
The random folder has additional files that were used to create the graphs and videos in this project. The folder contains data for all the runs that were used for the data collection process. They may be a bit cryptic but contain the files for initial parents, final evolved children, fitness plots, child weights, and mutation history.
