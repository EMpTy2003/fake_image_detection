# fake_image_detection

This fake_image_detection provides an API for uploading an image file, performing image classification, and serving the results. The server also serves static files for a React.js frontend.

## Features

- Upload image files for classification.
- Perform image classification using a deep learning model.
- Serve the uploaded images and classification results.
- Serve static files for a React.js frontend.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/EMpTy2003/fake_image_detection.git
   cd your_project

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
## Usage
1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```
This will start the server, and you can access it at http://localhost:8000.

API Endpoints:

*  GET /api/v1: Test endpoint to check if the server is running.

 * POST /api/v1/uploadfile/: Upload an image file for classification. You can provide a custom filename if needed.

* GET /api/v1/get_image/{image_path}: Retrieve the classified image based on the image path.

3. To use the server with a React.js frontend, make sure to build the frontend and place the static files in the static/ directory.

Access the React.js frontend at http://localhost:8000 or customize the URL accordingly.

## Configuration
You can configure the server by modifying the main.py file and adjusting the FastAPI settings, such as CORS settings and file paths.
```bash
# Configuration settings
origins = ["*"]  # Configure allowed origins for CORS
upload_dir = Path("uploads")  # Configure the directory for uploaded files
image_dir = Path("out")  # Configure the directory for output images

```
