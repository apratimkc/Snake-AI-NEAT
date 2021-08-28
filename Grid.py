#------------
# 0 1 2 3
# 4 5 6 7
# 8 9 9 0
# 0 0 0 0
#------------

class Grid:
    def __init__(self, size):
        self.size = size
        self.matrix = [[0]*self.size for _ in range(self.size)]
        
    def getValue(self, x, y):
        if x<0 or x>self.size-1 or y<0 or y>self.size-1:
            return 3 # WALL=3
        return self.matrix[self.size-y-1][x]
    
    def setValue(self, value, x, y):
        self.matrix[self.size-y-1][x] = value
        
    def get_grid_co(self,vec2):
        x = vec2.x
        y= vec2.y
        return self.size-y-1, x
        
    def reset(self):
        self.matrix = [[0]*self.size for _ in range(self.size)]
        
            