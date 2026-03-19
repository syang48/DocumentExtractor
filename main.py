import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.converter import convert_to_png
from services.processor import extract_elements
from dotenv import load_dotenv

load_dotenv() # Loads settings from .env
app = FastAPI()

# Connect the frontend folder so you can visit http://localhost:8000/
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Essential: Allows your HTML to talk to your Python code
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    
    # Keep original extension (.docx or .pdf)
    ext = os.path.splitext(file.filename)[1] 
    upload_path = f"storage/uploads/{job_id}{ext}"

    with open(upload_path, "wb") as f:
        f.write(await file.read())

    # Now the converter handles the rest
    png_path = convert_to_png(upload_path, job_id)
    
    if png_path:
        return extract_elements(png_path)
    return {"error": "Conversion failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)