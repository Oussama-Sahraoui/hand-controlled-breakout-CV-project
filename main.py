import pygame
import sys
import os
import cv2
import mediapipe as mp
import threading


mp_hands = mp.solutions.hands.Hands()  # set up media pipe to detect hands
mp_drawing = mp.solutions.drawing_utils

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 600, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CV pong game by angrwolfjr/oussama')

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()
player_1 = pygame.image.load(os.path.join('assets/player.png')) #load the images of player
ball = pygame.image.load(os.path.join('assets/ball.png'))   #and ball
ball_rect=ball.get_rect()  #get the rect of the ball for collision detection
player_1_rect=player_1.get_rect() #same thing
direction="l"  #init some values
boxes=[]
blue=(0,0,255)
red=(255,0,0)
green=(0,255,0)
yellow=(255,255,0)

class box:   #define a class for boxes
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
defaultx=5   #creating the boxes that we'll break
fx=defaultx
fy=10
stepx=50
stepy=30
num=12
for i in range(3):
    for i in range(num):
        boxes.append(box(fx,fy,blue))
        fx+=stepx
    fx=defaultx
    fy+=stepy
    for i in range(num):
        boxes.append(box(fx,fy,red))
        fx+=stepx
    fx=defaultx
    fy+=stepy
    for i in range(num):
        boxes.append(box(fx,fy,green))
        fx+=stepx
    fx=defaultx
    fy+=stepy
    for i in range(num):
        boxes.append(box(fx,fy,yellow))
        fx+=stepx
    
    
    
    



bx=280 #init value of ball 
by=600
xd="left" #init direction of ball
yd="up"
p1x,p1y,p2x,p2y=260,775,260,25 #init player position

running = True
def player_move(direction): #function to move the player
    global p1x,p2x
    if direction=="left" and p1x>0:
        p1x-=3
    elif direction=="right" and p1x<550:
        p1x+=3
    else:
        return
    
        
def ball_move(): #function to move the ball
    global bx,by,xd,yd
    if bx<0:
        xd="right"
    elif bx>575:
        xd="left"
    if by<0:
        yd="down"
    elif by>775:
        yd="up"
    if xd=="right":
        bx+=3
    else:
        bx-=3
    if yd=="up":
        by-=3
    else:
        by+=3
    
def hand_input(): #function that detects which side of the screen your hand is on
    global direction #and changes the direction var
    while True:
        clock.tick(60)   
        success, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(frame_rgb)
        hand_landmarks = results.multi_hand_landmarks
        if hand_landmarks:
            for hand_lm in hand_landmarks:
                x_min, = 2000, 
                x_max, = -100, 
                for lm in hand_lm.landmark:
                    x = int(lm.x * frame.shape[1] )
                    x_min = min(x_min, x) 
                    x_max = max(x_max, x)
            
                if x_max<0: #logic to check which side the hand is on
                    direction="else"
                if (x_min+x_max/2)<415:
                    direction="left"
                else:
                    direction="right"
    
thread = threading.Thread(target=hand_input)
#I kept tha game and hand detection on seperate
#threads to make sure the game runs faster
thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    
                
            
    
    screen.fill((255, 255, 255))
    
        
    ball_rect.topleft=(bx,by)
    player_1_rect.topleft=(p1x,p1y)
    for i in range(0,len(boxes)):
        rect=pygame.Rect(boxes[i].x, boxes[i].y, 40,20) #for collision
        pygame.draw.rect(screen, boxes[i].color, pygame.Rect(boxes[i].x, boxes[i].y, 40,20)) #draw rect
        if ball_rect.colliderect(rect): #when the ball collides with a box, we pop it
            boxes.pop(i)                #from the array
            yd="down"               
            break
        for j in range(4):
            pygame.draw.rect(screen, (0,0,0), (boxes[i].x-j,boxes[i].y-j,45,25), 1) #drawing borders around each
            #box
       


    if ball_rect.colliderect(player_1_rect): #collision with the the player
        yd="up"

    

        
        
   
    player_move(direction) #calling the move function
    screen.blit(ball, (bx, by))
    screen.blit(player_1, (p1x, p1y))
    ball_move()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
