import cv2
import sys
from game_manager import GameManager

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py video')
        exit(1)
    
    output_scaling = 0.5
    output = {}
    if len(sys.argv) == 3:
        output['file'] = sys.argv[2]
    
    # process video
    if sys.argv[1].endswith('.mp4'):
        manager = GameManager()
        video = cv2.VideoCapture(sys.argv[1])

        if output:
            fps = video.get(cv2.CAP_PROP_FPS)
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH) * output_scaling)
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT) * output_scaling)
            output['writer'] = cv2.VideoWriter(output['file'], cv2.VideoWriter_fourcc(*'MP4V'), fps, (width, height))
            print('Writing output video to {}'.format(output['file']))
        
        while True:
            ret, frame = video.read()
            if not ret:
                break
            manager.processFrame(frame)
            manager.draw(frame)
            frame = cv2.resize(frame, None, fx=output_scaling, fy=output_scaling, interpolation=cv2.INTER_AREA)

            if output:
                output['writer'].write(frame)

            if not output:
                cv2.imshow('Video', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        video.release()
        if output:
            output['writer'].release()
    else:
        print('invalid video file')

    cv2.destroyAllWindows()