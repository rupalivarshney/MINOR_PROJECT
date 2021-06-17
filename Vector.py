#################################################################
#   Filename:   Vector.py
#   Desc:       This file contains 2D vector operations and helper
#               functions for mathematical operations
#
#################################################################
import operator
import math

class Vector(object):
    _cords_ = ['x', 'y']

    def __init__(self, x, y = None):
        if y == None:
            # we are having list or tuple of length 2
            self.x = x[0]; self.y = x[1];
        else:
            self.x = x; self.y = y;

    def normalize(self):
        """This function returns normalized length of vector"""
        length = self.length()
        if length != 0:
            return self* (1/length)

        return  Vector(self)

    def __nonzero__(self):
        return bool(self.x or self.y)

    def __len__(self):
        return 2

    def __neg__(self):
        return Vector(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vector(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vector(operator.abs(self.x), operator.abs(self.y))
        return Vector(operator.abs(self.x), operator.abs(self.y))

    # OPERATOR OVERLOADING
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)

        if hasattr(other, "__getitem__"):
            return Vector(self.x + other[0], self.y + other[1])
        else: return Vector(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)

        if hasattr(other, "__getitem__"):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y)

        if hasattr(other, "__getitem__"):
            return Vector(self.x * other[0], self.y * other[1])
        else: # scalar
            return Vector(self.x * other, self.y * other)

    def mul_vec_scalar(self, other):
            return Vector(self.x * other, self.y * other)

    def __div__(self, other):
        return self.binary_operation(other, operator.div)


    def __truediv__(self, other):  # used
        return self.binary_operator(other, operator.truediv)

    def __rtruediv__(self, other):
        return self.binary_operator_rightvector(other, operator.truediv)

    def length(self):
        return math.sqrt( (self.x)**2 + (self.y)**2)

    def distance(self, other):
        return math.sqrt( (self.x - other[0])**2 + (self.y - other[1])**2)


    def dot_product(self, other):
        return float(self.x * other[0] + self.y * other[1])

    def projection(self, other):
        len_sqr = other[0]*other[0] + other[1]*other[1]
        projected_len = self.dot_product(other)
        projected = other * (projected_len / len_sqr)
        return projected

    def perpendicular(self):
        return Vector(-self.y, self.x)

    def __getitem__(self, item):
        if item == 0: return  self.x
        elif item == 1: return self.y
        else: raise IndexError("Invalid index encounter " + str(item))

    def __gstitem__(self, item, value):
        if item == 0: self.x = value
        elif item == 1: self.y = value
        else: raise IndexError("Invalid index encounter " + str(item))

    def __repr__(self): return "Vector(%s, %s)" %(self.x, self.y)



    def binary_operator(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vector):
            return Vector(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vector(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vector(f(self.x, other),
                         f(self.y, other))

    def binary_operator_rightvector(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vector(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vector(f(other, self.x),
                         f(other, self.y))



    @staticmethod
    def Dot_product(another, other):
        return float(another.x * other[0] + another.y * other[1])


    @staticmethod
    def Projection(another, other):
        len_sqr = other[0] * other[0] + other[1] * other[1]
        projected_len = Vector.Dot_product(another, other)
        projected = other * (projected_len / len_sqr)
        return projected