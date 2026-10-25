"""
The shapes that are used to demonstrate Case A and Case B strategy:
+ Polygon/Multi-polygon: flat segments on hull boundaries
+ A circle: the hull is the circle itself, having no flat segments
"""

import numpy as np
from abc import ABC, abstractmethod
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union

class Shape(ABC):
    @abstractmethod
    def contains(self, point):
        pass

    @abstractmethod
    def convex_hull(self):
        pass

    @abstractmethod
    def is_strictly_curved(self):
        pass

    @abstractmethod
    def sample_uniform(self, num_samples=1):
        pass


class PolygonShape(Shape):
    """
    Represents shapes with polygonal boundaries (single or multi-polygons).
    Always contains flat boundary convex hull segments, mapping to Case A.
    """
    def __init__(self, geometries):
        if isinstance(geometries, (Polygon, MultiPolygon)):
            self.geom = geometries
        else:
            polys = [Polygon(v) for v in geometries]
            self.geom = unary_union(polys)

    def contains(self, point):
        return self.geom.contains(Point(point))

    def convex_hull(self):
        return self.geom.convex_hull

    def is_strictly_curved(self):
        return False

    def sample_uniform(self, num_samples=1):
        minx, miny, maxx, maxy = self.geom.bounds
        samples = []
        while len(samples) < num_samples:
            p = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
            if self.geom.contains(p):
                samples.append([p.x, p.y])
        return samples[0] if num_samples == 1 else np.array(samples)


class CircleShape(Shape):
    """
    Represents a circular disk. 
    Demonstrates Case B natively because its boundary has zero flat segments.
    """
    def __init__(self, center=(0.0, 0.0), radius=1.0):
        self.center = np.array(center, dtype=float)
        self.radius = float(radius)

    def contains(self, point):
        return np.linalg.norm(np.array(point) - self.center) <= self.radius

    def convex_hull(self):
        return self

    def is_strictly_curved(self):
        return True

    def sample_uniform(self, num_samples=1):
        samples = []
        while len(samples) < num_samples:
            r = self.radius * np.sqrt(np.random.uniform(0, 1))
            theta = np.random.uniform(0, 2 * np.pi)
            p = self.center + np.array([r * np.cos(theta), r * np.sin(theta)])
            samples.append(p)
        return samples[0] if num_samples == 1 else np.array(samples)