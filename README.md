## Credit
Most if not all source code is taken from the ludobots subreddit: https://www.reddit.com/r/ludobots/

## 3D Parallel Hill Climber
For this assignment, I created randomly generated creatures with a random # of body components from 3-5. These body components each had randomly selected sizes from 0-1 (inclusive) for all three of its dimensions (x, y, and z). In addition, the joint axes were randomly chosen from a set of (0 0 1, 0 1 0, 1 0 0). As per the assignment instructions, links with sensors are colored green, and the ones without are colored blue. The decision as to whether a link was a sensor or not was up to a 50/50 coin flip. 

![image](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzM4MTEyNGRkNzY1ZjM2M2JhN2RkNzg3ZDk4N2U4Y2JkZjVkYTk5NiZjdD1n/X0BxQZVsnhE1xNoxgD/giphy.gif)

## Process Diagrams
![image](https://i.imgur.com/s5yTNch.png)
![image](https://i.imgur.com/j1hBYcD.png)
![image](https://i.imgur.com/j5GcmSO.png)
![image](https://i.imgur.com/WVQ18Xn.png)

![image](https://i.imgur.com/woX5Uhx.png)

## Parallel Hill Climber
There were a total of 5 possible changes that could be implemented per generation
### 1) Size Change of a Link
Changing the size of a link may change the location of joints and links as well

### 2) Move a Link
Moves a link somewhere else on the robot

### 3) Add or Remove a Link
Flip a coin whether to remove or add a link. If there are already 3 links, this option defaults to adding a link (there cannot be less than 3 links)

### 4) Change Weights of a Random Link
The same as we have seen in the previous parallel hill climber assignments

### 5) Change a Link to a Sensor From Non-Sensor or Vice-Versa
Randomly selects a link and changes it to a sensor if it wasn't already a sensor. Or changes it back to a normal link without a sensor if was previously a sensor.

## YouTube
This video can be found https://youtu.be/zliWP5UszRM

## Run the Code
After downloading all the code, run the file named **main.py**. This will essentially run search.py and the rest of the code to run the simulation. You can also change the variables in constants.py to modify things such as the number of generations 
