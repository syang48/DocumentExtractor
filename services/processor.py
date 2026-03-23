import cv2
import base64
import os
from pathlib import Path
from services.header_extractor import get_dynamic_header
from services.signature_extractor import get_signature_crop

def extract_elements(png_path):
    # 1. Setup Pathing
    # We derive the folder from the existing png_path
    current_png = Path(png_path)
    job_dir = current_png.parent
    base_name = current_png.stem # The filename without .png
    
    # Load the image
    img = cv2.imread(str(current_png))
    if img is None:
        return {"error": "File not found"}

    # 2. Perform Extractions
    header_cut = get_dynamic_header(img)
    signature_cut = get_signature_crop(img)

    # 3. Save physical files to the folder (The "History" Row)
    # We prefix these so they appear after the original conversion in the folder
    header_path = job_dir / f"{base_name}_header.png"
    signature_path = job_dir / f"{base_name}_signature.png"

    if header_cut is not None:
        cv2.imwrite(str(header_path), header_cut)
    
    if signature_cut is not None:
        cv2.imwrite(str(signature_path), signature_cut)

    # Helper function for Base64 (for your API response)
    def get_b64(image_array):
        if image_array is None:
            return None
        _, buffer = cv2.imencode('.png', image_array)
        return base64.b64encode(buffer).decode('utf-8')

    # 4. Return results (Paths + Base64)
    return {
        "header_text": "Header Found" if signature_cut is not None else "No Header Found",
        "header_img": get_b64(header_cut),
        "signature_text": "Signature Found" if signature_cut is not None else "No Signature Found",
        "signature_img": get_b64(signature_cut),
        "full_image": get_b64(img)
    }

