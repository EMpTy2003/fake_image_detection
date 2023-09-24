from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dl_model import Prediction

app = FastAPI()

# Allow Cross Origin
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1")
async def main():
    return {"message": "Hello World"}

# Define the directory where the uploaded & output files will be saved
upload_dir = Path("uploads")
image_dir = Path("out")

# ------------------------------ POST : FILE UPLOAD & PREDICTION ----------------------------
# This method is used to receive the files form the user and initiate the prediction process
@app.post("/api/v1/uploadfile/")
async def upload_file(file: UploadFile = File(...), 
                      custom_filename: str = "test.jpg"):

    # Create the output directory if it doesn't exist
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Use the custom filename if provided, or use the original filename (optional)
    # Reason for use : Because of some file have unsupported characters in its name
    if custom_filename:
        file_path = upload_dir / custom_filename
    else:
        file_path = upload_dir / file.filename

    # Save the uploaded file to the output directory
    with file_path.open("wb") as f:
        f.write(file.file.read())

    # Prediction Process
    pred = Prediction()
    pred._test_image_path = str(file_path)

    class_name, conf = pred.process()

    return {"filename": file_path.name, 
            "class": class_name[:-1], 
            "con": conf}


# --------------------------- GET : SEND THE OUTPUT FILES AS RESPONSE ----------------------
# This method is used to send the output files to the frontend
@app.get("/api/v1/get_image/{image_path}")
async def get_image(image_path: str):
    # Build the full image file path based on the path variable
    full_image_path = image_dir / image_path

    # Check if the image file exists
    if not full_image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image as a response
    return FileResponse(full_image_path)


# To serve static files of reactjs
app.mount("/",StaticFiles(directory="static/",html=True),name="static")

# To start the server use --> uvicorn main:app --reload
