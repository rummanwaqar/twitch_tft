import cv2
import sys
from game_manager import GameManager

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py img|video')
        exit(1)

    manager = GameManager()
    
    # process video
    if sys.argv[1].endswith('.mp4'):
        video = cv2.VideoCapture(sys.argv[1])
        while True:
            ret, frame = video.read()
            if not ret:
                break
            champions = manager.processFrame(frame)
            manager.draw(frame, champions)
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Video', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        video.release()
    # process image
    elif sys.argv[1].endswith('.jpg') or sys.argv[1].endswith('.bmp'):
        img = cv2.imread(sys.argv[1])
        champions = manager.processFrame(img)
        manager.draw(img, champions)
        cv2.imshow('Result', img)
        cv2.waitKey(0)

    cv2.destroyAllWindows()