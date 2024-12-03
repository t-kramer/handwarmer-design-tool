# example of view factor computation between two rectangles using pyviewfactor
# can import meshes in STL format

import pyvista as pv
import pyviewfactor as pvf

# rectangle a
pointa = [0, 0, 0]
pointb = [0.07, 0, 0]
pointc = [0.07, 0.1, 0]
rectangle_a = pv.Rectangle([pointa, pointb, pointc])

# rectangle b
pointa = [0, 0, 0.1]
pointb = [0.12, 0, 0.1]
pointc = [0.12, 0.08, 0.1]
liste_pts = [pointa, pointb, pointc]
liste_pts.reverse()  # reverse normal
rectangle_b = pv.Rectangle(liste_pts)

# preliminary check for visibility
if pvf.get_visibility(rectangle_a, rectangle_b):
    F = pvf.compute_viewfactor(rectangle_a, rectangle_b)
    print("View factor from between rectangles = ", F)
else:
    print("Not facing each other")
