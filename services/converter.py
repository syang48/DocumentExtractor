import fitz
import os
import time
from docx2pdf import convert

def convert_to_png(file_path, job_id):
    # Determine the file to open with fitz
    file_to_open = file_path 

    # 1. Handle Word Documents
    if file_path.lower().endswith(".docx"):
        pdf_output = f"storage/uploads/{job_id}.pdf"
        print(f"DEBUG: Starting DOCX to PDF conversion...")
        
        try:
            # The conversion often works even if it throws an error at the very end
            convert(file_path, pdf_output)
        except Exception as e:
            print(f"DEBUG: Ignored docx2pdf error: {e}")
            # We continue because the PDF is likely already saved
        
        # Give Windows a moment to finish writing the file to disk
        time.sleep(1) 
        file_to_open = pdf_output

    # 2. Open the PDF and convert to PNG
    try:
        if not os.path.exists(file_to_open):
            print(f"ERROR: File not found at {file_to_open}")
            return None

        doc = fitz.open(file_to_open)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        output_png = f"storage/output/{job_id}.png"
        pix.save(output_png)
        doc.close()
        
        print(f"SUCCESS: Created {output_png}")
        return output_png

    except Exception as e:
        print(f"FITZ ERROR: {e}")
        return None