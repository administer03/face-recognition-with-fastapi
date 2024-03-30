from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import uvicorn

app = FastAPI()

# Load the face detection engine
import face_detection_engine

@app.get('/')
# Defualt route, Display a welcome message
def read_main():
    return {"Welcome this is the main page of the face detection API."}

# Endpoint to detect faces in an uploaded image
@app.post("/detect_faces/")
async def detect_faces(file: UploadFile = File(...)) -> dict:
    # Read the uploaded image and perform face detection
    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use the face_detection_engine.py to detect faces
    detected_faces = face_detection_engine.face_detect(gray)
    
    # Save positions of detected faces
    positions = []
    for (x, y, w, h) in detected_faces:
        positions.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h)})
    
    # Return the number of detected faces and their positions as a dictionary
    return {"detected_faces": len(detected_faces), "positions": positions}

if __name__ == "__main__":
    # Start the server    
    uvicorn.run(app, host="localhost", port=8030, 
                log_level="info", loop="asyncio",)
                # ssl_keyfile="./ssl/server.key", ssl_certfile="./ssl/server.crt")
                # ssl_keyfile="./ssl/key.pem", ssl_certfile="./ssl/cert.pem")