from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Plane(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector # initial to set a normal vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term) # initial to set a value

        self.set_basepoint() # initial to run a function


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Plane.first_nonzero_index(n)
            initial_coefficient = Decimal(n[initial_index])

            basepoint_coords[initial_index] = c/initial_coefficient  # becasue c is decimal, so initial_coefficient needs to be decimal
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Plane.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant) # put value of constant into {}

        return output
    # determine if 2 planes are paralle 
    #(check if their normal vectors are parallel)
    def is_paralle_to(self, plane):
        return Vector(self.normal_vector).is_parallel_to(Vector(plane.normal_vector))
       
    # determine if 2 planes are equal 
    #(the vector connecting one point on each plane is orthogonal to the plane's normal vector)
    def __eq__(self, plane):
       if Vector(self.normal_vector).is_zero():
           if Vector(plane.normal_vector).is_zero():
               return False
           else:
               diff = self.constant_term - plane.constant_term
               return MyDecimal(diff).is_near_zero()
       elif Vector(plane.normal_vector).is_zero():
           return False
       
       if not self.is_paralle_to(plane):
           return False
        
       p1= self.basepoint
       p2= plane.basepoint
       p2_p1_vector = p2.minus(p1)
       if p2_p1_vector.orthogonal(Vector(self.normal_vector)):
           return "same plane"
       else:
           return "not the same plane"
    
    


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

#Test cosde
plane1 = Plane([-0.412, 3.806, 0.728], -3.46)
plane2 = Plane([1.03, -9.515, -1.82], 8.65)
plane3 = Plane([2.611, 5.528, 0.283], 4.6)
plane4 = Plane([7.715, 8.306, 5.342], 3.76)
plane5 = Plane([-7.926, 8.625, -7.212], -7.952)
plane6 = Plane([-2.642, 2.875, -2.404], -2.443)

print(plane1.is_paralle_to(plane2))
print(plane3.is_paralle_to(plane4))
print(plane5.is_paralle_to(plane6))
print(plane1.__eq__(plane2))
print(plane5.__eq__(plane6))