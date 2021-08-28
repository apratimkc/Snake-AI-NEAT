from Grid import Grid
from Snake import Snake
from Vector2 import Vector2
import random
import time
import math
from Game_GUI import GameGUI

class SnakeGame:
    def __init__(self, size):
        self.size = size
        self.grid = Grid(size)
        self.snake = Snake(3, size//2, size//2, size)
        self.food = Vector2(0,0)
        self.generate_food()
        self.init_grid()
        self.score = 0
        self.steps = 0
        self.lazySteps = 0
        self.cum_reward = 0
        self.last_food_dist = size*2
        #Reward Parameters
        self.roaming_reward = 1
        self.go_away_reward = -1.5
        self.food_reward = 10
        self.endGame = False
               
    def generate_food(self):
        while True:
            x = random.randint(0,self.size-1)
            y = random.randint(0,self.size-1)
            food = Vector2(x,y)
            if self.snake.contains(food)==False:
                break
        self.food = food
        
    def get_food_dir(self):
        #in format [R L U D]
        head = self.snake.get_head()
        diff = self.food - head
        return self.one_hot_code_dir(diff)
    
    def get_food_angle(self):
        head_dir = self.snake.head_direction
        food_dir = self.food - self.snake.get_head()
        return head_dir.angle(food_dir)
    
    def get_head_dir(self):
        return self.one_hot_code_dir(self.snake.head_direction)
    
    def one_hot_code_dir(self, dirV):
        res = [0,0,0,0] #in format [R L U D]     
        dirV = dirV.normalized()

        abs_x = abs(dirV.x)
        abs_y = abs(dirV.y)
        
        if abs_x>abs_y:
            if dirV.x >0:
                res[0]=1
            else:
                res[1]=1
        else:
            if dirV.y>0:
                res[2]=1
            else:
                res[3]=1

        return res
    
    def init_grid(self):
        self.grid.reset()
        for c in self.snake.bodyCOs:
            self.grid.setValue(2,c.x,c.y)
        self.grid.setValue(1,self.food.x,self.food.y)
        
    def update_grid(self, last_tail, eaten):
        self.grid.setValue(2, self.snake.get_head().x, 
                           self.snake.get_head().y)
        if eaten:
            self.grid.setValue(1,self.food.x,self.food.y)
        else:
            self.grid.setValue(0, last_tail.x, last_tail.y)
        
        
    def step(self, move):
        done, eaten = self.make_move(move)
        new_inputs = self.get_observation()
        reward = self.reward_calc(eaten)
        return new_inputs, reward, done
             
    def make_move(self, direction):
        alive, eaten, last_tail = self.snake.move(direction, self.food)
        self.steps +=1
        self.lazySteps += 1
        
        if eaten:
            self.score +=1
            self.lazySteps = 0
            self.generate_food()
        
        self.endGame = not alive
        if self.lazySteps > 100:
            self.endGame = True
        
        self.update_grid(last_tail, eaten)
        
        return self.endGame, eaten
    
    def reward_calc(self, eaten):
        return 1 if eaten else 0
        # r = 0
        # dist_food = self.food.sq_distance(self.snake.get_head())
        # if eaten:
        #     r = self.food_reward
        # else:
        #     if dist_food<self.last_food_dist:
        #         r = self.roaming_reward
        #     else:
        #         r = self.go_away_reward
        # self.last_food_dist = dist_food
        # return r
       
        
    def get_observation(self):
        obs_a = [0 for _ in range(8)]
        obs_b = [0 for _ in range(8)]
        origin = self.snake.get_head()
        for a in range(0,360,45):
            x = round(math.cos(math.radians(a)))
            y = round(math.sin(math.radians(a)))
            z = a//45
            val = self.scan(origin, Vector2(x,y), 5)
            # val = 0 for nothing, 1 for Food, 2 for Body, 3 for wall
            if val==1:
                obs_a[z]= 1
            elif val==2 or val==3:
                obs_b[z]= 1
        
        snake_head = self.snake.head_direction.clone()
        x_axis = Vector2(1,0)
        y_axis = Vector2(0,1)
        alpha = snake_head.angle(x_axis)
        beta = snake_head.angle(y_axis)
        if beta>(math.pi/2):
            alpha = (2*math.pi)-alpha

        rot_req = int(alpha//(math.pi/4))
        new_obs = obs_a[rot_req:]+ obs_a[:rot_req]+ obs_b[rot_req:]+ obs_b[:rot_req]

        return new_obs+ [self.get_food_angle()]
        
        
        #obs = obs + self.get_food_dir() + self.get_head_dir() + [self.get_food_angle()] 
        #return obs
    
    def auto_play(self, player, reward_calc, scan_dist, delay=0):
        endGame = False
        while endGame==False:
            move = player.get_move(self, scan_dist)
            endGame, eaten = self.make_move(move)
            food_dist = self.food.sq_distance(self.snake.get_head())
            self.cum_reward += reward_calc(food_dist, eaten)
            if delay>0:
               time.sleep(delay)
        return self.score, self.cum_reward
        
    def scan(self, origin, _dir, _range):
        for i in range(1,_range+1):
            p = origin + (_dir*i)
            if self.grid.getValue(p.x, p.y)!=0:
                return self.grid.getValue(p.x, p.y)
        return 0
    
    def __str__(self):
        txt = ''
        for i in range(self.size):
            for j in range (self.size):
                txt += str(self.grid.matrix[i][j])
            txt += '\n'
        return txt
        
# sgw = SnakeGame(10)
# print(sgw)
# import pickle
# with open('winner-feedforward', 'rb') as f:
#     c = pickle.load(f)

# print('Loaded genome:')
# print(c)

# while True:
#     print(sgw)
#     print(sgw.get_observation())
#     i = input('Input L, R, C, A :')
#     i = i.lower()
#     if i=='l':
#         sgw.make_move([1,0])
#     elif i =='r':
#         sgw.make_move([0,1])
#     elif i=='c':
#         sgw.make_move([0,0])
#     else:
#         break

# sg = SnakeGame(10)
# gui = GameGUI(10,sg)
# done = False
# while not done:
#     #print(sg)
#     gui.draw()
#     time.sleep(0.5)
#     action = [0,0,0]
#     rand_id = random.randint(0, 2)
#     action[rand_id] = 1
#     _, _, done = sg.step(action[0:2])
# gui.close()
    




