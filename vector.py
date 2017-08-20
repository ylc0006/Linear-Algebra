import math
from decimal import Decimal, getcontext

getcontext().prec =30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    # for printing 
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    # check if 2 vectors are same
    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    # method for vectors plus together
    def plus(self, v):
        new_coordinates = [x + y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # method for vectors minus
    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    # method for vector scale
    def scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    # calculate vector's magnitude
    def magnitude(self):
        magnitude = 0
        for i in range (0, self.dimension):
            magnitude += self.coordinates[i]**2
        magnitude = magnitude ** (Decimal(0.5))
        return magnitude
    
    # calcuate vector's unit vector (or its direction) (or normalize)
    def unit(self):
        if self.magnitude()==0:
            return "can not normalize zero vector"
        unit_vector = self.scalar(Decimal(1.0)/self.magnitude())
        #   unit_coordinates = [(1/self.magnitude())*x for x in self.coordinates]
        #return  Vector(unit_coordinates)
        return unit_vector
    
    # Inner produc or Dot prodcuts
    def inner_product(self, v):
        product =0
        inner_products = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        for i in range(0, len(inner_products)):
            product += inner_products[i]
        return product
    
    # calcuate angel between 2 vectors (defaulat in radians)
    def angel(self, v, in_degrees= False):
        if self.magnitude() == 0 or v.magnitude() ==0:
            return "can not compute an angel with zero vector"
        
        rad = math.acos(self.inner_product(v)/ (self.magnitude()*v.magnitude()))
        
        if in_degrees== False:
            return rad
        else:
            return math.degrees(rad)

# test code
vectorV1 = Vector([7.887, 4.138])
vectorW1 = Vector([-8.802, 6.776])
vectorV2 = Vector([-5.955, -4.904, -1.874])
vectorW2 = Vector([-4.496, -8.755, 7.103])
vectorV3 = Vector([3.183, -7.627])
vectorW3 = Vector([-2.668, 5.319])
vectorV4 = Vector([7.35, 0.221, 5.188])
vectorW4 = Vector([2.751, 8.259, 3.985])

print(vectorV1.inner_product(vectorW1))
print(vectorV2.inner_product(vectorW2))
print(vectorV3.angel(vectorW3))
print(vectorV4.angel(vectorW4, True))