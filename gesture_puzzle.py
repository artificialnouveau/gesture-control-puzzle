import cv2
import mediapipe as mp
import numpy as np
import random

# Constants
COLS = 4
ROWS = 4
WIDTH, HEIGHT = 400, 400
TILE_W, TILE_H = WIDTH // COLS, HEIGHT // ROWS
BUFFER_SIZE = 1000
TILES = []
BOARD = []

# Setup MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Setup OpenCV
cap = cv2.VideoCapture(0)

# Tiles Setup
class Tile:
    def __init__(self, index, img):
        self.index = index
        self.img = img

for i in range(COLS):
    for j in range(ROWS):
        x = i * TILE_W
        y = j * TILE_H
        index = i + j * COLS
        BOARD.append(index)
        tile = Tile(index, np.zeros((TILE_W, TILE_H, 3)))
        TILES.append(tile)

TILES.pop()
BOARD.pop()
BOARD.append(-1)

def swap(i, j, arr):
    arr[i], arr[j] = arr[j], arr[i]

def move(i, j, arr):
    blank = find_blank()
    blank_col = blank % COLS
    blank_row = blank // ROWS

    if is_neighbor(i, j, blank_col, blank_row):
        swap(blank, i + j * COLS, arr)

def find_blank():
    for i in range(len(BOARD)):
        if BOARD[i] == -1:
            return i

def is_neighbor(i, j, x, y):
    return (i == x or j == y) and (abs(i - x) == 1 or abs(j - y) == 1)

def simple_shuffle(arr):
    for _ in range(BUFFER_SIZE):
        r1 = random.randint(0, COLS - 1)
        r2 = random.randint(0, ROWS - 1)
        move(r1, r2, arr)

def is_solved():
    for i in range(len(BOARD) - 1):
        if BOARD[i] != TILES[i].index:
            return False
    return True

simple_shuffle(BOARD)

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the image horizontally
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and find hand landmarks
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * COLS)
            y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * ROWS)
            move(x, y, BOARD)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # update and draw tiles
    for i in range(COLS):
        for j in range(ROWS):
            x = i * TILE_W
            y = j * TILE_H
            index = i + j * COLS
            if BOARD[index] != -1:
                tile_img = TILES[BOARD[index]].img
                frame[y:y+TILE_H, x:x+TILE_W] = tile_img

    if is_solved():
        print("SOLVED")

    # Show image
    cv2.imshow('MediaPipe Hands', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
