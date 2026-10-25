"""
Core distance query engine
"""

import numpy as np

_current_p_s = None


def set_secret_point(p_s):
    """Sets the hidden secret point p_s for the current query session."""
    global _current_p_s
    _current_p_s = np.array(p_s, dtype=float)


def query_distance(p):
    """
    Returns the Euclidean distance between a query point p and the hidden point p_s,
    without requiring p_s to be passed explicitly.
    """
    if _current_p_s is None:
        raise ValueError("Secret point p_s has not been set. Call set_secret_point(p_s) first.")
    p = np.array(p, dtype=float)
    return np.linalg.norm(p - _current_p_s)


def intersect_circles(p1, r1, p2, r2):
    """
    Computes the intersection points of two circles (the mirror pair candidates).
    Given two guesses P1, P2 and their distance measurements d1, d2.
    """
    p1 = np.array(p1, dtype=float)
    p2 = np.array(p2, dtype=float)
    
    diff = p2 - p1
    d = np.linalg.norm(diff)
    
    if d > r1 + r2 or d < abs(r1 - r2) or (d == 0 and r1 == r2):
        return []
        
    u = diff / d
    n = np.array([-u[1], u[0]])
    
    a = (r1**2 - r2**2 + d**2) / (2.0 * d)
    h_sq = r1**2 - a**2
    h = np.sqrt(max(0.0, h_sq))
    
    p_mid = p1 + a * u
    if h == 0.0:
        return [p_mid]
        
    c1 = p_mid + h * n
    c2 = p_mid - h * n
    return [c1, c2]


def get_candidates(p1, d1, p2, d2):
    """
    Returns the mirror pair candidate points {P_s, sigma(P_s)} consistent with two distance queries.
    """
    return intersect_circles(p1, d1, p2, d2)