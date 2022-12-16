# FlappyBirdAI

## Abstract
Robotics and artificial intelligence have been prevalent for more than 10 years, and testing the effectiveness of new pathfinding or search optimization algorithms is a common task. These algorithms often need to be tested in simulated or artificial environments, which can be created specifically for this purpose. Games can also serve as a testing ground for these algorithms, allowing for the performance of the algorithms to be compared using artificial agents that follow the prescribed algorithm within the game environment. This project explores the potential of using a genetic algorithm called NEAT (Neuro-Evolution of Augmenting Topologies), to play the Flappy Bird game without explicit human intervention.

## How to Run
1. Unzip the file and install the required dependencies such as os, pygame, neat and random
2. Run "python FlappyBird.py" in the terminal
3. This will start the training and after few iterations, the bird will be able to play through the game without dying

## Approach
### Creating Flappy Bird game
We started with creating a baseline Flappy Bird game using
the pygame environment. Following steps were included in
the game -
- Created a Pygame window and set the title, size, and background color.
- Load the images that we needed for the game, such as the bird, pipes, and background.
- Defined the classes for the bird, pipes, and background objects. The bird class includes properties such as the bird’s position, velocity, and acceleration. The pipe class includes properties such as the pipe’s position and width. The background class includes the image for the background and a method for scrolling the background.
- Wrote the code to handle the game mechanics, such as the bird’s movement, the spawning and movement of the pipes, and the scoring system.
- Set up a game loop that updates the game objects and handles user input. The game loop also check for collisions and end the game if the bird hits a pipe or the ground.

### Defining the NEAT Parameters
Once the baseline game was ready, we proceeded with integrating a NEAT-algorithm based model with the game. The challenge here would be to devise an algorithm that should be able to detect the obstacle, find the distance between the obstacles relative to the current position of the bird, analyze the time to reach the obstacle, and then give an output by which the bird should successfully be able to void the obstacles. For this, calculating a valid fitness function was crucial.
The data that we considered while training the algorithm are: -
- Score
- Energy
- Distance travelles
- Vertical distance from pipe opening
