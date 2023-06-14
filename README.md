Game written in python using OpenAI ChatGPT 3.5.

------------------------------------------------

# Prerequisites

#### Python version 3.10+
#### pygame library

------------------------------------------------

# Setup

In order to run the game the **pygame** library is required. Use **pip install pygame** command to add the package.

Run the script using **python BeachBall.py** command in the project directory. 

------------------------------------------------

# Gameplay

The idea is to collect all the clouds wile avoiding the birds. 
If any bird touches the ball the game is over. When all the clouds are collected, user can proceed to the next, more difficult stage.
While proceeding, each time a new stage is generated an additional bird is added. Every two enemy added, 
an additional speed of the bird is added to the array of speeds which is displayed on the screen together with the current amount of birds and the total score.

- Move the ball: Left/Right arrow keys
- Jump: Up arrow
- Reset the game: Space bar
- Proceed to next stage: Enter
