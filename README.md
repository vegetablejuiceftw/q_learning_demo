# Conclusions:
First task was of course to refactor (nuke) the codebase as it was lacking on most parts even for me...

This kind of learning algorithm seems very _organic_ in the sense it gets stuck in **old patterns**.
This is very well illustrated in network packet branch where I explored the packet routing likeness of this setup to simulate a workload distribution system.

![alt text](http://i.imgur.com/6WmMxGJ.gif "Network simulation")
Here we can see once the packet(actor) has reached a goal, the goal goes to a sleep state (wall in the old demo).
What is apparent is that the nodes chosen are all close to the ones chosen last.
There are areas of higher usage peak.
It is clear from this that the actor will choose an path that it knows to be good before evaluating anything closer to its spawn point.

What is not as apparent is that the average trip time keeps increasing.
As I also have observed the actor getting stuck in circular paths, the current feedback mechanism needs to be revisited.

One possible solution to this is the introduction of randomness through random placement of the actor.
While this is effective in forcing new paths, it also makes it less intuitive to understand shortcomings of this implementation.

# q_learning_demo
This is the code for "How to use Q Learning in Video Games Easily" by Siraj Raval on Youtube

##Overview

This is the associated code for [this](https://youtu.be/A5eihauRQvo) video on Youtube by Siraj Raval. This is a simple example of a type of [reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning)
called [Q learning](https://en.wikipedia.org/wiki/Q-learning). 

	● Rules: The agent (yellow box) has to reach one of the goals to end the game (green or red cell).
	● Rewards: Each step gives a negative reward of -0.04. The red cell gives a negative reward of -1. The green one gives a positive reward of +1.
	● States: Each cell is a state the agent can be.
	● Actions: There are only 4 actions. Up, Down, Right, Left.

##Dependencies

None! Native Python

##Usage

Run `python Learner.py` in terminal to see the the bot in action. It'll find the optimal strategy pretty fast (like in 15 seconds)

##Challenge

The challenge for this video is to 

* modify the the game world so that it's bigger 
* add more obstacles
* have the bot start in a different position

**Bonus points if you modify the bot in some way that makes it more efficient**

#Due Date is Thursday at noon PST January 12th 2017

##Credits

The credits for this code go to [PhillipeMorere](https://github.com/PhilippeMorere). I've merely created a wrapper to get people started.
