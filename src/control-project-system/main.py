# Save this file as main.py
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()


# Define a path operation decorator for the root URL ("/") and the GET method
@app.get("/")
# Define the path operation function
def read_root():
    return {"message": "Hello World"}
