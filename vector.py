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
    
    # to deal with precision issue --> quite strange though
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance
    
    # check if 2 vectors are Parallel
    def is_parallel_to(self, v):
        return(self.is_zero() or v.is_zero() or self.angel(v, True) ==0 or
               self.angel(v, True) == 180)
    
    
    # check if 2 vectors are Orthogonal  (dot products == 0)
    def orthogonal(self, v, tolerance = 1e-10):
         # abs is bulit in fucntion for absolute value
        if abs(self.inner_product(v)) < tolerance: 
            return True
        else:
            return False
        
    # calculate vector projections
    def vector_projections(self, baseVector):
        baseUnitVector = baseVector.unit()
        product_of_baseUnitVector_and_vector = self.inner_product(baseUnitVector)
        
        projection_vector = baseUnitVector.scalar(product_of_baseUnitVector_and_vector)
        return projection_vector
    
    # calculate v perp
    def vector_perp(self, baseVector):
        projection_vector = self.vector_projections(baseVector)
        prep_vector = self.minus(projection_vector)
        return prep_vector
        
      
              

# test code
vectorV1 = Vector([3.039, 1.879])
vectorB1 = Vector([0.825, 2.036])
vectorV2 = Vector([-9.88, -3.264, -8.159])
vectorB2 = Vector([-2.155, -9.353, -9.473])
vectorV3 = Vector([3.009, -6.172, 3.692, -2.51])
vectorB3 = Vector([6.404, -9.144, 2.759, 8.718])

print(vectorV1.vector_projections(vectorB1))
#print(vectorV2.vector_perp(vectorB2))
#print(vectorV3.vector_projections(vectorB3))
#print(vectorV3.vector_perp(vectorB3))


