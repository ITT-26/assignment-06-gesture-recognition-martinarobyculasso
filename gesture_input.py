# gesture input program for first task

import pyglet
from recognizer import DollarRecognizer, Point

# constants
MIN_STROKE_LENGTH = 10
SCORE_THRESHOLD = 0.3

# variables
current_stroke = []

# setup
window = pyglet.window.Window(800, 600, caption="$1 Gesture Recognizer")
recognizer = DollarRecognizer()

# labels
result_label = pyglet.text.Label(
    "Draw a gesture using your mouse/touchpad!",
    x=10,
    y=10,
    color=(255, 255, 255, 255),
    font_size=20,
)

gestures_title = pyglet.text.Label(
    "Available gestures:", x=15, y=560, color=(200, 200, 200, 255), font_size=16
)

gesture_names = [u.name for u in recognizer.Unistrokes]
gesture_labels = [
    pyglet.text.Label(
        f"- {name}", x=15, y=535 - i * 20, color=(180, 180, 180, 255), font_size=14
    )
    for i, name in enumerate(gesture_names)
]

commands_title = pyglet.text.Label(
    "Commands:", x=630, y=560, color=(200, 200, 200, 255), font_size=16
)

command_labels = [
    pyglet.text.Label(
        "- [C]: clear stroke", x=630, y=535, color=(180, 180, 180, 255), font_size=14
    ),
    pyglet.text.Label(
        "- [Q] or [ESC]: quit", x=630, y=515, color=(180, 180, 180, 255), font_size=14
    ),
]


@window.event
def on_key_press(key, modifiers):
    # close window with [ESC] or 'q'
    if key == pyglet.window.key.ESCAPE or key == pyglet.window.key.Q:
        pyglet.app.exit()
    # clear screen with 'c'
    if key == pyglet.window.key.C:
        current_stroke.clear()
        result_label.text = "Draw a gesture using your mouse/touchpad!"


@window.event
def on_close():
    pyglet.app.exit()


@window.event
def on_mouse_press(x, y, button, modifiers):
    current_stroke.clear()
    result_label.text = "Drawing..."


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    current_stroke.append(Point(x, y))


@window.event
def on_mouse_release(x, y, button, modifiers):
    if len(current_stroke) > 10:
        result = recognizer.Recognize(current_stroke, True)  # True to use Protractor
        if result.score >= SCORE_THRESHOLD:
            result_label.text = f"Gesture: {result.name} | Score: {result.score:.2f} | Time: {result.time*1000:.1f}ms"
        else:
            result_label.text = (
                f"No confident match (best: {result.name}, score: {result.score:.2f})"
            )
    else:
        result_label.text = "Too short. Try again!"


@window.event
def on_draw():
    window.clear()

    # draw stroke
    if len(current_stroke) > 1:
        for i in range(1, len(current_stroke)):
            pyglet.shapes.Line(
                current_stroke[i - 1].x,
                current_stroke[i - 1].y,
                current_stroke[i].x,
                current_stroke[i].y,
                thickness=2,
                color=(255, 255, 255),
            ).draw()

    # draw labels
    gestures_title.draw()
    for label in gesture_labels:
        label.draw()
    result_label.draw()
    commands_title.draw()
    for label in command_labels:
        label.draw()


pyglet.app.run()
