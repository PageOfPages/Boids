""" Title: Boids
Author: Paige Arnold, 
Date: 8/11/2020
Given n amount of points. Points will continue 
to move to the Center of Mass until clusters converge
and there is no movement. """ 

import fractions

def neighbors(point, positions):
    """
    Args:
        point (int): a value in the range of 1 to the number of points
        positions (dict): gives you the current positions
    
    Returns:
        set [int]: the collection of neighbors of point
    """
    n = max(positions.keys())
    result = set([point])
    for i in reversed(range(1, point)):
        if positions[point] - positions[i] <= 1: 
            result.add(i)
        else:
            break 
    for i in range(point+1, n+1):
        if positions[i] - positions[point] <= 1:
            result.add(i)
        else:
            break
    return result

def runner(pts):
    """Runs the simulation of boids moving towards each other.

    runner first determines the distance between each point. Then it creates the points along a single,
    straight line. The points move towards the center of the boids in its range until they freeze. Then
    the value of each pont and the total number of timesteps in printed.

    Args:
        pts (): the points along the line (boids)

    """
        
    pd = 1 #initial distance between points at beginning of simulation (pd = "point distance")

    #create points. key is point name and value is point location on number line
    positions = {point:fractions.Fraction(point) for point in range(1,pts+1)}
    neighborhood = {point:neighbors(point, positions) for point in range

    #at time 1, endpoints move in pd/2
    timestep = 1
    positions[0], positions[pts-1] = pd/2, (pts-1-(pd/2))

    #create temporary dictionaries for new values and previous values
    temp_dict = positions.copy()
    last_dict = positions.copy()

    while(True):
        timestep+=1

        for pt in positions: 
            pt_values = positions[pt]
            total_pts = 1.0   
            for pt2 in positions:  
                if (abs(positions[pt]-positions[pt2]) <= pd) and pt!=pt2:
                    pt_values += positions[pt2]
                    total_pts+=1
            temp_dict[pt] = pt_values/total_pts 

        positions = temp_dict.copy()

        if notMoving(positions,last_dict):
            break
        
        last_dict = positions.copy()

    print (f"Given {pts} points, it will take {timestep} timesteps to get to the solution.\n")
    print (f"Solution: \n {positions}")


def notMoving(current, last):
    """Determines if current point is frozen.

    Uses the constant to determine if points are at the same value. If they are and have no other
    points in their range, they are frozen.

    Args:
        current (): current point
        last (): previous point

    Returns:
        bool: returns true if the current point is not moving

    """
    #collided_pts = list(set(points.values()))
    constant = 0.00001
    current = list(current.values())
    last = list(last.values())

    for i in range(len(current)):
        if abs(current[i] - last[i]) > constant:
            return False
    return True


#Test for 10 points
if __name__=="__main__":
    runner(11)
























# pd = 1 #initial distance between points at beginning of simulation (pd = "point distance")
# is_movement = True

# def runner(pts):
#     pd = 1.0 #initial distance between points at beginning of simulation (pd = "point distance")
#     is_movement = True

#     #create points. key is point name and value is point location on number line
#     p_dict = {point:float(point) for point in range(pts)}
#     t = 0
#     print(p_dict)

#     #create a temporary dictionary for new values
#     temp_dict = dict(p_dict)
#     while(t<3):
#         t+=1
#         #at time 1, endpoints move in pd/2
#         if t == 1:
#             p_dict[0], p_dict[pts-1] = pd/2, (pts-1-(pd/2))
#             print(str(p_dict))  
#         else:
#             for pt in p_dict:
#                 temp_pt = p_dict[pt]
#                 sum_of_pts = 1.0
#                 for pt2 in p_dict:
#                     if (abs(p_dict[pt]-p_dict[pt2]) <= pd) and pt!=pt2:
#                         # print(str(pt)+ "         " + str(pt2))
#                         temp_pt += p_dict[pt2]
#                         sum_of_pts += 1.0 
#                         print("At pt "+str(pt)+":"+str(p_dict[pt])+" And pt2 "+str(pt2)+":"+str(p_dict[pt2]))
#                 print(" The Math is " +str(temp_pt)+" / "+str(sum_of_pts)+" = "+str(temp_pt/sum_of_pts)+"\n")
#                 temp_dict[pt] = temp_pt/sum_of_pts
#                 # print(str(p_dict))
#                 # print(str(pt))
#                 # print(str(p_dict.keys()[p_dict.values().index(pt)]))
#                 if pt2 == t:
#                     print("HERE")
#                     p_dict = temp_dict
#             print("_____________________________________________________________")
#     print str(p_dict)

# runner(10)






#     # while(is_movement):
#     #     t+=1
#     #     #at time 1, endpoints move in pd/2
#     #     if t == 1:
#     #         p_dict[0], p_dict[pts-1] = 0.5, (pts-1.5)
#     #     #all other points follow formula
#     #     else:
#     #         for i in p_dict:
#     #             print(str(i))
#     #             is_movement = False
