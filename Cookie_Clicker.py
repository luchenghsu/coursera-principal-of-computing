"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_number_of_cookies = 0.0
        self._current_number_of_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)] 
        
        
    def __str__(self):
        """
        Return human readable state
        """  
        return "\nTime: " + str(self._current_time) + "\n" + "Current Cookies: " + str(self._current_number_of_cookies) + "\n" + "CPS: " + str(self._current_cps) + "\n" + "Total Cookies: " + str(self._total_number_of_cookies) + "\n" + "History (lenght: " + str(len(self.get_history())) + "): " + str(self.get_history())  
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_number_of_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.get_cookies() >= cookies:
            return 0.0
        return float(math.ceil((cookies - self.get_cookies())/self.get_cps()))
          
  
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        
        self._current_time += time
        self._current_number_of_cookies += self.get_cps() * time
        self._total_number_of_cookies += self.get_cps() * time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        
        if self.get_cookies() >= cost:
             
            self._current_number_of_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self.get_time(), item_name, cost, self._total_number_of_cookies))
              
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clone_build_info = build_info.clone()
    click_state = ClickerState()
    
    while click_state.get_time() <= duration:
        item = strategy(click_state.get_cookies(), click_state.get_cps(), click_state.get_history(), duration - click_state.get_time(), clone_build_info)
        
        if item == None: 
            break
            
        item_cost = clone_build_info.get_cost(item)    
        elapsed_time = click_state.time_until(item_cost)
        
        # If you would have to wait past the duration of the simulation to purchase the item, you should end the simulation.
        if click_state.get_time() + elapsed_time > duration:
            break
        
        click_state.wait(elapsed_time)
        click_state.buy_item(item, item_cost, clone_build_info.get_cps(item))    
        clone_build_info.update_item(item) 
     
    click_state.wait(duration - click_state.get_time())
  
    return click_state



def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"



def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    item_cost_dic = {}
    
    current_afforded = cookies + cps * time_left
    
    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost <= current_afforded:
            item_cost_dic[item_cost] = item
    
    if len(item_cost_dic) == 0:
        return None
    
    cheapest = min(item_cost_dic.keys())        
    
    return item_cost_dic[cheapest]

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    item_cost_dic = {}
    
    current_afforded = cookies + cps * time_left
    
    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost <= current_afforded:
            item_cost_dic[item_cost] = item
    
    if len(item_cost_dic) == 0:
        return None
    
    most_expensive = max(item_cost_dic.keys())        
    
    return item_cost_dic[most_expensive]

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    item_cost_dic = {}
    
    current_afforded = cookies + cps * time_left
    
    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost <= current_afforded:
            item_cps = build_info.get_cps(item)
            item_cost_dic[item_cps/item_cost] = item
    
    if len(item_cost_dic) == 0:
        return None
    
    best = max(item_cost_dic.keys())        
    
    return item_cost_dic[best]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

