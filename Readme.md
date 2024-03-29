### Face Detection

This project focuses on utilizing the OpenCV library for face detection in a video stream, with FastAPI employed for both server and client aspects.

#### Overview

The aim is to detect faces in real-time video streams using a high-performance server and display the results using a user-friendly interface.

#### Installation


```bash
# Install required dependencies for the server
pip install fastapi uvicorn opencv-python-headless numpy
```

# Run the FastAPI server
python api.py

# Run the client script
streamlit run client.py 

# Usage
Start the FastAPI server on the server machine.
Run the client script on the client machine.
View the video stream and detected faces via the Streamlit interface.
