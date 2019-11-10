'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search
import math

import time

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below
    
    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None
    SHOPS=None
    CUSTOMERS=None
    MAXBAGS = 0

    # Used in tests
    TIME = time.time()

    MOVES = ('West','North','East','South') # West: left / East: right 

   # --------------- Common functions to a SearchProblem -----------------

    # Obtain the total remaining pizzas to be delivered
    def getRemaining(self, customers):
        remaining = 0
        for c in customers:
            remaining += c[2]

        return remaining

    # Check if the cyclist can go to the next position
    # pos is the next position
    def canPass(self, pos, state):
        pizzas = state[1]
        customers = state[2]
        electric = state[3]
        charge = state[4]
        level = state[5]

        result = True
        if electric and charge > 0:
            result = True
        elif electric and charge <= 0:
            result = False

        # Going from pizza to customer directly or from charging station to customer directly is not allowed
        if ((self.getAttribute(state[0], 'recharge') and self.getAttribute(pos, 'unload')) or
            (self.getAttribute(state[0], 'unload') and self.getAttribute(pos, 'recharge')) or
            (self.getAttribute(state[0], 'unload') and self.getAttribute(pos, 'unload')) or
            (self.getAttribute(state[0], 'unload') and self.getAttribute(pos, 'unload')) or
            (state[0] in self.SHOPS and self.getAttribute(pos, 'unload')) or
            (self.getAttribute(state[0], 'unload') and pos in self.SHOPS)):
            result = result and False
            

        # If the cyclist does not have pizzas on board or the next position is
        # already fulfilled, the cyclist cannot go through
        for c in customers:
            if c[0] == pos[0] and c[1] == pos[1] and c[2] == 0:
                result = result and False
                break
            elif c[0] == pos[0] and c[1] == pos[1] and pizzas == 0:
                result = result and False
                break

        next_level = self.getAttribute(pos, 'level')
        if next_level == None:
            result = result and True
        elif math.fabs(level - next_level) <= 1:
            result = result and True
        else:
            result = result and False

        return result

    # Get the total discharge to the specified position
    # Currently bike has a range of 10 cells
    def getDischarge(self, pos, electric):
        dischargeRate = 10.0
        if electric:
            return dischargeRate #* (self.getAttribute(pos, 'cost')/2)
        else:
            return 0

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        pos = state[0]
        pizzas = state[1]
        customers = state[2]
        electric = state[3]
        charge = state[4]
        level = state[5]

        acciones = []

        # Check the neighbour cells
        if(pos[0]-1 >= 0 and
            not self.getAttribute((pos[0]-1, pos[1]), 'blocked') and
            self.canPass((pos[0]-1, pos[1]), state)):
            acciones.append('West')

        if(pos[0]+1 < self.CONFIG['map_size'][0] and
            not self.getAttribute((pos[0]+1, pos[1]), 'blocked') and
            self.canPass((pos[0]+1, pos[1]), state)):
            acciones.append('East')

        if(pos[1]-1 >= 0 and
            not self.getAttribute((pos[0], pos[1]-1), 'blocked') and
            self.canPass((pos[0], pos[1]-1), state)):
            acciones.append('North')

        if(pos[1]+1 < self.CONFIG['map_size'][1] and
            not self.getAttribute((pos[0], pos[1]+1), 'blocked') and
            self.canPass((pos[0], pos[1]+1), state)):
            acciones.append('South')

        # Check if it is a customer
        for c in customers:
            if(pos[0] == c[0]  and pos[1] == c[1]):
                acciones.append('Unload')
                break

        # Check if it's a pizza shop
        if(pos in self.SHOPS):
            acciones.append('Load')

        # Check if the bike is electric and needs recharging. Pizza shops also recharge batteries
        if(electric and (self.getAttribute(pos, 'recharge') or pos in self.SHOPS) and charge < 100):
            acciones.append('Recharge')

        return acciones


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        pos = state[0]
        old_pos = pos
        pizzas = state[1]
        customers = state[2]
        electric = state[3]
        charge = state[4]
        level = state[5]

        # Converts the customer tuple and all of it's items to lists to be able to modify them
        customers = list(customers)
        for i in xrange(len(customers)):
            customers[i] = list(customers[i])

        # Set the next position and the remaining charge
        if(action == 'West'):
            pos = (pos[0]-1, pos[1])
            charge = max(0, charge - self.getDischarge(pos, electric))
        if(action == 'East'):
            pos = (pos[0]+1, pos[1])
            charge = max(0, charge - self.getDischarge(pos, electric))

        if(action == 'North'):
            pos = (pos[0], pos[1]-1)
            charge = max(0, charge - self.getDischarge(pos, electric))
        if(action == 'South'):
            pos = (pos[0], pos[1]+1)
            charge = max(0, charge - self.getDischarge(pos, electric))

        old_level = self.getAttribute(old_pos, 'level')
        new_level = self.getAttribute(pos, 'level')
        # If the level of the position it is going to is None, the level stays the same
        if (not new_level == None):
            level = new_level
        # If we are going down, the battery refills a little bit
        # If we are going up, the battery drains faster
        if not old_level == None and not new_level == None:
            if old_level - new_level > 0:
                charge = max(0, charge + math.floor(self.getDischarge(pos, electric)/4))
            elif old_level - new_level < 0:
                charge = max(0, charge - (self.getDischarge(pos, electric)*2))

        # Recharge if the remaining total is lower than 100% if it is in a pizza shop
        # Also simulate that the recharging process is slow
        if action == 'Recharge' and (charge < 100 or (pos in self.SHOPS and charge < 100)):
            charge = min(charge + 20.0, 100.0)

        # Load one pizza per tick. Simulates that pizzas need to be done
        if(action == 'Load') and pizzas < self.MAXBAGS:
            pizzas += 1

        # Unload the pizzas
        if(action == 'Unload'):
            for x in customers:
                customer = (x[0], x[1])
                order = x[2]
                if pizzas > 0 and (customer[0] == pos[0] 
                    and customer[1] == pos[1]) and order > 0:
                    # Deliver all pizzas needed
                    x[2] = max(0, order - pizzas)
                    pizzas = max(0, pizzas - order)

        # Converts the customer list and all of it's items to tuples to be able to work with
        # the search algorithm
        for i in xrange(len(customers)):
            customers[i] = tuple(customers[i])

        return (pos, pizzas, tuple(customers), electric, charge, level)


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        goal = self.GOAL

        isGoal = self.getRemaining(state[2]) == 0 and state[2] == goal[2]
        isGoal = isGoal and state[0][0] == goal[0][0] and state[0][1] == goal[0][1]
        isGoal = isGoal and state[1] == goal[1]

        if isGoal:
            end = time.time()
            elapsed = end - self.TIME
            m, s = divmod(elapsed, 60)
            h, m = divmod(m, 60)
            print("Finished in %02d:%02.2f" % (m, s))

        return isGoal

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        pos = state2[0]
        pizzas = state[1]
        cost = 9223372036854775807 # Maximum integer posible. In case things go wrong
        electric = state[3]
        charge = state[4]
        old_level = state[5]
        new_level = state2[5]
        discharge = 1-(charge/100)

        level_cost = 1

        # Going down costs less, but going up 10x the pizzas the biker is carrying.
        if old_level - new_level < 0 and pizzas > 0:
            level_cost = pizzas * 10
        elif old_level - new_level > 0:
            level_cost = 0.25

        # If the bike is electric, when the charge is low, the cost to move is bigger
        # Carrying pizzas has a cost alongside the cost of running downhill or uphill.
        # Recharging has no cost
        if action in ('West','North','East','South'):
            cost = ((self.getAttribute(state2[0], 'cost') * (1+discharge)) + pizzas) * level_cost
        elif action in ('Unload', 'Load'):
            cost = math.fabs(state[1] - state2[1])
        elif action == 'Recharge':
            cost = 0

        return cost

    def distanceToNearestCharger(self, customer):
        chargers = []
        dist = 9223372036854775807

        for x in xrange(self.CONFIG['map_size'][0]):
            for y in xrange(self.CONFIG['map_size'][1]):
                if self.getAttribute((x,y), 'recharge'):
                    chargers.append((x, y))

        for c in chargers:
            distX = math.fabs(c[0] - customer[0])
            distY = math.fabs(c[1] - customer[1])
            dist = min(dist, math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)))

        return dist

    def distanceToNearestShop(self, customer):
        dist = 9223372036854775807
        shop = None

        for p in self.SHOPS:
            distX = math.fabs(p[0] - customer[0])
            distY = math.fabs(p[1] - customer[1])
            d = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))
            if d < dist:
                dist = d
                shop = p

        return dist, shop

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        # Define the heuristic to use. Distance means the sum of all distances
        # 0: Manhattan distances. Test only.
        # 1: Farthest distance first
        # 2: Closest distance first
        # 3: Farthest house and biggest order first
        # 4: Farthest house and lowest order first
        # 5: Nearest charging point and biggest order first. If the bike is not electric, defaults to 3
        # 6: Group by zones arround a shop
        # 7: 6 + biggest order first
        # 8: 6 + lowest order first
        # 9: 6 + nearest charging point. If bike is not electric, defaults to 6
        # 10: Full bag and many little orders first 
        # 11: Full bag and biggest orders first 
        heuristic = 1

        pos = state[0]
        pizzas = state[1]
        customers = state[2]
        remaining = self.getRemaining(customers)
        electric = state[3]
        charge = state[4]
        level = state[5]

        max_order = 5
        dX = math.fabs(self.CONFIG['map_size'][0] - pos[0] )
        dY = math.fabs(self.CONFIG['map_size'][1] - pos[1])
        max_distance = math.sqrt(math.pow(dX, 2) + math.pow(dY, 2))

        # Always prioritize lower levels while carrying pizzas
        h = pizzas * level
        #h += remaining - pizzas
        #h = 0


        if heuristic == 5 and not electric:
            heuristic = 3
        if heuristic == 9 and not electric:
            heuristic = 6

        if self.getRemaining(customers) == 0:
            distX = math.fabs(self.GOAL[0][0] - pos[0])
            distY = math.fabs(self.GOAL[0][1] - pos[1])
            h = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))
        elif heuristic == 0:
            h = 0
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))
        elif heuristic == 1:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += (max_distance+1 - math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)))
        elif heuristic == 2:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))
        elif heuristic == 3:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += (max_distance+1 - math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))) + (max_order+1 - c[2])
        elif heuristic == 4:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += (math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))) + c[2]
        elif heuristic == 5:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0:
                    h += (max_order+1 - c[2]) + self.distanceToNearestCharger(c)
        elif heuristic == 6:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    dist_customer, shop = self.distanceToNearestShop(c)
                    distX = math.fabs(shop[0] - pos[0])
                    distY = math.fabs(shop[1] - pos[1])
                    dist = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + dist_customer
                    h += dist
        elif heuristic == 7:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    dist_customer, shop = self.distanceToNearestShop(c)
                    distX = math.fabs(shop[0] - pos[0])
                    distY = math.fabs(shop[1] - pos[1])
                    dist = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + dist_customer
                    h += dist + (max_order+1 - c[2])
        elif heuristic == 8:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    dist_customer, shop = self.distanceToNearestShop(c)
                    distX = math.fabs(shop[0] - pos[0])
                    distY = math.fabs(shop[1] - pos[1])
                    dist = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + dist_customer
                    h += dist + c[2]
        elif heuristic == 9:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    dist_customer, shop = self.distanceToNearestShop(c)
                    distX = math.fabs(shop[0] - pos[0])
                    distY = math.fabs(shop[1] - pos[1])
                    dist = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + dist_customer
                    h += dist + self.distanceToNearestCharger(c)
        elif heuristic == 10:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0: 
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + c[2] + (self.MAXBAGS+1 - pizzas)
        elif heuristic == 11:
            for c in customers:
                if not c[0] == pos[0] and not c[1] == pos[1] and not c[2] == 0:
                    distX = math.fabs(c[0] - pos[0])
                    distY = math.fabs(c[1] - pos[1])
                    h += math.sqrt(math.pow(distX, 2) + math.pow(distY, 2)) + (max_order+1 - c[2]) + (self.MAXBAGS+1 - pizzas)

        if electric:
            h *= 1-(charge/100)

        return math.ceil(h * (self.getAttribute(pos, 'cost')/2 * (level+1)))


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print('\nMAP: {}\n'.format(self.MAP))
        print('POSITIONS: {}\n'.format(self.POSITIONS))
        print('CONFIG: {}\n'.format(self.CONFIG))

        print('map_size: {}\n'.format(self.CONFIG['map_size']))

        # Initialize self.SHOPS with pizza shops data and maxBags with the config parameter
        self.SHOPS = self.POSITIONS['pizza']
        self.MAXBAGS = self.CONFIG['maxBags']
        customers = []
        goalCustomers = []

        # If there is at least one charging station, the bike is electric
        electric = False

        # This indicates the terrain level
        level = 0

        # Add customers to customer with total amount from order
        # Add customers to goalCustomers with 0 pizzas ordered, for the final state
        # Set the bike as electric if there is at least one charging station
        for x in xrange(self.CONFIG['map_size'][0]):
            for y in xrange(self.CONFIG['map_size'][1]):
                if self.getAttribute((x,y), 'unload'):
                    customers.append((x, y, self.getAttribute((x,y), 'objects')))
                    goalCustomers.append((x, y, 0))
                if self.getAttribute((x, y), 'recharge'):
                    electric = True

        # ((X, Y), pizzas_carried, orders, electric, charge, level)
        # We need to convert the customers list into a tuple because the search algorithm needs the state to be hashable
        # and lists are not hashable
        initial_state = (self.AGENT_START, 0, tuple(customers), electric, 100.0, 0)
        final_state = (self.AGENT_START, 0, tuple(goalCustomers), electric, 100.0, 0)
        algorithm = simpleai.search.astar

        return initial_state,final_state,algorithm

    def printState (self,state):
        '''Return a string to pretty-print the state '''

        pos = state[0]
        pizzas = state[1]
        customers = state[2]
        level = state[5]
        pps='\nPosition: {}, {} | Level: {}\nPizzas: {} | Remaining: {}\nElectric: {} | Charge: {}\nCustomer(s) waiting for delivery:\n'.format(pos[0], pos[1], level, pizzas, self.getRemaining(customers), state[3], state[4])
        for c in customers:
            if not c[2] == 0:
                pps += '  ({}, {}): {} pizza(s)\n'.format(c[0], c[1], c[2])
        return (pps)

    def getPendingRequests (self, state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        pos = state[0]
        customers = state[2]
        requests = None

        # Get the number of requests from the state
        for c in customers:
            if c[0] == pos [0] and c[1] == pos[1]:
                requests = c[2]
                
        return requests

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string
           
           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''

        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData
        
    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True
      
        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)
            
        print ('-- INITIALIZATION OK')
        return True
        
    # END initializeProblem