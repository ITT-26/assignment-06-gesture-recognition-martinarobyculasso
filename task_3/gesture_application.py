# application for task 3
# "Ghost Buster game"

import pyglet
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recognizer import DollarRecognizer, Point

# constants
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 600
DANGER_LINE_X = 100
GHOST_SCALE = 0.3
HEART_SCALE = 1.5
GHOST_MARGIN_TOP = 20
GHOST_MARGIN_BOTTOM = 20
# the player must draw the gesture in a specific area in the screen
DRAW_ZONE_WIDTH = 250
DRAW_ZONE_HEIGHT = 200
DRAW_ZONE_X = WINDOW_WIDTH - DRAW_ZONE_WIDTH
DRAW_ZONE_Y = 0
PANEL_WIDTH = DRAW_ZONE_WIDTH
DEATH_DISPLAY_TIME = 0.6  # seconds to show ghost_dead before removing
PANEL_COLOR = (58, 84, 73, 255)
DANGER_LINE_COLOR = (255, 0, 0, 180)
MIN_STROKE_LENGTH = 10
SCORE_THRESHOLD = 0.5
REQUIRED_GESTURES = {
    "rectangle",
    "pigtail",
    "caret",
}  # filter only these 3 gestures

# variables
current_stroke = []
game_state = "start_screen"  # "start_screen", "playing", "game_over", "freeze"
ghost_list = []
points = 0
lives = 3

# game window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Ghost Buster")

# recognizer object
recognizer = DollarRecognizer()


# ASSETS =======

# path for assets (background, game objects, sprite)
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
pyglet.resource.path = [assets_dir]
pyglet.resource.reindex()

# font
pyglet.font.add_file(os.path.join(assets_dir, "ChelseaMarket-Regular.ttf"))

# static background
background_img = pyglet.resource.image("background.jpg")
background = pyglet.sprite.Sprite(background_img, x=0, y=0)
background.scale_x = WINDOW_WIDTH / background_img.width
background.scale_y = WINDOW_HEIGHT / background_img.height

# enemy sprites
ghost_rectangle = pyglet.resource.image("ghost_rectangle.png")
ghost_pig = pyglet.resource.image("ghost_pigtail.png")
ghost_caret = pyglet.resource.image("ghost_caret.png")
ghost_dead = pyglet.resource.image("ghost_dead.png")
ghost_evil = pyglet.resource.image("ghost_evil.png")

# lives
heart_full_img = pyglet.resource.image("heart_full.png")
heart_empty_img = pyglet.resource.image("heart_empty.png")
heart_1 = pyglet.sprite.Sprite(
    heart_full_img, x=WINDOW_WIDTH - 100, y=WINDOW_HEIGHT - 40
)
heart_1.scale = HEART_SCALE
heart_2 = pyglet.sprite.Sprite(
    heart_full_img, x=WINDOW_WIDTH - 70, y=WINDOW_HEIGHT - 40
)
heart_2.scale = HEART_SCALE
heart_3 = pyglet.sprite.Sprite(
    heart_full_img, x=WINDOW_WIDTH - 40, y=WINDOW_HEIGHT - 40
)
heart_3.scale = HEART_SCALE

# LABELS =======

# score label
score_label_points = pyglet.text.Label(
    "0",
    font_size=16,
    font_name="Chelsea Market",
    color=(0, 0, 0, 255),
    x=WINDOW_WIDTH - 20,
    y=WINDOW_HEIGHT - 70,
    anchor_x="right",
)

score_label_text = pyglet.text.Label(
    "Score: ",
    font_name="Chelsea Market",
    font_size=16,
    color=(0, 0, 0, 255),
    x=WINDOW_WIDTH - 40,
    y=WINDOW_HEIGHT - 70,
    anchor_x="right",
)

# title and instructions
game_title_label = pyglet.text.Label(
    "Ghost Buster",
    font_size=48,
    font_name="Chelsea Market",
    color=(255, 255, 255, 255),
    x=WINDOW_WIDTH // 2,
    y=WINDOW_HEIGHT - 80,
    anchor_x="center",
    anchor_y="center",
)

instructions_label = pyglet.text.Label(
    "Draw the matching gesture in the box to banish each ghost!\nDon't let them cross the red line.",
    font_size=18,
    color=(255, 255, 255, 255),
    x=WINDOW_WIDTH // 2,
    y=WINDOW_HEIGHT - 160,
    anchor_x="center",
    anchor_y="center",
    multiline=True,
    width=700,
    align="center",
)

