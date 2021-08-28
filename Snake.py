from Vector2 import Vector2

class Snake:
    def __init__(self, size, spawnX, spawnY, boardSize):
        self.size = size
        self.boardSize = boardSize
        self.bodyCOs = [Vector2(spawnX-i,spawnY) for i in range(size)]
        self.head_direction = Vector2(-1,0)
        self.alive = True
        
    def get_head(self):
        return self.bodyCOs[self.size-1]
    
    def contains(self, point):
        for body in self.bodyCOs:
            if body==point:
                return True
        return False
    
    def die(self):
        self.alive=False
        #print('THE SNAKE HAS DIED')
    
    def move(self, direction, food_pos):
        moveLeft = True if direction[0]==1 else False
        moveRight = True if direction[1]==1 else False
        last_tail = last_tail = self.bodyCOs[0].clone()
        
        if moveLeft & moveRight:
            print('invalid command')
            return False,False,last_tail
        
        if self.can_die([moveLeft, moveRight]):
            self.die()
            return self.alive, False,last_tail
        
        caneat = self.can_eat(direction, food_pos)
        
        newHead, d = self.get_projected_pos([moveLeft, moveRight])
        self.bodyCOs.append(newHead)
        
        if not caneat:
            self.bodyCOs.pop(0)
        else:
            self.size+=1
        self.head_direction = d
        
        return self.alive, caneat, last_tail
            
    
    def get_projected_pos(self, direction):
        [left, right] = direction
        d = self.head_direction.clone()
        if left:
            d.rotate_left()
        elif right:
            d.rotate_right()
            
        head = self.get_head()        
        head = head+d
        return head,d
    
    def can_eat(self, direction, food_pos):
        head, d = self.get_projected_pos(direction)
        if head==food_pos:
            return True
        else:
            return False
        
    def can_die(self, direction):
        head, _ = self.get_projected_pos(direction)
        maxL = self.boardSize-1
        if head.x<0 or head.x>maxL or head.y<0 or head.y>maxL:
            return True
        elif self.contains(head):
            return True
        else:
            return False
            
            
