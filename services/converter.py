import fitz
import os
import subprocess
import shutil

def convert_to_png(file_path, job_id):
    """
    Converts DOCX or PDF to PNG. 
    Uses LibreOffice for DOCX -> PDF, then PyMuPDF for PDF -> PNG.
    """
    # 1. Setup paths
    file_to_open = file_path 
    upload_dir = "storage/uploads"
    output_dir = "storage/output"
    
    # Ensure directories exist
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # 2. Handle Word Documents (Using LibreOffice/soffice)
    if file_path.lower().endswith(".docx"):
        final_pdf_path = os.path.join(upload_dir, f"{job_id}.pdf")
        
        # LibreOffice names output based on the input filename
        base_name = os.path.basename(file_path)
        temp_pdf_name = os.path.splitext(base_name)[0] + ".pdf"
        temp_pdf_path = os.path.join(upload_dir, temp_pdf_name)

        print(f"DEBUG: Starting LibreOffice DOCX to PDF conversion...")
        
        try:
            # We use 'soffice' in headless mode. 
            # Subprocess.run waits for completion, so no time.sleep(1) is needed.
            subprocess.run([
                'soffice', 
                '--headless', 
                '--convert-to', 'pdf', 
                '--outdir', upload_dir, 
                file_path
            ], check=True, capture_output=True)

            # LibreOffice doesn't let us pick the output filename directly, 
            # so we move/rename it to our expected job_id format.
            if os.path.exists(temp_pdf_path):
                shutil.move(temp_pdf_path, final_pdf_path)
                file_to_open = final_pdf_path
            else:
                # Fallback check: if the user uploaded a file with the same name as job_id
                if os.path.exists(final_pdf_path):
                    file_to_open = final_pdf_path
                else:
                    print(f"ERROR: LibreOffice finished but PDF was not found.")
                    return None
                
        except subprocess.CalledProcessError as e:
            print(f"DEBUG: LibreOffice error: {e.stderr.decode() if e.stderr else e}")
            return None
        except Exception as e:
            print(f"DEBUG: Unexpected conversion error: {e}")
            return None

    # 3. Open the PDF (original or converted) and convert to PNG
    try:
        if not os.path.exists(file_to_open):
            print(f"ERROR: File not found at {file_to_open}")
            return None

        # Process with PyMuPDF (fitz)
        doc = fitz.open(file_to_open)
        
        # Ensure the document actually has pages
        if len(doc) == 0:
            print("ERROR: PDF has no pages.")
            return None
            
        page = doc[0]  # Get first page
        
        # matrix=fitz.Matrix(2, 2) provides 2x zoom for better PNG quality
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        
        output_png = os.path.join(output_dir, f"{job_id}.png")
        pix.save(output_png)
        doc.close()
        
        print(f"SUCCESS: Created {output_png}")
        return output_png

    except Exception as e:
        print(f"FITZ ERROR: {e}")
        return None
