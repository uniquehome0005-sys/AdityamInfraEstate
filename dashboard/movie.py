import cv2
import os
import numpy as np
import random

# ======================
# CONFIG
# ======================
image_folder = "images/"
output_video = "output.mp4"

fps = 30
hold_frames = 25
transition_frames = 20

# ======================
# LOAD IMAGES
# ======================
images = sorted([
    img for img in os.listdir(image_folder)
    if img.lower().endswith((".jpg", ".png", ".jpeg"))
])

if not images:
    raise Exception("No images found!")

first = cv2.imread(os.path.join(image_folder, images[0]))
h, w = first.shape[:2]

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(output_video, fourcc, fps, (w, h))


# ======================
# HELPERS
# ======================

def resize(img):
    return cv2.resize(img, (w, h))


def fade(img1, img2, a):
    return cv2.addWeighted(img1, 1 - a, img2, a, 0)


def zoom(img, scale):
    H, W = img.shape[:2]
    newH, newW = int(H * scale), int(W * scale)

    zoomed = cv2.resize(img, (newW, newH))

    x = newW // 2 - W // 2
    y = newH // 2 - H // 2

    cropped = zoomed[max(0, y):y + H, max(0, x):x + W]
    return cv2.resize(cropped, (W, H))


def slide(img1, img2, direction, t):
    """direction: left, right, up, down"""
    frame = np.zeros_like(img1)

    offset = int(t * w)

    if direction == "left":
        frame[:, :w - offset] = img1[:, offset:]
        frame[:, w - offset:] = img2[:, :offset]

    elif direction == "right":
        frame[:, offset:] = img1[:, :w - offset]
        frame[:, :offset] = img2[:, w - offset:]

    elif direction == "up":
        offset = int(t * h)
        frame[:h - offset, :] = img1[offset:, :]
        frame[h - offset:, :] = img2[:offset, :]

    elif direction == "down":
        offset = int(t * h)
        frame[offset:, :] = img1[:h - offset, :]
        frame[:offset, :] = img2[h - offset:, :]

    return frame


# ======================
# ANIMATION OPTIONS
# ======================

animations = [
    "zoom_in",
    "zoom_out",
    "left",
    "right",
    "up",
    "down",
    "fade"
]


def apply_animation(img1, img2, anim, t):
    if anim == "zoom_in":
        return zoom(img1, 1 + 0.3 * t)

    elif anim == "zoom_out":
        return zoom(img1, 1.3 - 0.3 * t)

    elif anim in ["left", "right", "up", "down"]:
        return slide(img1, img2, anim, t)

    elif anim == "fade":
        return fade(img1, img2, t)

    return img1


# ======================
# MAIN LOOP
# ======================

for i in range(len(images) - 1):

    img1 = resize(cv2.imread(os.path.join(image_folder, images[i])))
    img2 = resize(cv2.imread(os.path.join(image_folder, images[i + 1])))

    anim = random.choice(animations)

    # HOLD phase (animated)
    for f in range(hold_frames):
        frame = apply_animation(img1, img2, "zoom_in", f / hold_frames)
        video.write(frame)

    # TRANSITION phase
    for f in range(transition_frames):
        t = f / transition_frames
        frame = apply_animation(img1, img2, anim, t)
        video.write(frame)

# LAST IMAGE HOLD
last = resize(cv2.imread(os.path.join(image_folder, images[-1])))

for f in range(hold_frames):
    frame = zoom(last, 1 + 0.2 * (f / hold_frames))
    video.write(frame)

video.release()

print("✅ Advanced animated video created:", output_video)