# $1 gesture recognizer - Python Version

# Based on the JavaScript implementation by:
#   Jacob O. Wobbrock, Ph.D. - University of Washington
#   Andrew D. Wilson, Ph.D.  - Microsoft Research
#   Yang Li, Ph.D.           - University of Washington
#
# Original source: https://depts.washington.edu/acelab/proj/dollar/index.html
#
# Reference:
#   Wobbrock, J.O., Wilson, A.D. and Li, Y. (2007). Gestures without libraries,
#   toolkits or training: A $1 recognizer for user interface prototypes.
#   Proceedings of UIST '07, pp. 159-168.
#   https://dl.acm.org/citation.cfm?id=1294238
#
# Python translation by: Martina Roby Culasso


# IMPORTS ===

import math
import time

# CONSTANTS (independent) ===

NUM_UNISTROKES = 5  # changed to fit assignment requirements, original is 16
NUM_POINTS = 64
SQUARE_SIZE = 250.0
DIAGONAL = math.sqrt(SQUARE_SIZE * SQUARE_SIZE + SQUARE_SIZE * SQUARE_SIZE)
HALF_DIAGONAL = 0.5 * DIAGONAL
PHI = 0.5 * (-1.0 + math.sqrt(5.0))


# CLASSES ===


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Unistroke:
    def __init__(self, name, points):
        self.name = name
        self.points = Resample(points, NUM_POINTS)
        radians = IndicativeAngle(self.points)
        self.points = RotateBy(self.points, -radians)
        self.points = ScaleTo(self.points, SQUARE_SIZE)
        self.points = TranslateTo(self.points, ORIGIN)
        self.vector = Vectorize(self.points)


class Result:
    def __init__(self, name, score, ms):
        self.name = name
        self.score = score
        self.time = ms


# CONSTANTS CONT. (dependent on classes) ===

ORIGIN = Point(0, 0)


# CLASSES CONT. ===