start_prompt_label = pyglet.text.Label(
    "Press [SPACE] to start, or 'Q'/[ESC] to quit",
    font_size=20,
    color=(0, 200, 0, 255),
    x=WINDOW_WIDTH // 2,
    y=80,
    anchor_x="center",
    anchor_y="center",
)

draw_here_label = pyglet.text.Label(
    "Draw here:",
    font_size=16,
    font_name="Chelsea Market",
    color=(0, 0, 0, 255),
    x=DRAW_ZONE_X + 65,
    y=DRAW_ZONE_Y + DRAW_ZONE_HEIGHT + 10,
    anchor_x="center",
    anchor_y="bottom",
)

# gesture reference image for start screen
gesture_ref_img = pyglet.resource.image("title_ghosts.png")
gesture_ref_sprite = pyglet.sprite.Sprite(gesture_ref_img)
gesture_ref_sprite.scale = 0.12
gesture_ref_sprite.x = WINDOW_WIDTH // 2 - gesture_ref_sprite.width // 2
gesture_ref_sprite.y = WINDOW_HEIGHT // 2 - gesture_ref_sprite.height // 2 - 30

# game over screen
game_over_label = pyglet.text.Label(
    "Game Over",
    font_size=48,
    font_name="Chelsea Market",
    color=(220, 30, 30, 255),
    x=WINDOW_WIDTH // 2,
    y=WINDOW_HEIGHT // 2 + 60,
    anchor_x="center",
    anchor_y="center",
)

final_score_label = pyglet.text.Label(
    "",
    font_size=24,
    font_name="Chelsea Market",
    color=(255, 255, 255, 255),
    x=WINDOW_WIDTH // 2,
    y=WINDOW_HEIGHT // 2 - 15,
    anchor_x="center",
    anchor_y="center",
)

restart_prompt_label = pyglet.text.Label(
    "Press 'R' to restart, or 'Q'/[ESC] to quit",
    font_size=18,
    color=(0, 200, 0, 255),
    x=WINDOW_WIDTH // 2,
    y=80,
    anchor_x="center",
    anchor_y="center",
)

# CLASSES =======


class Ghost:
    def __init__(self, type, y_pos, speed):
        self.type = type
        self.y_pos = y_pos
        self.speed = speed
        self.crossed_danger = False
        self.dying = False
        self.dead_timer = 0.0

        if type == "rectangle":
            img = ghost_rectangle
        elif type == "pigtail":
            img = ghost_pig
        elif type == "caret":
            img = ghost_caret
        self.sprite = pyglet.sprite.Sprite(img, x=WINDOW_WIDTH - PANEL_WIDTH, y=y_pos)
        self.sprite.scale = GHOST_SCALE

    def draw(self):
        self.sprite.draw()

    def update_pos(self, dt):
        if self.dying:
            self.dead_timer += dt
        else:
            self.sprite.x -= self.speed * dt

    def kill(self):
        self.dying = True
        self.sprite.image = ghost_dead


# FUNCTIONS =======


def create_obstacle(dt):
    if game_state != "playing":
        return

    ghost_type = random.choice(list(REQUIRED_GESTURES))
    ghost_y = random.randint(
        GHOST_MARGIN_BOTTOM, WINDOW_HEIGHT - GHOST_MARGIN_TOP - 100
    )
    ghost_speed = random.randint(40, 100)  # not so fast to allow drawing time

    ghost = Ghost(ghost_type, ghost_y, ghost_speed)
    ghost_list.append(ghost)


def show_game_over(dt):
    global game_state
    game_state = "game_over"
    final_score_label.text = f"Final Score: {points}"


def update_lives():
    if lives == 3:
        heart_3.image = heart_full_img
        heart_2.image = heart_full_img
        heart_1.image = heart_full_img
    elif lives == 2:
        heart_3.image = heart_empty_img
    elif lives == 1:
        heart_3.image = heart_empty_img
        heart_2.image = heart_empty_img
    elif lives <= 0:
        heart_3.image = heart_empty_img
        heart_2.image = heart_empty_img
        heart_1.image = heart_empty_img


def update_score():
    score_label_points.text = str(points)


def kill_closest_ghost(gesture_name):
    global points
    matching = [g for g in ghost_list if g.type == gesture_name and not g.dying]
    if not matching:
        return
    target = min(matching, key=lambda g: g.sprite.x)
    target.kill()
    points += 1
    update_score()


