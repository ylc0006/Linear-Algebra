from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector  # initial to set a normal vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term) # initial to set a value

        self.set_basepoint() # initial to run a function


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = Decimal(n[initial_index]) 

            basepoint_coords[initial_index] = c/initial_coefficient # becasue c is decimal, so initial_coefficient needs to be decimal
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
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
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1) # put value of i+1 into{}
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
    # determine if 2 lines are paralle 
    #(check if their normal vectors are parallel)
    def is_paralle_to(self, line):
        return Vector(self.normal_vector).is_parallel_to(Vector(line.normal_vector))
    
    # determine if 2 lines are equal 
    #(the vector connecting one point on each line is orthogonal to the line's normal vector)
    def __eq__(self, line):
       p1= self.basepoint
       p2= line.basepoint
       p2_p1_vector = p2.minus(p1)
       if p2_p1_vector.orthogonal(Vector(self.normal_vector)):
           return "same line"
       else:
           return "not the same line"
    
    # compute the intersection of 2 lines, or return some indication of no 
    # intersection / infinite intersections
    def intersect_with_at(self, line):
        A, B = self.normal_vector
        C, D = line.normal_vector
        k1 = self.constant_term
        k2 = line.constant_term
        # Ax + By = k1
        # Cx + Dy = k2       
        A = Decimal(A)
        B = Decimal(B)
        C = Decimal(C)
        D = Decimal(D)
        x =  (D*k1 - B*k2)/ (A*D- B*C)
        y = -(C*k1 - A*k2)/ (A*D- B*C)
        return [x, y]



    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable): # enumerate() get the content and index of list
                                            # item means coefficients of the line
                                            # k means the index
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
    
# test code
line1 = Line([4.046, 2.836], 1.21)
line2 = Line([10.115, 7.09], 3.025)
line3 = Line([7.204, 3.182], 8.68)
line4 = Line([8.172, 4.114], 9.883)
line5 = Line([1.182, 5.562], 6.744)
line6 = Line([1.773, 8.343], 9.525)
#line7 = Line([1.773, 8.343],"A")
print(line1.is_paralle_to(line2))
print(line3.is_paralle_to(line4))
print(line5.is_paralle_to(line6))
print(line1.__eq__(line2))
print(line5.__eq__(line6))
print(line3.intersect_with_at(line4))





    
