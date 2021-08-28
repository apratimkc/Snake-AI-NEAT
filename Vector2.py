import math
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def rotate_right(self):
        x = self.y
        y = -self.x
        self.x = x
        self.y = y
        
    def rotate_left(self):
        x = -self.y
        y = self.x
        self.x = x
        self.y = y
        
    def normalized(self):
        m = self.magnitude()
        v = Vector2(0, 0)
        if(m!=0):
            v.x = self.x/m
            v.y = self.y/m
        return v
        
    def sq_distance(self, o):
        sq_d = ((self.x-o.x)**2) + ((self.y-o.y)**2)
        return sq_d
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def dot(self, other):
        return ((self.x*other.x) + (self.y*other.y))
    
    def angle(self, other):
        # cos a = (u.v)/(|u|.|v|)
        cos_a = self.dot(other)/(self.magnitude() * other.magnitude())
        a = (math.acos(cos_a))
        return a
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __add__(self, o):
        return Vector2(self.x+o.x, self.y+o.y)
    
    def __sub__(self, o):
        return Vector2(self.x-o.x, self.y-o.y)
    
    def __mul__(self,_int):
        return Vector2(self.x*_int, self.y*_int)
    
    def __eq__(self, o):
        if self.x == o.x and self.y==o.y:
            return True
        else:
            return False
    
    def clone(self):
        v = Vector2(self.x,self.y)
        return v