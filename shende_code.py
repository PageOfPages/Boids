from fractions import Fraction
import math
import random 
from collections import defaultdict
import numpy as np
from collections import namedtuple

# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator

Cluster = namedtuple("Cluster",["interval", "pos", "step"])

def potential(systm):
    """Computes a potential function that is always non-negative and zero at equilibrium
    """
    # diffs = [v for v in np.diff(systm) if v<=1.0]
    # return sum(diffs)


def neighborhood(config):
    """
    Args:
        config (dict): point-index -> position fraction
    Returns:
        (dict) point-index: (leftend, rightend) of point-indexes 
        of current neighbors
    """
    points = sorted(config.keys()) # assumed to be 1,2,...,n in sequence
    result = defaultdict(tuple)
    for pt in points:
        left_end = pt
        for i in reversed(range(1, pt)):
            if config[pt] - config[i] <= 1:
                left_end = i
            else:
                break
        right_end = pt
        for i in range(pt+1, len(points)+1):
            if config[i] - config[pt] <= 1:
                right_end = i
            else:
                break
        result[pt] = (left_end, right_end)
    return result

def hk_next_config(config):
    """Returns the next configuration

    Args:
        config (dict): point-index -> position fraction
    """
    curr_neigh = neighborhood(config)
    next_config = defaultdict(Fraction)
    for pt in config:
        left_end, right_end = curr_neigh[pt]
        posns = [config[i] for i in range(left_end, right_end+1)]
        next_config[pt] = sum(posns)/(right_end - left_end + 1)
    return next_config


def isclose(config1, config2):
    """Checks if config1 and config2 are close enough to be deemed equal
    Args:
        config1, config2 (dict): successive HK dynamics configurations
    """
    return all ([math.isclose(config1[pt], config2[pt]) for pt in config1])


def dumbbellHK(n):
    """Creates a dumbbell 
    The "bar" has n+1 >= 3 equally spaced points at 0, 1, ..., n 
    while the "bells" at each end have n points at distance 1/n 
    from the ends
    Args:
        n (int): n >= 2
    Returns:
        dictionary of point-indices and corresponding position fractions
    """
    d = defaultdict(Fraction)
    for pt in range(1, n+1):
        d[pt] = Fraction(-1, n)
    for pt in range(n+1, 2*n+2):
        d[pt] = Fraction(pt -(n+1), 1)
    for pt in range(2*n+2, 3*n+2):
        d[pt] = Fraction(n*n + 1, n)
    return d


# initial configurations uniformHk and randomHK
def uniformHK(n):
    return dict([(i, Fraction(i)) for i in range(1,n+1)])


# testing to get cluster change pattern of convergence 
def clusterHK(n, incrementTop, incrementBottom, group_size): 
    steps = uniformHK(n)
    for i in range(0,group_size):
        steps[i+1]+=Fraction(incrementTop).limit_denominator()
        steps[n-i]+=Fraction(incrementBottom).limit_denominator()
    
    return steps  

def exponentialHK(n, alpha): 
    steps = uniformHK(n)
    mid = math.ceil(n/2)
    for i in range(1,mid):
        steps[mid-i] = Fraction(steps[mid-i+1] - alpha**(i-1)).limit_denominator()
        steps[mid+i] = Fraction(steps[mid+i-1] + alpha**(i-1)).limit_denominator()
    
    return steps  

# def linearHK(n, incrementTop, incrementBottom, group_size): 
#     steps = uniformHK(n)
#     for i in range(0,group_size):
#         steps[i+1]+=Fraction(incrementTop).limit_denominator()
#         steps[n-i]+=Fraction(incrementBottom).limit_denominator()
    
#     return steps  
 
 
def randomHK(n):
    return dict(zip(range(n+1), sorted(random.uniform(1, n+1)
                                       for i in range(1,n+1))))


