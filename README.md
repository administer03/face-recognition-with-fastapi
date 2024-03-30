# Face Detection

This project focuses on utilizing the OpenCV library for face detection in a video stream, with FastAPI employed for both server and client aspects. Additionally, the frontend in this test employs Streamlit, a framework for creating user interfaces based on the Python language.


## Installation

> [!Note]
> Here, Python 3.9.12 is required.

```
pip install -r requirements.txt
```

## Config HTTPS
In this step, we will generate a self-signed certificate for the HTTPS connection.
Here, I decided to use the mkcert tool to generate the certificate.
```
mkcert localhost 127.0.0.1 0.0.0.0
```
Then, move the generated files, name "localhost-key.pem" and "localhost.pem", to the "certs" folder.

> [!Note]
> In this testing, the certificate is generated for the localhost only.

## Run the FastAPI server
```
python api.py
```

## Run the client script
```
streamlit run client.py
```

## Usage
Start the FastAPI server on the server machine.
Run the client script on the client machine.
View the video stream and detected faces via the Streamlit interface.