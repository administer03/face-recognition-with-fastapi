# Face Detection

This project focuses on utilizing the OpenCV library for face detection in a video stream, with FastAPI employed for both server and client aspects. Additionally, the frontend in this test employs Streamlit, a framework for creating user interfaces based on the Python language.


## Installation

```
pip install -r requirements.txt
```

## Run the FastAPI server
```
python api.py
```

## Config HTTPS
In this step, we will generate a self-signed certificate for the HTTPS connection.
```
mkcert localhost 127.0.0.1 0.0.0.0
```
Then, move the generated files, name "localhost-key.pem" and "localhost.pem", to the "certs" folder.

## Run the client script
```
streamlit run client.py
```

## Usage
Start the FastAPI server on the server machine.
Run the client script on the client machine.
View the video stream and detected faces via the Streamlit interface.