class DollarRecognizer:
    def __init__(self):
        # I formatteed the code inside VSCode to follow Python conventions, that's why this part is written in so many lines)
        self.Unistrokes = []
        self.Unistrokes.append(
            Unistroke(
                "rectangle",
                [
                    Point(78, 149),
                    Point(78, 153),
                    Point(78, 157),
                    Point(78, 160),
                    Point(79, 162),
                    Point(79, 164),
                    Point(79, 167),
                    Point(79, 169),
                    Point(79, 173),
                    Point(79, 178),
                    Point(79, 183),
                    Point(80, 189),
                    Point(80, 193),
                    Point(80, 198),
                    Point(80, 202),
                    Point(81, 208),
                    Point(81, 210),
                    Point(81, 216),
                    Point(82, 222),
                    Point(82, 224),
                    Point(82, 227),
                    Point(83, 229),
                    Point(83, 231),
                    Point(85, 230),
                    Point(88, 232),
                    Point(90, 233),
                    Point(92, 232),
                    Point(94, 233),
                    Point(99, 232),
                    Point(102, 233),
                    Point(106, 233),
                    Point(109, 234),
                    Point(117, 235),
                    Point(123, 236),
                    Point(126, 236),
                    Point(135, 237),
                    Point(142, 238),
                    Point(145, 238),
                    Point(152, 238),
                    Point(154, 239),
                    Point(165, 238),
                    Point(174, 237),
                    Point(179, 236),
                    Point(186, 235),
                    Point(191, 235),
                    Point(195, 233),
                    Point(197, 233),
                    Point(200, 233),
                    Point(201, 235),
                    Point(201, 233),
                    Point(199, 231),
                    Point(198, 226),
                    Point(198, 220),
                    Point(196, 207),
                    Point(195, 195),
                    Point(195, 181),
                    Point(195, 173),
                    Point(195, 163),
                    Point(194, 155),
                    Point(192, 145),
                    Point(192, 143),
                    Point(192, 138),
                    Point(191, 135),
                    Point(191, 133),
                    Point(191, 130),
                    Point(190, 128),
                    Point(188, 129),
                    Point(186, 129),
                    Point(181, 132),
                    Point(173, 131),
                    Point(162, 131),
                    Point(151, 132),
                    Point(149, 132),
                    Point(138, 132),
                    Point(136, 132),
                    Point(122, 131),
                    Point(120, 131),
                    Point(109, 130),
                    Point(107, 130),
                    Point(90, 132),
                    Point(81, 133),
                    Point(76, 133),
                ],
            )
        )
        self.Unistrokes.append(
            Unistroke(
                "circle",
                [
                    Point(127, 141),
                    Point(124, 140),
                    Point(120, 139),
                    Point(118, 139),
                    Point(116, 139),
                    Point(111, 140),
                    Point(109, 141),
                    Point(104, 144),
                    Point(100, 147),
                    Point(96, 152),
                    Point(93, 157),
                    Point(90, 163),
                    Point(87, 169),
                    Point(85, 175),
                    Point(83, 181),
                    Point(82, 190),
                    Point(82, 195),
                    Point(83, 200),
                    Point(84, 205),
                    Point(88, 213),
                    Point(91, 216),
                    Point(96, 219),
                    Point(103, 222),
                    Point(108, 224),
                    Point(111, 224),
                    Point(120, 224),
                    Point(133, 223),
                    Point(142, 222),
                    Point(152, 218),
                    Point(160, 214),
                    Point(167, 210),
                    Point(173, 204),
                    Point(178, 198),
                    Point(179, 196),
                    Point(182, 188),
                    Point(182, 177),
                    Point(178, 167),
                    Point(170, 150),
                    Point(163, 138),
                    Point(152, 130),
                    Point(143, 129),
                    Point(140, 131),
                    Point(129, 136),
                    Point(126, 139),
                ],
            )
        )
        self.Unistrokes.append(
            Unistroke(
                "check",
                [
                    Point(91, 185),
                    Point(93, 185),
                    Point(95, 185),
                    Point(97, 185),
                    Point(100, 188),
                    Point(102, 189),
                    Point(104, 190),
                    Point(106, 193),
                    Point(108, 195),
                    Point(110, 198),
                    Point(112, 201),
                    Point(114, 204),
                    Point(115, 207),
                    Point(117, 210),
                    Point(118, 212),
                    Point(120, 214),
                    Point(121, 217),
                    Point(122, 219),
                    Point(123, 222),
                    Point(124, 224),
                    Point(126, 226),
                    Point(127, 229),
                    Point(129, 231),
                    Point(130, 233),
                    Point(129, 231),
                    Point(129, 228),
                    Point(129, 226),
                    Point(129, 224),
                    Point(129, 221),
                    Point(129, 218),
                    Point(129, 212),
                    Point(129, 208),
                    Point(130, 198),
                    Point(132, 189),
                    Point(134, 182),
                    Point(137, 173),
                    Point(143, 164),
                    Point(147, 157),
                    Point(151, 151),
                    Point(155, 144),
                    Point(161, 137),
                    Point(165, 131),
                    Point(171, 122),
                    Point(174, 118),
                    Point(176, 114),
                    Point(177, 112),
                    Point(177, 114),
                    Point(175, 116),
                    Point(173, 118),
                ],
            )
        )
        self.Unistrokes.append(
            Unistroke(
                "delete",
                [
                    Point(123, 129),
                    Point(123, 131),
                    Point(124, 133),
                    Point(125, 136),
                    Point(127, 140),
                    Point(129, 142),
                    Point(133, 148),
                    Point(137, 154),
                    Point(143, 158),
                    Point(145, 161),
                    Point(148, 164),
                    Point(153, 170),
                    Point(158, 176),
                    Point(160, 178),
                    Point(164, 183),
                    Point(168, 188),
                    Point(171, 191),
                    Point(175, 196),
                    Point(178, 200),
                    Point(180, 202),
                    Point(181, 205),
                    Point(184, 208),
                    Point(186, 210),
                    Point(187, 213),
                    Point(188, 215),
                    Point(186, 212),
                    Point(183, 211),
                    Point(177, 208),
                    Point(169, 206),
                    Point(162, 205),
                    Point(154, 207),
                    Point(145, 209),
                    Point(137, 210),
                    Point(129, 214),
                    Point(122, 217),
                    Point(118, 218),
                    Point(111, 221),
                    Point(109, 222),
                    Point(110, 219),
                    Point(112, 217),
                    Point(118, 209),
                    Point(120, 207),
                    Point(128, 196),
                    Point(135, 187),
                    Point(138, 183),
                    Point(148, 167),
                    Point(157, 153),
                    Point(163, 145),
                    Point(165, 142),
                    Point(172, 133),
                    Point(177, 127),
                    Point(179, 127),
                    Point(180, 125),
                ],
            )
        )
        self.Unistrokes.append(
            Unistroke(
                "pigtail",
                [
                    Point(81, 219),
                    Point(84, 218),
                    Point(86, 220),
                    Point(88, 220),
                    Point(90, 220),
                    Point(92, 219),
                    Point(95, 220),
                    Point(97, 219),
                    Point(99, 220),
                    Point(102, 218),
                    Point(105, 217),
                    Point(107, 216),
                    Point(110, 216),
                    Point(113, 214),
                    Point(116, 212),
                    Point(118, 210),
                    Point(121, 208),
                    Point(124, 205),
                    Point(126, 202),
                    Point(129, 199),
                    Point(132, 196),
                    Point(136, 191),
                    Point(139, 187),
                    Point(142, 182),
                    Point(144, 179),
                    Point(146, 174),
                    Point(148, 170),
                    Point(149, 168),
                    Point(151, 162),
                    Point(152, 160),
                    Point(152, 157),
                    Point(152, 155),
                    Point(152, 151),
                    Point(152, 149),
                    Point(152, 146),
                    Point(149, 142),
                    Point(148, 139),
                    Point(145, 137),
                    Point(141, 135),
                    Point(139, 135),
                    Point(134, 136),
                    Point(130, 140),
                    Point(128, 142),
                    Point(126, 145),
                    Point(122, 150),
                    Point(119, 158),
                    Point(117, 163),
                    Point(115, 170),
                    Point(114, 175),
                    Point(117, 184),
                    Point(120, 190),
                    Point(125, 199),
                    Point(129, 203),
                    Point(133, 208),
                    Point(138, 213),
                    Point(145, 215),
                    Point(155, 218),
                    Point(164, 219),
                    Point(166, 219),
                    Point(177, 219),
                    Point(182, 218),
                    Point(192, 216),
                    Point(196, 213),
                    Point(199, 212),
                    Point(201, 211),
                ],
            )
        )

    def Recognize(self, points, useProtractor):
        t0 = time.time()
        candidate = Unistroke("", points)

        u = -1
        b = math.inf

        for i in range(0, len(self.Unistrokes)):
            if useProtractor:
                d = OptimalCosineDistance(self.Unistrokes[i].vector, candidate.vector)
            else:
                d = DistanceAtBestAngle(
                    candidate.points,
                    self.Unistrokes[i],
                    -ANGLE_RANGE,
                    +ANGLE_RANGE,
                    ANGLE_PRECISION,
                )

            if d < b:
                b = d
                u = i

        t1 = time.time()

        if u == -1:
            result = Result("No match.", 0.0, t1 - t0)
        else:
            score = (1.0 - b) if useProtractor else (1.0 - b / HALF_DIAGONAL)
            result = Result(self.Unistrokes[u].name, score, t1 - t0)

        return result

    def AddGesture(self, name, points):
        self.Unistrokes.append(Unistroke(name, points))
        num = 0

        for i in range(0, len(self.Unistrokes)):
            if self.Unistrokes[i].name == name:
                num += 1

        return num

    def DeleteUserGestures(self):
        del self.Unistrokes[NUM_UNISTROKES:]

        return NUM_UNISTROKES


