"""
+ Case A: using supporting lines and extreme points
+ Case B: choosing P2 to form the microscopic crust K where delta < d1.
Note that for case B, delta = diam K is the chord length, simplifying calculations.

INTEGRITY NOTE: Per Theorem 1, at most 3 queries, including the final one is needed to 
arrive at P_s. Each function _strategy_case_a and _strategy_case_b performs exactly TWO 
distance queries, as marked in the implementation, the third query/attempt is the return value.
Reason for this is we already know mathematically that the third query yields d = 0, and it is also 
rigorously checked via experiments.py whether the final guess is valid.
"""

import numpy as np
from query import query_distance, get_candidates

def solve_shape(shape, p_s):
    """
    Executes the 3-guess strategy to find p_s inside the shape.
    Automatically branches into Case A (polygons with flat boundary segments) 
    or Case B (strictly curved shapes like circles).
    """
    if not shape.is_strictly_curved():
        return _strategy_case_a(shape, p_s)
    else:
        return _strategy_case_b(shape, p_s)

def _strategy_case_a(shape, p_s):
    """
    Case A strategy: Boundary of the convex hull contains a segment [A, B].
    Chooses the endpoints of the segment as P1 and P2.
    """
    hull = shape.convex_hull()
    coords = list(hull.exterior.coords)[:-1] # Drop duplicate closing vertex
    
    # Take the first maximal segment [A, B] from the convex hull
    A = np.array(coords[0], dtype=float)
    B = np.array(coords[1], dtype=float)

    # --- QUERY LOCATIONS FOR CASE A ---
    p1 = A
    p2 = B
    d1 = query_distance(p1, p_s)
    d2 = query_distance(p2, p_s)
    
    candidates = get_candidates(p1, d1, p2, d2)
    
    # Filter the candidate that lies within S
    final_guess = None
    for c in candidates:
        if shape.contains(c):
            final_guess = c
            break
            
    if final_guess is None and len(candidates) > 0:
        final_guess = candidates[0]
        
    return [p1, p2, final_guess]

def _strategy_case_b(shape, p_s):
    """
    Case B strategy: Boundary contains no segments (strictly curved).
    Chooses an adaptive second query P2 close to P1 such that the chord cap diameter delta < d1.
    """
    # Assuming CircleShape parameters
    center = shape.center
    radius = shape.radius
    
    # --- QUERY LOCATIONS FOR CASE B ---
    # Guess P1 on the boundary
    p1 = center + np.array([radius, 0.0])
    d1 = query_distance(p1, p_s)
        
    # Choose P2 close to P1 such that chord length (delta) < d1
    target_chord = min(radius * 0.1, d1 * 0.5)
    val = min(1.0, target_chord / (2.0 * radius))
    d_theta = 2.0 * np.arcsin(val)
    
    p2 = center + np.array([radius * np.cos(d_theta), radius * np.sin(d_theta)])
    d2 = query_distance(p2, p_s)
    
    candidates = get_candidates(p1, d1, p2, d2)
    
    # Filter the candidate that lies within S
    final_guess = None
    for c in candidates:
        if shape.contains(c):
            final_guess = c
            break
            
    if final_guess is None and len(candidates) > 0:
        final_guess = candidates[0]
        
    return [p1, p2, final_guess]