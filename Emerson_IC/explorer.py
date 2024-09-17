# EXPLORER AGENT
# @Author: Tacla, UTFPR
#
### It walks randomly in the environment looking for victims. When half of the
### exploration has gone, the explorer goes back to the base.

import sys
import os
import random
import math
from abc import ABC, abstractmethod
from vs.abstract_agent import AbstAgent
from vs.constants import VS
from map import Map

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def front(self):
        if not self.is_empty():
            x= self.items.pop()
            self.items.append(x)
            return x


    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def search(self, item):
        size=len(self.items)
        for i in range(size):
            if self.items[i]==item:
                return 1
        return 0

class Untried:
    def __init__(self):
        self.position = []
        self.untried = [] 

    def push(self, item):
        self.position.append(item)
        actions=[0,1,2,3,4,5,6,7]
        self.untried.append(actions)

    def search(self, item):
        size=len(self.position)
        for i in range(size):
            if self.position[i]==item:
                return i
        return 0
    
    def empty(self, item):
        i=self.search(item)
        return len(self.untried[i])==0

    def untried_action(self,item,action):
        i=self.search(item)
        size=len(self.untried[i])
        for j in range(size):
            if self.untried[i][j]==action:
                self.untried[i].pop(j)
                return 1
        return 0


    

class Explorer(AbstAgent):
    position_visited = {(0,0)}

    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env: a reference to the environment 
        @param config_file: the absolute path to the explorer's config file
        @param resc: a reference to the rescuer agent to invoke when exploration finishes
        """

        super().__init__(env, config_file)
        self.walk_stack = Stack()  # a stack to store the movements
        self.untried = Untried()   # a stack to store untried actions in each position
        self.unbacktracking = 0    # a boolean 
        self.set_state(VS.ACTIVE)  # explorer is active since the begin
        self.resc = resc           # reference to the rescuer agent
        self.x = 0                 # current x position relative to the origin 0
        self.y = 0                 # current y position relative to the origin 0
        self.begin = 0             # next direction
        self.map = Map()           # create a map for representing the environment
        self.sizemap = 2852        #size of the map
        self.random= 0             # the agentes walks in rando direction or not
        self.victims = {}          # a dictionary of found victims: (seq): ((x,y), [<vs>])
                                   # the key is the seq number of the victim,(x,y) the position, <vs> the list of vital signals

        # put the current position - the base - in the map
        self.map.add((self.x, self.y), 1, VS.NO_VICTIM, self.check_walls_and_lim())

        self.begin=self.get_begin()-1

        #put the current position in the untried stack
        self.untried.push((self.x,self.y))

    def get_next_position(self):
        self.unbacktracking = 0

        # Check the neighborhood walls and grid limits
        obstacles = self.check_walls_and_lim()

        direction=self.begin

        # Loop until a CLEAR position is found
        while True:

            # Check if there is some untried move
            if not self.untried.empty((self.x,self.y)):

                if self.random:
                    # Get a random direction
                    direction = random.randint(0, 7)

                else:
                    if self.get_clockwise():
                        direction +=self.get_step()
                        if direction>7:
                            direction=direction-8
                    else:
                        direction -=self.get_step()
                        if direction<0:
                            direction=direction+8

                #check if this is an untried action
                if(self.untried.untried_action((self.x,self.y),direction)):

                    # Check if the corresponding position in walls_and_lim is CLEAR
                    if (obstacles[direction] == VS.CLEAR):
                        return Explorer.AC_INCR[direction]
                        
            else:
                self.unbacktracking = 1
                dx, dy = self.walk_stack.pop()
                dx = dx * -1
                dy = dy * -1
                return (dx,dy)
                
    
    def explore(self):
        # get an random increment for x and y       
        dx, dy = self.get_next_position()


        # Moves the body to another position
        rtime_bef = self.get_rtime()
        result = self.walk(dx, dy)
        rtime_aft = self.get_rtime()

        # Test the result of the walk action
        # Should never bump, but for safe functionning let's test
        if result == VS.BUMPED:
            # update the map with the wall
            self.map.add((self.x + dx, self.y + dy), VS.OBST_WALL, VS.NO_VICTIM, self.check_walls_and_lim())
            #print(f"{self.NAME}: Wall or grid limit reached at ({self.x + dx}, {self.y + dy})")

        if result == VS.EXECUTED:
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim

            # update the agent's position relative to the origin
            self.x += dx
            self.y += dy

            Explorer.position_visited.add((self.x,self.y))

            if not self.unbacktracking:
                self.walk_stack.push((dx, dy))

                # put the current position in the untried stack
                if not self.untried.search((self.x,self.y)):
                    self.untried.push((self.x,self.y))

            # Check for victims
            seq = self.check_for_victim()
            if seq != VS.NO_VICTIM:
                vs = self.read_vital_signals()
                self.victims[vs[0]] = ((self.x, self.y), vs)
                print(f"{self.NAME} Victim found at ({self.x}, {self.y}), rtime: {self.get_rtime()}")
            #print(f"{self.NAME} Seq: {seq} Vital signals: {vs}")
            
            # Calculates the difficulty of the visited cell
            difficulty = (rtime_bef - rtime_aft)
            if dx == 0 or dy == 0:
                difficulty = difficulty / self.COST_LINE
            else:
                difficulty = difficulty / self.COST_DIAG

            # Update the map with the new cell
            self.map.add((self.x, self.y), difficulty, seq, self.check_walls_and_lim())
            #print(f"{self.NAME}:at ({self.x}, {self.y}), diffic: {difficulty:.2f} vict: {seq} rtime: {self.get_rtime()}")

        return

    def come_back(self):
        dx, dy = self.walk_stack.pop()
        dx = dx * -1
        dy = dy * -1

        result = self.walk(dx, dy)
        if result == VS.BUMPED:
            print(f"{self.NAME}: when coming back bumped at ({self.x+dx}, {self.y+dy}) , rtime: {self.get_rtime()}")
            return
        
        if result == VS.EXECUTED:
            # update the agent's position relative to the origin
            self.x += dx
            self.y += dy
            #print(f"{self.NAME}: coming back at ({self.x}, {self.y}), rtime: {self.get_rtime()}")
        
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""


        '''
        consumed_time = self.TLIM - self.get_rtime()
        if consumed_time < self.get_rtime():
            self.explore()
            return True
        '''
        
        
        if len(Explorer.position_visited) < self.sizemap:
            self.explore()
            return True
            
        # time to come back to the base
        if self.walk_stack.is_empty() or (self.x == 0 and self.y == 0):
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            #print(f"{self.NAME}: rtime {self.get_rtime()}, invoking the rescuer")
            #input(f"{self.NAME}: type [ENTER] to proceed")
            #self.resc.go_save_victims(self.map, self.victims)
            return False
        
        return True