# FUNCTIONS ===


# we can't use a regular "for i in range(len(points))" because the length of points can change inside the loop
def Resample(points, n):
    I = PathLength(points) / (n - 1)
    D = 0.0
    newpoints = [points[0]]
    i = 1
    temp_len = len(points)

    while i < temp_len:
        d = Distance(points[i - 1], points[i])
        if D + d >= I:
            qx = points[i - 1].x + ((I - D) / d) * (points[i].x - points[i - 1].x)
            qy = points[i - 1].y + ((I - D) / d) * (points[i].y - points[i - 1].y)
            q = Point(qx, qy)
            newpoints.append(q)
            points.insert(i, q)
            D = 0.0
        else:
            D += d
        i += 1
        temp_len = len(points)

    if len(newpoints) == n - 1:
        qx_temp = points[-1].x
        qy_temp = points[-1].y
        q_temp = Point(qx_temp, qy_temp)
        newpoints.append(q_temp)

    return newpoints


def IndicativeAngle(points):
    c = Centroid(points)

    return math.atan2(c.y - points[0].y, c.x - points[0].x)


def RotateBy(points, radians):
    c = Centroid(points)
    cos = math.cos(radians)
    sin = math.sin(radians)
    newpoints = []

    for i in range(0, len(points)):
        qx = (points[i].x - c.x) * cos - (points[i].y - c.y) * sin + c.x
        qy = (points[i].x - c.x) * sin + (points[i].y - c.y) * cos + c.y
        newpoints.append(Point(qx, qy))

    return newpoints


