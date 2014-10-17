# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PADDLE_VELOCITY = 4

ball_vel = [0,0]

paddle1_pos = []
paddle2_pos = []

paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global paddle1_pos
    global paddle2_pos
    
    paddle1_pos = [[0, HEIGHT / 2], [0, HEIGHT / 2 + PAD_HEIGHT]]
    paddle2_pos = [[WIDTH, HEIGHT / 2],[WIDTH, HEIGHT / 2 + PAD_HEIGHT]]
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    ball_vel[0] = random.randrange(120,240) // 60 
    ball_vel[1] = random.randrange(60,180) // 60
    
    if direction == RIGHT:
        ball_vel[1] = - ball_vel[1]
    else:
        ball_vel[1] = -ball_vel[1]
        ball_vel[0] = -ball_vel[0]
    
    return None

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    #canvas.draw_line([0, HEIGHT / 2], [PAD_WIDTH, HEIGHT / 2 + PAD_HEIGHT], PAD_WIDTH, "White")
    
    
    # update ball
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    
    ### Verify if ball hits the left or right gutter
    if ball_pos[0] <= PAD_WIDTH:
       score2 += 1
       spawn_ball(RIGHT)
    
    if ball_pos[0] >= (WIDTH - PAD_WIDTH):
        score1 += 1
        spawn_ball(LEFT)
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen     
    paddle1_pos[0][1] += paddle1_vel
    paddle1_pos[1][1] += paddle1_vel
    paddle2_pos[0][1] += paddle2_vel
    paddle2_pos[1][1] += paddle2_vel
    
    if paddle1_pos[0][1] <= 0:
        paddle1_pos = [[0,0],[0,PAD_HEIGHT]]
    if paddle1_pos[1][1] >= HEIGHT:
        paddle1_pos = [[0,HEIGHT-PAD_HEIGHT],[0,HEIGHT]]
        
    if paddle2_pos[0][1] <= 0:
        paddle2_pos = [[WIDTH,0],[WIDTH,PAD_HEIGHT]]
    if paddle2_pos[1][1] >= HEIGHT:
        paddle2_pos = [[WIDTH,HEIGHT-PAD_HEIGHT],[WIDTH,HEIGHT]]
        
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], 16, "White")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], 16, "White")

    ### Verify if ball hits paddle 1
    if ball_pos[0] - BALL_RADIUS <= 0:
        if paddle1_pos[0][1] <= ball_pos[1] <= paddle1_pos[1][1]:
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            else:
                ball_vel[0] -= 1             
            ball_vel[1] += 1
            ball_vel[0] = - ball_vel[0] 
            
    # Verify if ball hits paddle 2
    if ball_pos[0] + BALL_RADIUS >= WIDTH:
        if paddle2_pos[0][1] <= ball_pos[1] <= paddle2_pos[1][1]:
            if ball_vel[0] > 0:
                ball_vel[0] += 1
            else:
                ball_vel[0] -= 1  
            ball_vel[0] = - ball_vel[0]
    
    ## Draw scores
    canvas.draw_text(str(score1), [200,20], 24, "White")
    canvas.draw_text(str(score2), [400,20], 24, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = - PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = - PADDLE_VELOCITY
    else:
        return None
    
    return None
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP["down"]) or (key == simplegui.KEY_MAP["up"]):
        paddle2_vel = 0
    elif (key == simplegui.KEY_MAP["s"]) or (key == simplegui.KEY_MAP["w"]):
        paddle1_vel = 0
    else:
        return None
    
    return None

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
reset = frame.add_button('Reset', new_game)
