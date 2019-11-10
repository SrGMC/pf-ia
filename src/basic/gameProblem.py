'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''

from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search
import math

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

    MOVES = ('West','North','East','South') # West: left / East: right 

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        pos = state[0]
        customer = (state[2][0], state[2][1])
        acciones = []
        if(pos[0]-1 >= 0 and
            not self.getAttribute((pos[0]-1, pos[1]), 'blocked')):
            acciones.append('West')

        if(pos[0]+1 < self.CONFIG['map_size'][0] and
            not self.getAttribute((pos[0]+1, pos[1]), 'blocked')):
            acciones.append('East')

        if(pos[1]-1 >= 0 and
            not self.getAttribute((pos[0], pos[1]-1), 'blocked')):
            acciones.append('North')

        if(pos[1]+1 < self.CONFIG['map_size'][1] and
            not self.getAttribute((pos[0], pos[1]+1), 'blocked')):
            acciones.append('South')

        if(pos[0] == customer[0]  and pos[1] == customer[1]):
            acciones.append('Unload')

        if(pos in self.SHOPS):
            acciones.append('Load')

        return acciones


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        next_state = state
        pos = state[0]
        pizzas = state[1]
        customer = list(state[2])

        if(action == 'West'):
            pos = (pos[0]-1, pos[1])
        if(action == 'East'):
            pos = (pos[0]+1, pos[1])

        if(action == 'North'):
            pos = (pos[0], pos[1]-1)
        if(action == 'South'):
            pos = (pos[0], pos[1]+1)

        if(action == 'Unload'):
            order = customer[2]
            if pizzas > 0 and order > 0:
                    # Deliver all available pizzas
                    customer[2] = max(0, order - pizzas)
                    pizzas = max(0, pizzas - order)
        if(action == 'Load' and pizzas < self.MAXBAGS):
            pizzas += 1

        return (pos, pizzas, tuple(customer))


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        customer = state[2]
        pos = state[0]
        goal = self.GOAL[0]
        pizzas = state[1]
        allDelivered = customer[2] == 0 and pos[0] == goal[0] and pos[1] == goal[1] and pizzas == 0

        if allDelivered:
            print("Reached goal!")

        return allDelivered

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        if action in ('West','North','East','South'):
            return self.getAttribute(state2[0], 'cost')
        elif action in ('Load', 'Unload'):
            return 1

        # In case something goes wrong
        return 9223372036854775807

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        pos = state[0]
        goal = (state[2][0], state[2][1])
        order = state[2][2]
        pizzas = state[1]

        h = 0

        if order > 0:
            distX = math.fabs(pos[0] - goal[0])
            distY = math.fabs(pos[1] - goal[1])

            h = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))

            h += math.fabs(order - pizzas)
        else:
            distX = math.fabs(pos[0] - goal[0])
            distY = math.fabs(pos[1] - goal[1])

            h = math.sqrt(math.pow(distX, 2) + math.pow(distY, 2))

        return h


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

        # Initialize self.SHOPS with pizza shops data
        self.SHOPS = self.POSITIONS['pizza']
        customer = ()
        self.MAXBAGS = self.CONFIG['maxBags']

        # Add customer to state with its order size
        for x in xrange(self.CONFIG['map_size'][0]):
            for y in xrange(self.CONFIG['map_size'][1]):
                if self.getAttribute((x,y), 'unload'):
                    customer = (x, y, self.getAttribute((x,y), 'objects'))
                    break

        ''' ((X, Y), pizzas, orders)'''
        initial_state = (self.AGENT_START, 0, customer)
        final_state = (self.AGENT_START, 0, (customer[0], customer[1], 0))
        # breadth_first, depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
        algorithm = simpleai.search.depth_first

        self.GOAL = final_state

        return initial_state, final_state, algorithm

    def printState (self,state):
        '''Return a string to pretty-print the state '''

        pos = state[0]
        pizzas = state[1]
        customer = state[2]
        pps='\nPosition: {}, {}\nNo. pizzas carried: {}\nCustomer(s) waiting for delivery:\n'.format(pos[0], pos[1], pizzas)
        pps += '  ({}, {}): {} pizza(s)\n'.format(customer[0], customer[1], customer[2])
        return (pps)

    def getPendingRequests (self, state):
        ''' Return the number of pending requests in the given position (0-N). 
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        pos = state[0]
        customer = state[2]
        requests = None

        # Get the number of requests from the state
        if customer[0] == pos[0] and customer[1] == pos[1]:
            requests = customer[2]
                
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

