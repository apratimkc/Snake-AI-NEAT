import pygame
import numpy as np
import time
import threading
from Vector2 import Vector2

class GameGUI():
    
    def __init__(self, boardSize, game):
        #Colors
        self.bg = (255, 227, 227)
        self.sc = (98, 131, 149)
        self.border = (38, 42, 83)
        self.bc = (255, 160, 160)

        # Intialize the pygame
        pygame.init()
        #cals
        self.boardSize = boardSize
        self.s_width = 1000
        self.s_height = 600
        self.gameWindowSize = 500
        self.cell_width = int(self.gameWindowSize/boardSize)
        self.cell_height = int(self.gameWindowSize/boardSize)
        
        self.screen = pygame.display.set_mode((self.s_width, self.s_height))
        self.game = game
        self.anim_time = 0.5
        
        self.txt_gen = 0
        self.txt_score = 0
        self.txt_high_score = 0
        self.last_snake_co = []
        self.offset = 20
        self.y_offset = (self.s_height - self.gameWindowSize)/2
        self.genome_struct_img = None
    
    def load_genome_struct_img(self, filename):
        img = pygame.image.load(filename)
        #img = pygame.transform.rotate(img, 90)
        img_h = img.get_rect().height
        img_w = img.get_rect().width
        scale = img_h/(self.s_height-self.offset)
        img_h = int(img_h/scale)
        img_w = int(img_w/scale)
        img = pygame.transform.scale(img, (img_w,img_h))
        self.genome_struct_img = img
        
    def DrawScreen(self):
        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen,self.bg,(self.offset,self.y_offset,self.gameWindowSize,self.gameWindowSize),2)
        pygame.draw.rect(self.screen,(125,125,125),(self.offset,self.y_offset,self.gameWindowSize,self.gameWindowSize),2)

        s = self.game
        for i in range(s.snake.size):
            x,y = self.game.grid.get_grid_co(self.game.snake.bodyCOs[i])

            x = (x * self.cell_width) + self.offset
            y = (y * self.cell_height) + self.y_offset
            
            pygame.draw.rect(self.screen,self.sc,(x+1,y+1,self.cell_width-1,self.cell_height-1))
            pygame.draw.rect(self.screen,self.border,(x+1,y+1,self.cell_width-1,self.cell_height-1),2)
        
        x,y = self.game.grid.get_grid_co(self.game.food)

        x = x * self.cell_width + (self.cell_width/2) + self.offset
        y = y * self.cell_height + (self.cell_height/2)+ self.y_offset
        pygame.draw.circle(self.screen,self.bc,(x,y), self.cell_height*0.4)
        pygame.draw.circle(self.screen,self.border,(x,y), self.cell_height*0.4,2)
        
        self.draw_stat()
        self.draw_genome_struct()
        #self.DrawGrid()
        #self.DrawNetwork()
        #self.DrawScore()
    
           
    def draw_stat(self):
        blue = (38, 42, 83)
        font = pygame.font.SysFont('consolas', 24) #freesansbold
        text = font.render(f"Generation: {self.txt_gen}    Score: {self.txt_score}    Best: {self.txt_high_score}", True, blue)
        textRect = text.get_rect()
        textRect.center = (self.offset+textRect.width/2, self.s_height-20)
        self.screen.blit(text, textRect)
        
    def draw_genome_struct(self):
        if self.genome_struct_img != None:
            left_len = self.gameWindowSize+self.offset*2
            right_len = self.s_width-left_len
            img_w = self.genome_struct_img.get_rect().width
            x = left_len + (right_len-img_w)/2
            y = (self.s_height - self.genome_struct_img.get_rect().height)/2
            if y<0:
                y = 0
            self.screen.blit(self.genome_struct_img,(x,y))
            
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        # if event.type == pygame.MOUSEBUTTONUP:
        #     game.pauseGame = not game.pauseGame
                
    
        self.DrawScreen()
        pygame.display.update()
        return True
        
    def close(self):
        pygame.quit()