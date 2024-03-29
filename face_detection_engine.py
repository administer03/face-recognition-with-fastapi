#!/usr/bin/python
import sys
import cv2
import argparse


def face_capture(source):
    cam = cv2.VideoCapture(0)
    # read image data from input stream
    image = cv2.imread(source)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray


def webcam_capture(source):
    cam = cv2.VideoCapture(source)

    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        return None, None

    # read image data from input stream
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame, gray


def face_detect(gray, cascasdepath="haarcascade_frontalface_default.xml"):
    # process face detection
    face_cascade = cv2.CascadeClassifier(cascasdepath)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(30, 30)

    )
    print("The number of faces found = ", len(faces))

    return faces


def render(image, faces, nogui=False):
    # create output image
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + h, y + h), (0, 255, 0), 2)

    if nogui:
        cv2.imwrite('detected_face.png', image)
        return len(faces)
    else:
        cv2.imshow("Faces found", image)
        print("Press ESC to exit.")
        cv2.waitKey(0)


if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser(description='Simple Face Detection.')
    parser.add_argument("-s", "--source",
                        type=str,
                        default="0",
                        help="Source. Path to the input image.")

    parser.add_argument("-m", "--model",
                       type=str,
                       default="haarcascade_frontalface_default.xml",
                       help="Model path. Path to the 'haarcascade_frontalface_default.xml'.")

    parser.add_argument("-u", "--nogui",
                        type=bool,
                        default=False,
                        help="Enable GUI?. Disable GUI. Default False.")

    args = parser.parse_args()
    print("Using model", args.model)

    # Run the face detection
    if args.source == "0":
        print("Detect face using webcam")
        image, gray = webcam_capture(int(args.source))
    else:
        print("Detect face in", args.source)
        image, gray = face_capture(args.source)

    detected_faces = face_detect(gray, cascasdepath=args.model)
    n_faces = render(image, detected_faces, nogui=False)

    cv2.destroyAllWindows()
