[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/iuYZxbvR)

# Assignment 6: Gesture Recognition

Assignment 6 for the Interactive Techniques and Technologies course (ITT), Universität Regensburg.

Author: Martina Roby Culasso

---

Each task folder contains an `info.txt` file with a description of the files and relevant notes.

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Task 1 - Implementing the $1 Gesture Recognizer

A Python port of Wobbrock et al.'s $1 unistroke gesture recognizer, with a pyglet interface to draw and test five gestures (rectangle, circle, check, delete, pigtail) live.

**Usage:**

```bash
cd task_1
python gesture_input.py
```

---

## Task 2 - Comparing Gesture Recognizers

Trains five LSTM classifiers of decreasing size on Wobbrock et al.'s gesture logs, then evaluates them on a custom test set captured with `capture_logs.py`. Results and discussion are in `unistroke_gestures.ipynb`.

**Usage:**

(If you want to recapture the test set)

```bash
cd task_2
python capture_logs.py
```

(If you want to retrain the models)

Open `task_2/unistroke_gestures.ipynb` and run all cells. Before running, make sure the `logs/` folder with Wobbrock et al.'s gesture log dataset is present locally.

---

## Task 3 - Gesture Detection Game

"Ghost Buster": a small game controlled with three gestures (rectangle, pigtail, caret). Draw the matching gesture to banish ghosts before they cross the danger line.

**Usage:**

```bash
cd task_3
python gesture_application.py
```

**Controls:**

| Key | Action |
|-----|--------|
| Mouse (in drawing zone) | Draw a gesture |
| `Space` | Start the game |
| `R` | Restart after game over |
| `Q` / `Esc` | Quit |

---

## Bonus - Study Participation

Signed up to take part in Michael's data logging study for his LSTM, scheduled for next Friday.