def update(dt):
    global ghost_list, lives, game_state

    if game_state != "playing":
        return

    for ghost in ghost_list:
        ghost.update_pos(dt)

    survivors = []
    for ghost in ghost_list:
        if ghost.dying:
            if ghost.dead_timer < DEATH_DISPLAY_TIME:
                survivors.append(ghost)
            continue

        ghost_center_x = ghost.sprite.x + ghost.sprite.width / 2
        if ghost_center_x <= DANGER_LINE_X and not ghost.crossed_danger:
            ghost.crossed_danger = True
            lives -= 1
            update_lives()
            ghost.sprite.image = ghost_evil
            if lives <= 0:
                game_state = "freeze"
                pyglet.clock.schedule_once(show_game_over, 1.0)

        if ghost.sprite.x > -ghost.sprite.width:
            survivors.append(ghost)

    ghost_list = survivors


def in_draw_zone(x, y):
    return (
        DRAW_ZONE_X <= x <= DRAW_ZONE_X + DRAW_ZONE_WIDTH
        and DRAW_ZONE_Y <= y <= DRAW_ZONE_Y + DRAW_ZONE_HEIGHT
    )


def reset():
    global lives, points, game_state, ghost_list

    lives = 3
    points = 0
    ghost_list = []
    update_lives()
    update_score()
    game_state = "playing"


# PYGLET =======


@window.event
def on_mouse_press(x, y, button, modifiers):
    if game_state != "playing" or not in_draw_zone(x, y):
        return
    current_stroke.clear()
    current_stroke.append(Point(x, window.height - y))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if game_state != "playing" or not current_stroke:
        return
    current_stroke.append(Point(x, window.height - y))


@window.event
def on_mouse_release(x, y, button, modifiers):
    if game_state != "playing" or len(current_stroke) < MIN_STROKE_LENGTH:
        current_stroke.clear()
        return

    result = recognizer.Recognize(current_stroke, True)
    current_stroke.clear()

    if result.score >= SCORE_THRESHOLD and result.name in REQUIRED_GESTURES:
        kill_closest_ghost(result.name)


@window.event
def on_key_press(key, modifiers):
    global game_state

    if key == pyglet.window.key.ESCAPE or key == pyglet.window.key.Q:
        pyglet.app.exit()

    if key == pyglet.window.key.SPACE and game_state == "start_screen":
        reset()

    if key == pyglet.window.key.R and game_state == "game_over":
        reset()


@window.event
def on_draw():
    window.clear()
    background.draw()

    if game_state == "playing" or game_state == "freeze":
        for ghost in ghost_list:
            ghost.draw()

        # side panel
        pyglet.shapes.Rectangle(
            WINDOW_WIDTH - PANEL_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT, color=PANEL_COLOR
        ).draw()

        heart_1.draw()
        heart_2.draw()
        heart_3.draw()
        score_label_text.draw()
        score_label_points.draw()

        # draw zone on top of the panel
        pyglet.shapes.Rectangle(
            DRAW_ZONE_X,
            DRAW_ZONE_Y,
            DRAW_ZONE_WIDTH,
            DRAW_ZONE_HEIGHT,
            color=(0, 0, 0, 255),
        ).draw()

        draw_here_label.draw()

        pyglet.shapes.Line(
            DANGER_LINE_X,
            0,
            DANGER_LINE_X,
            WINDOW_HEIGHT,
            thickness=5,
            color=DANGER_LINE_COLOR,
        ).draw()

        # live stroke feedback
        if len(current_stroke) > 1:
            for i in range(1, len(current_stroke)):
                p1 = current_stroke[i - 1]
                p2 = current_stroke[i]
                pyglet.shapes.Line(
                    p1.x,
                    window.height - p1.y,
                    p2.x,
                    window.height - p2.y,
                    thickness=2,
                    color=(255, 255, 255),
                ).draw()

    elif game_state == "start_screen":
        pyglet.shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=(0, 0, 0, 130)
        ).draw()
        game_title_label.draw()
        instructions_label.draw()
        gesture_ref_sprite.draw()
        start_prompt_label.draw()

    elif game_state == "game_over":
        pyglet.shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, color=(0, 0, 0, 130)
        ).draw()
        game_over_label.draw()
        final_score_label.draw()
        restart_prompt_label.draw()


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.clock.schedule_interval(create_obstacle, 2)

pyglet.app.run()
