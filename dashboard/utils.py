def generate_property_video(image_paths):

    import cv2
    import numpy as np
    import random
    import uuid

    output_path = f"/tmp/property_{uuid.uuid4().hex}.mp4"

    fps = 30
    hold_frames = 25
    transition_frames = 20

    if not image_paths:
        raise Exception("No images found")

    first = cv2.imread(image_paths[0])
    h, w = first.shape[:2]

    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

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
        frame = np.zeros_like(img1)
        offset = int(t * w)

        if direction == "left":
            frame[:, :w - offset] = img1[:, offset:]
            frame[:, w - offset:] = img2[:, :offset]

        elif direction == "right":
            frame[:, offset:] = img1[:, :w - offset]
            frame[:, :offset] = img2[:, w - offset:]

        return frame

    animations = ["zoom_in", "zoom_out", "left", "right", "fade"]

    def apply(img1, img2, anim, t):
        if anim == "zoom_in":
            return zoom(img1, 1 + 0.3 * t)
        elif anim == "zoom_out":
            return zoom(img1, 1.3 - 0.3 * t)
        elif anim in ["left", "right"]:
            return slide(img1, img2, anim, t)
        elif anim == "fade":
            return fade(img1, img2, t)
        return img1

    for i in range(len(image_paths) - 1):

        img1 = resize(cv2.imread(image_paths[i]))
        img2 = resize(cv2.imread(image_paths[i + 1]))

        anim = random.choice(animations)

        for f in range(hold_frames):
            frame = apply(img1, img2, "zoom_in", f / hold_frames)
            video.write(frame)

        for f in range(transition_frames):
            t = f / transition_frames
            frame = apply(img1, img2, anim, t)
            video.write(frame)

    video.release()

    return output_path