def ScaleTo(points, size):
    B = BoundingBox(points)
    newpoints = []

    for i in range(0, len(points)):
        qx = points[i].x * (size / B.width)
        qy = points[i].y * (size / B.height)
        newpoints.append(Point(qx, qy))

    return newpoints


def TranslateTo(points, pt):
    c = Centroid(points)
    newpoints = []

    for i in range(0, len(points)):
        qx = points[i].x + pt.x - c.x
        qy = points[i].y + pt.y - c.y
        newpoints.append(Point(qx, qy))

    return newpoints


def Vectorize(points):
    sum = 0.0
    vector = []

    for i in range(0, len(points)):
        vector.append(points[i].x)
        vector.append(points[i].y)
        sum += points[i].x * points[i].x + points[i].y * points[i].y

    magnitude = math.sqrt(sum)

    for i in range(0, len(vector)):
        vector[i] /= magnitude

    return vector


def OptimalCosineDistance(v1, v2):
    a = 0.0
    b = 0.0

    for i in range(0, len(v1), 2):
        a += v1[i] * v2[i] + v1[i + 1] * v2[i + 1]
        b += v1[i] * v2[i + 1] - v1[i + 1] * v2[i]
    angle = math.atan(b / a)

    return math.acos(a * math.cos(angle) + b * math.sin(angle))


def DistanceAtBestAngle(points, T, a, b, threshold):
    x1 = PHI * a + (1.0 - PHI) * b
    f1 = DistanceAtAngle(points, T, x1)
    x2 = (1.0 - PHI) * a + PHI * b
    f2 = DistanceAtAngle(points, T, x2)

    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = PHI * a + (1.0 - PHI) * b
            f1 = DistanceAtAngle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - PHI) * a + PHI * b
            f2 = DistanceAtAngle(points, T, x2)

    return min(f1, f2)


def DistanceAtAngle(points, T, radians):
    newpoints = RotateBy(points, radians)

    return PathDistance(newpoints, T.points)


def Centroid(points):
    x = 0.0
    y = 0.0

    for i in range(0, len(points)):
        x += points[i].x
        y += points[i].y

    x /= len(points)
    y /= len(points)

    return Point(x, y)


def BoundingBox(points):
    minX = math.inf
    maxX = -math.inf
    minY = math.inf
    maxY = -math.inf

    for i in range(0, len(points)):
        minX = min(minX, points[i].x)
        maxX = max(maxX, points[i].x)
        minY = min(minY, points[i].y)
        maxY = max(maxY, points[i].y)

    return Rectangle(minX, minY, maxX - minX, maxY - minY)


def PathDistance(pts1, pts2):
    d = 0.0

    for i in range(0, len(pts1)):
        d += Distance(pts1[i], pts2[i])

    return d / len(pts1)


def PathLength(points):
    d = 0.0

    for i in range(1, len(points)):
        d += Distance(points[i - 1], points[i])

    return d


def Distance(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    return math.sqrt(dx * dx + dy * dy)


def Deg2Rad(d):
    return d * math.pi / 180.0


# CONSTANTS CONT. (dependent on defined functions) ===

ANGLE_RANGE = Deg2Rad(45.0)
ANGLE_PRECISION = Deg2Rad(2.0)
