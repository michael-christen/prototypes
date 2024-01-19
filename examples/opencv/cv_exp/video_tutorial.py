import sys

import numpy as np
import cv2


def main(load):
    cap = cv2.VideoCapture(load)
    if not cap.isOpened():
        print('Cannot open camera')
        sys.exit()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # write the flipped frame
        out.write(frame)

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        load = sys.argv[1]
    else:
        load = 0
    main(load)
