# gesture input program for first task

import pyglet
from recognizer import DollarRecognizer, Point

# constants
MIN_STROKE_LENGTH = 10
SCORE_THRESHOLD = 0.5
REQUIRED_GESTURES = {
    "rectangle",
    "circle",
    "check",
    "delete",
    "pigtail",
}  # filter only these 5 gestures as required by task 1

# variables
current_stroke = []

# setup
window = pyglet.window.Window(1100, 600, caption="$1 Gesture Recognizer")
recognizer = DollarRecognizer()

# sprite
gesture_reference = pyglet.image.load("gesture_reference.png")
gesture_sprite = pyglet.sprite.Sprite(gesture_reference, x=800, y=150)
gesture_sprite.scale = 0.4

# labels
result_label = pyglet.text.Label(
    "Draw a gesture using your mouse/touchpad!",
    x=15,
    y=560,
    color=(255, 255, 255, 255),
    font_size=20,
)

gestures_title = pyglet.text.Label(
    "Available gestures:", x=800, y=560, color=(200, 200, 200, 255), font_size=16
)
recognizer.Unistrokes = [
    u for u in recognizer.Unistrokes if u.name in REQUIRED_GESTURES
]
gesture_names = [u.name for u in recognizer.Unistrokes]
gesture_labels = [
    pyglet.text.Label(
        f"- {name}", x=800, y=535 - i * 20, color=(180, 180, 180, 255), font_size=14
    )
    for i, name in enumerate(gesture_names)
]

commands_label = pyglet.text.Label(
    "Commands: [C] clear stroke | [Q] or [ESC] quit",
    x=15,
    y=15,
    color=(180, 180, 180, 255),
    font_size=16,
)


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
    current_stroke.append(Point(x, y))  # capture first point


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    current_stroke.append(Point(x, y))  # capture dragging


@window.event
def on_mouse_release(x, y, button, modifiers):
    if len(current_stroke) > 10:
        # transform the points to top-left Y coordinates for the recognizer 
        processed_stroke = [Point(p.x, window.height - p.y) for p in current_stroke]

        # pass the processed stroke
        result = recognizer.Recognize(processed_stroke, True)

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
    result_label.draw()
    gestures_title.draw()
    for label in gesture_labels:
        label.draw()
    gesture_sprite.draw()
    commands_label.draw()


pyglet.app.run()
