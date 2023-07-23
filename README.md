# Gesture Controlled Video Jigsaw Puzzle

This is a Python application that uses OpenCV and Google's MediaPipe library to create a gesture-controlled video jigsaw puzzle. You can control the puzzle pieces by moving your hand in front of the webcam. 

## Dependencies
This application uses the following libraries:
- OpenCV
- MediaPipe
- Numpy

Install them using pip:
```
pip install opencv-python-headless
pip install mediapipe
pip install numpy
```

## How to Run
1. Ensure you have Python 3.6+ installed on your machine.
2. Install the dependencies listed above.
3. Run `python puzzle.py` in your terminal.

## How to Play
- Move your hand in front of the camera. The application uses the position of the index finger tip to determine the coordinates of the click.
- To move a puzzle piece, position your index finger over it and perform a click gesture.
- The game is solved when all pieces are in their correct position.

## Customizations
You may adjust several parameters in the script to fit your requirements:
- `COLS` and `ROWS`: Change these to alter the puzzle complexity.
- Hand detection parameters in the `mp_hands.Hands()` constructor can be adjusted to better suit your lighting conditions and needs.

## Troubleshooting
If you encounter issues with the application, ensure that your webcam is properly connected and functioning. You may need to adjust the hand detection parameters to work better with your specific webcam and lighting conditions.

Enjoy the game!