def simulate(init_system):
    """Determine HK dynamics of system
    Args:
        init_system (dict): initial configuration of agents
    """
    evolution = defaultdict(dict)
    step = 0
    evolution[step] = init_system
    while True: # update the system
        print('At step {}: \n'.format(step))
        for pt in evolution[step]:
            print('\tAgent {}: {:.3f} or {}'.format(pt,
                                                    float(evolution[step][pt]),
                                                    (evolution[step][pt])))
        step += 1
        evolution[step] = hk_next_config(evolution[step-1])
        print('Positions: ')
        if isclose(evolution[step], evolution[step-1]):
            break
    print('System took {} steps to converge!'.format(step-1))


def create_data(init_system):
    """Determine HK dynamics of system
    Args:
        init_system (dict): initial configuration of agents
    Returns: 
        2d numpy array of floats. Rows of agents and Columns of steps.
    """
    evolution = defaultdict(dict)
    step = 0
    evolution[step] = init_system
    # initializer 2d list 
    data = []
    # Populate the list (appending)
    while True: # update the system
        step_data = []  #Step column in a table of --> rows = agents and columns = steps
        for pt in evolution[step]:
            pt_val = float(evolution[step][pt])
            step_data.append(pt_val)
        data.append(step_data)
        step += 1
        evolution[step] = hk_next_config(evolution[step-1])
        if isclose(evolution[step], evolution[step-1]):
            break
    #steps_to_conv = format(step-1) # Not used. Steps can be determined by the amount of columns
    np_data = np.array(data).T
    print(np_data)   #commenting out so I can test collect_data
    return np_data

    #create another arr 


# ///////////////////////////////////////// TO DO ////////////////////////////////////////////

def collect_data(np_data):
    '''Collect HK dynamics of system 
    Args:
        data (numpy 2d array): final configuration of agents where 
                                rows = agents and columns = steps  
    Returns:
        List of steps_of_cluster (List of ints), cluster_pts (List of floats), 
        cluster_vals (List of lists of ints)
    '''
    all_clusters = []
    steps_of_cluster = []
    cluster_pts = []
    clustter_vals = []

    #use namedTuple to store interval, position, and step

    step = len(np_data[0])  #how many steps it takes for entire system to converge
    pts = len(np_data)  # n values

    for i in range(step):
        # t_pts = []
        # t_vals = []
        # t_all_pts = []
        # t_all_vals = []   // not used? maybe needed for storing

        start = 0
        end = 1
        while (end<pts):
            #contruct next cluster
            if np.isclose(np_data[start][i], np_data[end][i]):
                print(str(np_data[start][i]) + " and " + str(np_data[end][i]))
                print(str(start) + " and " + str(end))
                print("---------------")
                end+=1   # end += 1
                continue 
            ##we may have a new cluster at this point
            if start < (end-1): #more than one point in the cluster
                clusters = Cluster((start, end-1), np_data[start][i], i)
                #store somewhere !!!    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                print(clusters)
                # clusters = ((start, end-1), np_data[start][i], i)  #might need to fix this?? doesnt look right
                start = end + 1  #end = end + 1
                end = start + 1
            else: 
                start += 1
                end += 1

    #print(clusters)    
    # print("HELLO WE MADE IT!")        


# def check_neighbors():


'''Need an SQLite file for an all_data_table of all and a method to query users. 
    1. create all_data_table of n vs alpha
    2. query users for range of n and alpha to test
    3. If data in all_data_table does not exist, create. 
    4. create methods for user to query data
        a. query for all clusters for n 
        b. query for all clusters for a
        c. query for all clusters for n and a
'''
# ///////////////////////////////////////////////////////////////////////////////////////////


# Test Methods
if __name__ == '__main__':
    #simulate(uniformHK(20))
    # create_data(exponentialHK(5, 0.99))
    #simulanp_data[end][i]te(exponentialHK(11, 0.99))
    collect_data(create_data(exponentialHK(5, 0.99)))

