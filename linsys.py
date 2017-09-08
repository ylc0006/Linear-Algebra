from decimal import Decimal, getcontext
from copy import deepcopy
from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        self[row1], self[row2] = self[row2], self[row1]
        ''' 
        tempPlane = self[row1] 
        self[row1] = self[row2]
        self[row2] = tempPlane
        '''
        


    def multiply_coefficient_and_row(self, coefficient, row):
        n = self[row].normal_vector
        new_normal_vector =[]
        for item in n:
            new_normal_vector.append(item * coefficient)
      
        new_constant_term = self[row].constant_term * coefficient
        self[row] = Plane(new_normal_vector, new_constant_term)
                      

    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        tempVector = [x * coefficient for x in self[row_to_add].normal_vector]
        tempPlane = Plane( tempVector , self[row_to_add].constant_term * coefficient)
        
        row_to_add_list = tempPlane.normal_vector
        row_to_be_added_to_list = self[row_to_be_added_to].normal_vector
        new_vector = [x + y for x, y in zip(row_to_add_list, row_to_be_added_to_list)]
        self[row_to_be_added_to].normal_vector = new_vector
        
        new_constant_term = self[row_to_be_added_to].constant_term + tempPlane.constant_term
        self[row_to_be_added_to].constant_term = new_constant_term
        
                   


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


'''
# code for playing 
p0 = Plane([1, 1, 1], 1)
p1 = Plane([0, 1, 0], 2)
p2 = Plane([1, 1, -1], 3)
p3 = Plane([1, 0, -2], 2)

s = LinearSystem([p0,p1,p2,p3])


print (s.indices_of_first_nonzero_terms_in_each_row())
print ('{},{},{},{}'.format(s[0],s[1],s[2],s[3]))
print (len(s))
print (s)
'''

# Test code
p1 = Plane([1,1,1], constant_term=1)
p2 = Plane([0,1,1], constant_term=2)
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print ('test case 1 failed')

p1 = Plane([1,1,1], constant_term=1)
p2 = Plane([1,1,1], constant_term=2)
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term=1)):
    print ('test case 2 failed')

p1 = Plane([1,1,1], constant_term=1)
p2 = Plane([0,1,0], constant_term=2)
p3 = Plane([1,1,-1], constant_term=3)
p4 = Plane([1,0,-2], constant_term=2)
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector([0,0,-2]), constant_term=2) and
        t[3] == Plane()):
    print ('test case 3 failed')

p1 = Plane([0,1,1], constant_term=1)
p2 = Plane([1,-1,1], constant_term=2)
p3 = Plane([1,2,-5], constant_term=3)
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane([1,-1,1], constant_term=2) and
        t[1] == Plane([0,1,1], constant_term=1) and
        t[2] == Plane([0,0,-9], constant_term=-2)):
    print ('test case 4 failed')











'''
# Test swap code
s.swap_rows(0,1)
print('test case 1',s)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 1 failed')

s.swap_rows(1,3)
print('test case 2',s)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print ('test case 2 failed')

s.swap_rows(3,1)
print('test case 3',s)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 3 failed')


# Test multiply coefficient and row code
s.multiply_coefficient_and_row(1,0)
print('test case 4',s)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print ('test case 4 failed')

s.multiply_coefficient_and_row(-1,2)
print('test case 5', s)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane([-1,-1,1], constant_term= -3) and
        s[3] == p3):
    print ('test case 5 failed')


s.multiply_coefficient_and_row(10,1)
print('test case 6', s)
if not (s[0] == p1 and
        s[1] == Plane([10,10,10], constant_term=10) and
        s[2] == Plane([-1,-1,1], constant_term=-3) and
        s[3] == p3):
    print ('test case 6 failed')



# Test multiple times row to row code
s.add_multiple_times_row_to_row(0,0,1)
print('test case 7', s)
if not (s[0] == p1 and
        s[1] == Plane([10,10,10], constant_term=10) and
        s[2] == Plane([-1,-1,1], constant_term=-3) and
        s[3] == p3):
    print ('test case 7 failed')

s.add_multiple_times_row_to_row(1,0,1)
print('test case 8', s)
if not (s[0] == p1 and
        s[1] == Plane([10,11,10], constant_term=12) and
        s[2] == Plane([-1,-1,1], constant_term=-3) and
        s[3] == p3):
    print ('test case 8 failed')

s.add_multiple_times_row_to_row(-1,1,0)
print('test case 9', s)
if not (s[0] == Plane([-10,-10,-10], constant_term=-10) and
        s[1] == Plane([10,11,10], constant_term=12) and
        s[2] == Plane([-1,-1,1], constant_term=-3) and
        s[3] == p3):
    print ('test case 9 failed')
'''