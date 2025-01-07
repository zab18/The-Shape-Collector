from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import sys

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

#human drawing properties
BASKET_WIDTH = 80
BASKET_HEIGHT = 20
basket_x = WINDOW_WIDTH // 2 - BASKET_WIDTH // 2
basket_y = 50  # Fixed y-position for the basket
basket_speed = 20

# Background color
background_color = [0.0, 0.0, 0.0, 1.0]  # Default: black (night mode)

# Shape properties
shapes = []  
shape_types = ["triangle", "circle", "square"]
shape_fall_speed = 4
new_shape_interval = 50  # interval between new shapes

# Game state
score = 0
frame_count = 0
round_target = random.randint(1, 10)  # Random number of shapes to collect (1-10)
current_target_shape = random.choice(shape_types)
missed_target_count = 0
wrong_shape_count = 0
MAX_MISSES = 3
MAX_WRONGS = 3
game_over_flag = False
level_complete_flag = False
circle_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)  # Center of the circle
circle_radius = 50


def init():
    glClearColor(*background_color)  
    glColor3f(1.0, 1.0, 1.0)  
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)



def spawn_shape():
    shape_type = random.choice(shape_types)
    x = random.randint(20, WINDOW_WIDTH - 20)
    y = WINDOW_HEIGHT
    shapes.append([shape_type, x, y])


def move_shapes():
    global shapes, score, missed_target_count, wrong_shape_count, game_over_flag, level_complete_flag

    for shape in shapes[:]:
        shape[2] -= shape_fall_speed  # Move shape down

        if is_caught(shape):
            shapes.remove(shape)
            if shape[0] == current_target_shape:
                score += 1
                if score >= round_target:
                    level_complete_flag = True
                    return
            else:
                wrong_shape_count += 1
                if wrong_shape_count >= MAX_WRONGS:
                    game_over("Collected wrong shape too many times!")
        elif shape[2] < basket_y and shape[0] == current_target_shape:
            shapes.remove(shape)
            missed_target_count += 1
            if missed_target_count >= MAX_MISSES:
                game_over("Missed too many target shapes!")


def is_caught(shape):
    x, y = shape[1], shape[2]
    return basket_y <= y <= basket_y + BASKET_HEIGHT and basket_x <= x <= basket_x + BASKET_WIDTH


def draw_human(x, y):
    """Draws a simple human shape at the given position."""
    # Head (circle)
    glColor3f(1.0, 0.8, 0.6)  # Skin tone
    glBegin(GL_POLYGON)
    for i in range(360):
        theta = i * math.pi / 180
        glVertex2f(x + 15 * math.cos(theta), y + BASKET_HEIGHT + 15 + 15 * math.sin(theta))
    glEnd()

    # Torso (rectangle)
    glColor3f(1.0, 0.08, 0.58)
    glBegin(GL_QUADS)
    glVertex2f(x - 10, y + BASKET_HEIGHT + 15)  # Top left
    glVertex2f(x + 10, y + BASKET_HEIGHT + 15)  # Top right
    glVertex2f(x + 10, y)  # Bottom right
    glVertex2f(x - 10, y)  # Bottom left
    glEnd()

    # Arms (lines)
    glColor3f(0.0, 0.0, 1.0)  # blue
    glBegin(GL_LINES)
    # Left arm
    glVertex2f(x - 10, y + BASKET_HEIGHT + 10)
    glVertex2f(x - 30, y + BASKET_HEIGHT + 5)
    # Right arm
    glVertex2f(x + 10, y + BASKET_HEIGHT + 10)
    glVertex2f(x + 30, y + BASKET_HEIGHT + 5)
    glEnd()

    # Legs (lines)
    glColor3f(0.0, 0.0, 1.0)  # Same as torso
    glBegin(GL_LINES)
    # Left leg
    glVertex2f(x - 5, y)
    glVertex2f(x - 15, y - 20)
    # Right leg
    glVertex2f(x + 5, y)
    glVertex2f(x + 15, y - 20)
    glEnd()

def draw_shapes():
    for shape in shapes:
        if shape[0] == "triangle":
            draw_triangle(shape[1], shape[2])
        elif shape[0] == "circle":
            draw_circle(shape[1], shape[2])
        elif shape[0] == "square":
            draw_square(shape[1], shape[2])


