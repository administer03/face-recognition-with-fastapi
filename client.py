import streamlit as st
import cv2
import numpy as np
import requests
from PIL import Image

# Function to send a frame to the server
def send_frame_to_server(frame) -> dict:
    try: # In case of send on HTTPS
        url = "https://0.0.0.0:8030/detect_faces/"
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(url, files={'file': ("frame.jpg", img_encoded.tobytes())}, verify=False)

    except: # In case of send on HTTP
        url = "http://0.0.0.0:8030/detect_faces/"
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post(url, files={'file': ("frame.jpg", img_encoded.tobytes())})
        
    # Return the response
    return response.json()

# Function to detect faces in a frame, returns the frame with x,y,w,h of detected faces
def detect_faces(frame) -> tuple((np.ndarray, int, list)):
    response = send_frame_to_server(frame)
    n_faces = response["detected_faces"]
    positions = response.get("positions", [])

    # Loop through the detected faces and draw rectangles on the frame
    for index_, pos in enumerate(positions):
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Add a label, number of the face
        cv2.putText(frame, f"Face {index_+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Return the frame with detected faces, number of faces, and positions
    return frame_rgb, n_faces, positions

def main():
    st.title("Real-Time Face Detection 🤖")
    st.sidebar.title("Settings") 
    
    #Create a menu bar for input type
    menu = ["Picture","Webcam"]
    choice = st.sidebar.selectbox("Input type",menu)
    
    # Incase user selects Picture
    if choice == "Picture":
        st.sidebar.title("Upload Picture")
        uploaded_file = st.sidebar.file_uploader("Choose a picture", type=['jpg','jpeg','png'])
        if uploaded_file is not None:
            # Read the image from the file_uploader
            image = Image.open(uploaded_file).convert('RGB')
            image = np.array(image)
            # Detect faces in the image
            detect_frame, n_faces, positions = detect_faces(image)
            # Display the image with detected faces
            st.image(detect_frame)
            # Display logs in the console
            print(f"Number of faces detected: {n_faces}")
            print(f"Positions of faces: {positions}")
        else:
            st.info("Please upload an image file")
    
    # Incase user selects Webcam
    elif choice == "Webcam":
        # Open the webcam
        cap = cv2.VideoCapture(0)
        # Check if the webcam can be opened
        if not cap.isOpened():
            st.error("Failed to open webcam.")
            st.error("Please turn on the camera and restart the app.")
        # Create a placeholder for the frame
        FRAME_WINDOW = st.image([])
        # Loop to capture frames from the webcam
        while cap.isOpened():
            ret, frame = cap.read()
            # Check if the frame was captured
            if not ret:
                st.error("Failed to capture frame from camera")
                st.info("Please turn off the other app that is using the camera and restart app")
                break
            # Detect faces in the frame
            detected_frame, n_faces, positions = detect_faces(frame)
            # Display the frame with detected faces via the placeholder
            FRAME_WINDOW.image(detected_frame)
            # Display logs in the console
            print(f"Positions of faces: {positions}")
        cap.release()

if __name__ == "__main__":
    main()
    
# """ Usage: streamlit run website.py """