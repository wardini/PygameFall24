
from level_objects import Point
import numpy as np


a = Point(10,10,"a")
b = Point(20,20,"b")
b.back_linked_point=a
b.new_slope(25,25)

print(a)
print(b)

print(b.spline_points)

c = b.spline_points - np.array([12,12])
print(c)
d = np.linalg.norm(c,axis=1)
print(d)
print("less than")
print(d[d<5])
e = np.argmin(d)
print(e,b.spline_points[e])
