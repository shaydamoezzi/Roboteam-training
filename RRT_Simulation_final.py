#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 23:29:07 2020

@author: shaydamoezzi

Roboteam training: RRT simulation
"""
#importing modules
import random, pygame, sys, math
from math import *
from pygame import *



#variable initializations
XDIM = 720
YDIM = 500
windowSize = [XDIM, YDIM]
delta = 25.0        #maximum distance from parent to child node
POINT_RADIUS = 15
NUMNODES = 5000     #maximum number of nodes we will let the simulation create
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = 0, 0, 255
GREEN = 0, 255, 0
CYAN = 0,255,255
count = 0
obstructions = []    #list of rectangular obstructions (to be created later)


pygame.init()
screen = pygame.display.set_mode(windowSize)


class Node(object):
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent


def generate_random_node():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        noCollision = collides(p)
        if not noCollision:
            return p
 

def dist(p1,p2):
    """
    Inputs: p1 and p2 are points represented ny a tuple (x,y)
    
    Output: Tuple, The euclidian distance between the two points

    """    
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))



def reached_goal(p1, p2, radius):
    """
    Inputs: p1 and p2 are points represented ny a tuple (x,y)
            -p1 is the coordinate of the current node
            -p2 is the coordinate of the goal node
            Radius: the radius of the circle that is representing our goal node
    
    Output: Boolean, True if the current node has reached the goal node

    """  
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def nearest_node(p1,p2):
    if dist(p1,p2) < delta:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return (p1[0] + delta*cos(theta), p1[1] + delta*sin(theta))



def draw_obstacles():
    """
    Creates rectangle "obstacles" in window at predetermined locations

    """
    global obstructions
    obstructions = []
    obstructions.append(pygame.Rect((100,50),(200,150)))
    obstructions.append(pygame.Rect((400,200),(200,100)))
    obstructions.append(pygame.Rect((200,400), (300, 50)))
    for rect in obstructions:
        draw.rect(screen, WHITE, rect)

def collides(p):    #check if point collides with the obstacle
    """
    Input: p, a tuple of x,y coordinates of node
    
    Output: Boolean, returns True if coordinates of node never equal a coordinate
            within boundaries of obstructions, False if does not
    """
    for rect in obstructions:
        if rect.collidepoint(p):
            return True
    return False
 

def set_simulation():
    global count
    screen.fill(BLACK)
    draw_obstacles()
    count = 0

def main():
    set_simulation()
    print("Running Rapidly Expanding Random Tree Simulation.")
    global count
    nodes = []
    initialP = (50, 150)    #first node coordinates
    goalP = (700, 450)      #goal node coordinates

    initialPoint = Node(initialP, None) #no parent node because it is the root
    nodes.append(initialPoint) # add each node we create to a list
    draw.circle(screen, RED, initialPoint.point, POINT_RADIUS)
    goalPoint = Node(goalP, None)       #initially it has no parent because that will be determined upon running simulation
    draw.circle(screen, GREEN, goalPoint.point, POINT_RADIUS)
    currentState = 'building tree'
    goalNode = []
    

    while True:

        if currentState == 'reached goal':  #goal has been reached, now tracing back each node to root to draw path
            currNode = goalNode.parent
            display.set_caption('Goal Reached! The path is highlighted in yellow.')
            while currNode.parent != None:
                draw.line(screen, YELLOW, currNode.point, currNode.parent.point, 2)
                currNode = currNode.parent
            

        elif currentState == 'building tree':
            count += count
            display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while not foundNext:
                    random_node = generate_random_node()
                    parentNode = nodes[0]
                    for node in nodes:      #iterating through all our existing nodes to find one with closest distance to new node
                        if dist(node.point,random_node) <= dist(parentNode.point,random_node):
                            newPoint = nearest_node(node.point,random_node)
                            if not collides(newPoint):      #checking for collisions
                                parentNode = node
                                foundNext = True

                newnode = nearest_node(parentNode.point, random_node)  
                nodes.append(Node(newnode, parentNode))
                circ_rad = 4
                draw.circle(screen, (0, 255, 255), (int(newnode[0]), int(newnode[1])), 3) #drawing new node onto screen
                draw.line(screen, RED, parentNode.point, newnode, 1)    #drawing line from parent to new node

                if reached_goal(newnode, goalPoint.point, 20):
                    currentState = 'reached goal'
                    goalNode = nodes[-1]  #goal node is the final node in our nodes list

                
            else:
                return print("Could not find a path with given amount of nodes.")

        #handle quit event
        for e in event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                pygame.display.quit()
                pygame.quit()
                sys.exit("Exiting")
                

        display.update()

main()

 