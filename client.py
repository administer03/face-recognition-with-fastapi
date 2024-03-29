import streamlit as st
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def send_frame_to_server(frame) -> dict:
    url = "http://0.0.0.0:8030/detect_faces/"
    _, img_encoded = cv2.imencode('.jpg', frame)
    response = requests.post(url, files={'file': ("frame.jpg", img_encoded.tobytes())})
    return response.json()

def detect_faces(frame) -> tuple((np.ndarray, int, list)):
    response = send_frame_to_server(frame)
    n_faces = response["detected_faces"]
    positions = response.get("positions", [])

    for index_, pos in enumerate(positions):
        x, y, w, h = pos["x"], pos["y"], pos["width"], pos["height"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Face {index_+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, n_faces, positions

def main():
    st.title("Real-Time Face Detection 🤖")
    st.sidebar.title("Settings") 
    
    #Create a menu bar
    menu = ["Picture","Webcam"]
    choice = st.sidebar.selectbox("Input type",menu)
    if choice == "Picture":
        st.sidebar.title("Upload Picture")
        uploaded_file = st.sidebar.file_uploader("Choose a picture", type=['jpg','jpeg','png'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('RGB')
            image = np.array(image)
            detect_frame, n_faces, positions = detect_faces(image)
            st.image(detect_frame)
            print(f"Number of faces detected: {n_faces}")
            print(f"Positions of faces: {positions}")
        else:
            st.info("Please upload an image file")
        
    else:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Failed to open webcam.")
            st.error("Please turn on the camera and restart the app.")
        
        # start_button = st.button('Start')
        # stop_button = st.button('Stop')
        FRAME_WINDOW = st.image([])
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame from camera")
                st.info("Please turn off the other app that is using the camera and restart app")
                break
            
            detected_frame, n_faces, positions = detect_faces(frame)
            FRAME_WINDOW.image(detected_frame)
            print(f"Positions of faces: {positions}")

        cap.release()

if __name__ == "__main__":
    main()

# """ Usage: streamlit run website.py """