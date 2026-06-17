# this is a helper script to capture my own logs and test the LSTM from task 2
# saved in "datasets" folder, one level up

# Note: this script was written for personal use during data capture, so it intentionally lacks
# features like selecting a specific gesture to redo or discarding a bad sample mid-session.

import pyglet
import time
import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
task_1_dir = os.path.join(os.path.dirname(current_dir), 'task_1')
sys.path.append(task_1_dir)
from recognizer import Point

# the 16 gesture classes from the original dataset
GESTURE_CLASSES = [
    "arrow", "caret", "check", "circle", "delete_mark", "left_curly_brace",
    "left_sq_bracket", "pigtail", "question_mark", "rectangle",
    "right_curly_brace", "right_sq_bracket", "star", "triangle", "v", "x"
]

# IMPORTANT: I noticed that the logs have question_mark as one of the gestures, while the $1 recognizer has zig_zag instead
# I decided to capture question_mark logs, since the LSTM will be trained with that gesture, but then I'll have to exclude it
# when I compare the results vs. the $1 recognizer

REPS_PER_GESTURE = 10       
SUBJECT_NAME = "MartinaRobyCulasso" 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "datasets")

# state
current_gesture_index = 0
current_rep = 1  # index
current_stroke = []  
stroke_start_time = None

window = pyglet.window.Window(800, 600, caption="Gesture Capture")

instructions_label = pyglet.text.Label(
    "", x=15, y=560, color=(255, 255, 255, 255), font_size=18
)
progress_label = pyglet.text.Label(
    "", x=15, y=15, color=(180, 180, 180, 255), font_size=14
)


def update_labels():
    gesture_name = GESTURE_CLASSES[current_gesture_index]
    instructions_label.text = f"Draw: {gesture_name}  (rep {current_rep}/{REPS_PER_GESTURE})"
    progress_label.text = f"Gesture {current_gesture_index + 1}/{len(GESTURE_CLASSES)} | Press [C] to clear, [Q]/[ESC] to quit"


def save_gesture_xml(gesture_name, rep_number, points_with_time):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{gesture_name.replace(' ', '_')}{rep_number:02d}.xml"
    filepath = os.path.join(OUTPUT_DIR, filename)

    num_pts = len(points_with_time)
    total_ms = points_with_time[-1][1] if points_with_time else 0
    now = datetime.now()

    lines = ['<?xml version="1.0" encoding="utf-8" standalone="yes"?>']
    lines.append(
        f'<Gesture Name="{gesture_name}{rep_number:02d}" Subject="{SUBJECT_NAME}" '
        f'Speed="medium" Number="{rep_number}" NumPts="{num_pts}" '
        f'Millseconds="{total_ms}" AppName="GestureInput" AppVer="1.0" '
        f'Date="{now.strftime("%A, %B %d, %Y")}" TimeOfDay="{now.strftime("%I:%M:%S %p")}">'
    )
    for point, t_ms in points_with_time:
        lines.append(f'  <Point X="{int(point.x)}" Y="{int(point.y)}" T="{t_ms}" />')
    lines.append('</Gesture>')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Saved {filepath}")


@window.event
def on_key_press(key, modifiers):
    if key == pyglet.window.key.ESCAPE or key == pyglet.window.key.Q:
        pyglet.app.exit()
    if key == pyglet.window.key.C:
        current_stroke.clear()
        instructions_label.color = (255, 255, 255, 255)


@window.event
def on_mouse_press(x, y, button, modifiers):
    global stroke_start_time
    current_stroke.clear()
    stroke_start_time = time.time()
    y_flipped = window.height - y  # match recognizer's coordinate convention
    current_stroke.append((Point(x, y_flipped), 0))


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    elapsed_ms = int((time.time() - stroke_start_time) * 1000)
    y_flipped = window.height - y
    current_stroke.append((Point(x, y_flipped), elapsed_ms))


@window.event
def on_mouse_release(x, y, button, modifiers):
    global current_gesture_index, current_rep

    if len(current_stroke) < 10:
        instructions_label.text = "Too short, try again!"
        return

    gesture_name = GESTURE_CLASSES[current_gesture_index]
    save_gesture_xml(gesture_name, current_rep, current_stroke)
    current_stroke.clear()

    current_rep += 1
    if current_rep > REPS_PER_GESTURE:
        current_rep = 1
        current_gesture_index += 1
        if current_gesture_index >= len(GESTURE_CLASSES):
            instructions_label.text = "All done! You can close the window."
            return

    update_labels()


@window.event
def on_draw():
    window.clear()

    if len(current_stroke) > 1:
        for i in range(1, len(current_stroke)):
            p1, _ = current_stroke[i - 1]
            p2, _ = current_stroke[i]
            pyglet.shapes.Line(
                p1.x, window.height - p1.y,
                p2.x, window.height - p2.y,
                thickness=2, color=(255, 255, 255)
            ).draw()

    instructions_label.draw()
    progress_label.draw()


update_labels()
pyglet.app.run()