def draw_triangle(x, y):
    glColor3f(1.0, 0.0, 0.0)  # Red color
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x - 10, y - 20)
    glVertex2f(x + 10, y - 20)
    glEnd()


def draw_circle(x, y):
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glBegin(GL_POLYGON)
    for i in range(360):
        theta = i * math.pi / 180
        glVertex2f(x + 10 * math.cos(theta), y + 10 * math.sin(theta))
    glEnd()


def draw_square(x, y):
    glColor3f(0.0, 1.0, 1.0)  # Cyan color
    glBegin(GL_QUADS)
    glVertex2f(x - 10, y + 10)
    glVertex2f(x + 10, y + 10)
    glVertex2f(x + 10, y - 10)
    glVertex2f(x - 10, y - 10)
    glEnd()

def draw_arrow_circle(forward=True): 
    """Draws a circular arrow with a proper arrowhead."""
    xc, yc = circle_center
    r = circle_radius * 1.8  

    # outer circle
    glColor3f(0.0, 1.0, 0.0)  # Green color for the outer circle
    midpoint_circle(xc, yc, r)

    # circular arc
    glColor3f(1.0, 0.0, 0.0)  # Red color for the arrow arc
    glBegin(GL_LINE_STRIP)
    for angle in range(60, 300, 2):  # Arc segment for the arrow
        rad = math.radians(angle)
        glVertex2f(xc + math.cos(rad) * r * 0.6, yc + math.sin(rad) * r * 0.6)
    glEnd()

    # Arrowhead angles and positions
    arrow_tip_angle = 300   # Angle for the arrow tip
    arrow_width_angle = 25  # Half-angle for the arrowhead's width

    # Tip of the arrow
    arrow_tip_x = xc + math.cos(math.radians(arrow_tip_angle)) * r * 0.6
    arrow_tip_y = yc + math.sin(math.radians(arrow_tip_angle)) * r * 0.8

    # Base points of the arrowhead (left and right corners)
    arrow_base_left_x = xc + math.cos(math.radians(arrow_tip_angle - arrow_width_angle)) * r * 0.4
    arrow_base_left_y = yc + math.sin(math.radians(arrow_tip_angle - arrow_width_angle)) * r * 0.4

    arrow_base_right_x = xc + math.cos(math.radians(arrow_tip_angle + arrow_width_angle)) * r * 0.5
    arrow_base_right_y = yc + math.sin(math.radians(arrow_tip_angle + arrow_width_angle)) * r * 0.5

    #the arrowhead
    glColor3f(1.0, 0.0, 0.0)  # Red color for the arrowhead
    glBegin(GL_TRIANGLES)
    glVertex2f(arrow_tip_x, arrow_tip_y)  # Tip of the arrow
    glVertex2f(arrow_base_left_x, arrow_base_left_y)  # Left base point
    glVertex2f(arrow_base_right_x, arrow_base_right_y)  # Right base point
    glEnd()



def draw_next_round_arrow_circle():
    """Draws a green circle with a right-sided arrow inside."""
    xc, yc = circle_center
    r = circle_radius

    # outer circle
    glColor3f(0.0, 1.0, 0.0)  # Green color
    midpoint_circle(xc, yc, r)

    # arrow body
    glColor3f(0.2, 0.5, 0.8)  # color for the arrow
    glBegin(GL_LINES)
    glVertex2f(xc - r * 0.4, yc)  # Start of the arrow body
    glVertex2f(xc + r * 0.4, yc)  # End of the arrow body
    glEnd()

    # Calculation of arrowhead points
    arrow_tip_x = xc + r * 0.4
    arrow_tip_y = yc

    arrow_top_x = xc + r * 0.3
    arrow_top_y = yc + r * 0.1

    arrow_bottom_x = xc + r * 0.3
    arrow_bottom_y = yc - r * 0.1

    # the next round arrowhead
    glBegin(GL_TRIANGLES)
    glVertex2f(arrow_tip_x, arrow_tip_y)      # Tip of the arrow
    glVertex2f(arrow_top_x, arrow_top_y)      # Top of the arrowhead
    glVertex2f(arrow_bottom_x, arrow_bottom_y)  # Bottom of the arrowhead
    glEnd()


