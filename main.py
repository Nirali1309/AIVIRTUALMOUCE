import cv2   # package
import mediapipe as mp   # package
import pyautogui   # package

cap = cv2.VideoCapture(0)   # for the videocapture.... 0 for the pc camera or primary camera

hand_detector = mp.solutions.hands.Hands()   # for handDetector
drawing_utils = mp.solutions.drawing_utils   # for the landmark

screen_width, screen_height = pyautogui.size()    # width and height of the screen
index_y = 0   # initialization

while True:
    _, frame = cap.read()    # to read the captured video
    frame = cv2.flip(frame, 1)   # for flip the frame

    frame_height, frame_width, _ = frame.shape   # initialized frame height and width same as frame shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # convert the color BGR to RGB

    output = hand_detector.process(rgb_frame)   # for the output
    hands = output.multi_hand_landmarks   # for the multi hand landmark

    if hands:
        for hand in hands:

            drawing_utils.draw_landmarks(frame, hand)   # for the landmark of hand on hand
            landmarks = hand.landmark    # landmarks

            for id, landmark in enumerate(landmarks):

                x = int(landmark.x*frame_width)   # for the x position of the landmark
                y = int(landmark.y*frame_height)   # for the y position of the landmark

                if id == 8:   # for the first finger of the hand

                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))   # draw circle around the landmark
                    index_x = screen_width/frame_width*x   # for the cursor to visit whole screen in x direction using index finger
                    index_y = screen_height/frame_height*y   # for the cursor to visit whole screen in y direction  using index finger

                if id == 4:   # for the thump of hand

                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))   # draw circle around the landmark
                    thumb_x = screen_width/frame_width*x   # for the cursor to visit whole screen in x direction using thump
                    thumb_y = screen_height/frame_height*y  # for the cursor to visit whole screen in y direction using thump
                    print('outside', abs(index_y - thumb_y))   # to print the landmark in output

                    if abs(index_y - thumb_y) < 20:   # if the index finger and thump distant less than 20 then
                        pyautogui.click()   # for the click
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:   # if the index finger and thump distant less than 100 then
                        pyautogui.moveTo(index_x, index_y)   # to move the cursor

    cv2.imshow('Virtual Mouse', frame)    # show the frame
    cv2.waitKey(1)
