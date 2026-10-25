"""
Run numerical tests to prove the 3 queries prediction
"""

import numpy as np
from shapely.geometry import Polygon
from shape import PolygonShape, CircleShape
from query import set_secret_point
from strategies import solve_shape

HIT_TOLERANCE = 1e-7
TRIALS = 10000

def run_experiment():
    print("==================================================")
    print(" Running 3-Guess Strategy Validation Suite")
    print("==================================================")
    
    # Define raw coordinate lists for an irregular, jagged multi-component shape (Case A)
    poly1_coords = [(0, 0), (0.8, 1.5), (1.2, 0.4), (2.5, 2.2), (3.0, 0.2), (1.5, -0.8)]
    poly2_coords = [(4.5, 0.5), (5.2, 2.8), (6.8, 1.0), (7.5, 3.2), (8.2, 0.0), (6.0, -1.2)]
    
    # PolygonShape handles building and unifying them internally
    polygons= PolygonShape([poly1_coords, poly2_coords])
    circle = CircleShape(center=(0, 0), radius=2.0)
    
    tests = [
        ("Polygon Shape (Case A)", polygons), 
        ("Circle Shape (Case B)", circle)
    ]
    
    for name, shape in tests:
        successes = 0
        max_guesses = 0
        
        for _ in range(TRIALS):
            # Sample hidden point and hide it in the query engine
            p_s = shape.sample_uniform()
            set_secret_point(p_s)
            
            # Execute solver without exposing p_s
            guesses = solve_shape(shape)
            max_guesses = max(max_guesses, len(guesses))
            
            # Verify final guess successfully hits p_s
            if np.linalg.norm(np.array(guesses[-1]) - np.array(p_s)) < HIT_TOLERANCE:
                successes += 1
        
        print(f"[{name}]")
        print(f"  - Success Rate : {successes}/{TRIALS}")
        print(f"  - Max Guesses  : {max_guesses} (Theorem limit: <= 3)")
        print("-" * 50)

if __name__ == "__main__":
    run_experiment()