def midpoint_circle(xc, yc, r):
    x, y = 0, r
    d = 1 - r

    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(xc + x, yc + y)
        glVertex2f(xc - x, yc + y)
        glVertex2f(xc + x, yc - y)
        glVertex2f(xc - x, yc - y)
        glVertex2f(xc + y, yc + x)
        glVertex2f(xc - y, yc + x)
        glVertex2f(xc + y, yc - x)
        glVertex2f(xc - y, yc - x)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()


def is_mouse_in_circle(mx, my, cx, cy, r):
    distance = math.sqrt((mx - cx) ** 2 + (my - cy) ** 2)
    return distance <= r


def game_over(reason):
    global game_over_flag
    game_over_flag = True
    print(f"Game Over! {reason}")


def restart_game():
    global shapes, score, frame_count, round_target, current_target_shape
    global missed_target_count, wrong_shape_count, game_over_flag, level_complete_flag

    shapes = []
    score = 0
    frame_count = 0
    round_target = random.randint(1, 10)
    current_target_shape = random.choice(shape_types)
    missed_target_count = 0
    wrong_shape_count = 0
    game_over_flag = False
    level_complete_flag = False


def advance_round():
    global score, round_target, current_target_shape, missed_target_count, wrong_shape_count, level_complete_flag
    shapes.clear()
    score = 0
    round_target = random.randint(1, 10)
    current_target_shape = random.choice(shape_types)
    missed_target_count = 0
    wrong_shape_count = 0
    level_complete_flag = False

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if game_over_flag:
        glColor3f(0.3, 0.5, 0.8)
        glRasterPos2f(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 70)
        for char in "You've failed... Try again":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        draw_arrow_circle(forward=False)

    elif level_complete_flag:
        glColor3f(0.3, 0.5, 0.8)  # text color

        
        glRasterPos2f(WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 + 100)
        for char in "You've successfully completed the task.":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

       
        glRasterPos2f(WINDOW_WIDTH // 2 - 40, WINDOW_HEIGHT // 2 + 80)
        for char in "Next Round":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        # Draw the symbol (right-sided arrow in green circle)
        draw_next_round_arrow_circle()
    else:
        draw_human(basket_x + BASKET_WIDTH // 2, basket_y)  #human drawing
        draw_shapes()
        glColor3f(0.4, 0.3, 0.8)
        glRasterPos2f(10, WINDOW_HEIGHT - 20)
        for char in f"Score: {score} Target: {round_target} {current_target_shape}s":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        glRasterPos2f(10, WINDOW_HEIGHT - 40)
        for char in f"Missed: {missed_target_count}/{MAX_MISSES} Wrong: {wrong_shape_count}/{MAX_WRONGS}":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glutSwapBuffers()


def mouse_motion(button, state, x, y):
    global level_complete_flag, game_over_flag

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        mx, my = x, WINDOW_HEIGHT - y
        if game_over_flag and is_mouse_in_circle(mx, my, *circle_center, circle_radius):
            restart_game()
        elif level_complete_flag and is_mouse_in_circle(mx, my, *circle_center, circle_radius):
            advance_round()


def keyboard(key, x, y):
    global basket_x, background_color

    if key == b'\x1b':  # Escape key
        glutLeaveMainLoop()
    elif key == b'a':  # Move human left
        basket_x = max(basket_x - basket_speed, 0)
    elif key == b'd':  # Move human right
        basket_x = min(basket_x + basket_speed, WINDOW_WIDTH - BASKET_WIDTH)
    elif key == b'w':  # Day mode
        background_color = [0.8, 1.0, 1.0, 1.0]  # sky white
        glClearColor(*background_color)
    elif key == b'b':  # Night mode
        background_color = [0.0, 0.0, 0.0, 1.0]  # Regular black
        glClearColor(*background_color)


def update(value):
    global frame_count

    if not game_over_flag and not level_complete_flag:
        frame_count += 1
        if frame_count % new_shape_interval == 0:
            spawn_shape()

        move_shapes()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Shape Collector Game")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse_motion)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
