import pygame as pyg

pyg.init()

shutDownFlag = False

while not shutDownFlag:
    screen = pyg.display.set_mode((800, 600))
    
    for event in pyg.event.get():
        
        if event.type == pyg.QUIT:
            shutDownFlag = True