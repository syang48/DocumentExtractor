import fitz
import os
import subprocess
import shutil
from pathlib import Path

def get_soffice_path():
    """Locates LibreOffice binary for docx conversion."""
    search_paths = [
        '/opt/homebrew/bin/soffice',
        '/usr/bin/soffice',
        '/usr/bin/libreoffice'
    ]
    for path in search_paths:
        if os.path.exists(path): return path
    return shutil.which('soffice') or shutil.which('libreoffice')

def convert_to_png(file_path, original_filename):
    """
    Converts docx/pdf to png. The resulting PNG is stored in a folder 
    named after the file. Intermediate PDFs are NOT saved.
    """
    # 1. Setup the Job Folder
    base_name = Path(original_filename).stem
    job_dir = Path("storage/output") / base_name
    job_dir.mkdir(parents=True, exist_ok=True)
    
    png_path = job_dir / f"{base_name}.png"
    temp_pdf_path = None

    try:
        # 2. Identify the PDF Source
        if original_filename.lower().endswith(".docx"):
            soffice_bin = get_soffice_path()
            if not soffice_bin:
                print("CRITICAL: 'soffice' not found.")
                return None
            
            # Convert DOCX to a temporary PDF inside the job folder
            subprocess.run([
                soffice_bin, '--headless', '--convert-to', 'pdf', 
                '--outdir', str(job_dir.absolute()), 
                os.path.abspath(file_path)
            ], check=True, capture_output=True)
            
            temp_pdf_path = job_dir / f"{base_name}.pdf"
            pdf_to_open = str(temp_pdf_path)
        else:
            # If it's already a PDF, just point to the original upload path
            pdf_to_open = file_path

        # 3. Process with PyMuPDF (Extract PNG)
        doc = fitz.open(pdf_to_open)
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(str(png_path))
        doc.close()

        # 4. Cleanup: Remove the temporary PDF if it was created
        if temp_pdf_path and temp_pdf_path.exists():
            temp_pdf_path.unlink()

        print(f"SUCCESS: PNG saved to {job_dir}")
        return str(png_path)

    except Exception as e:
        print(f"ERROR: {e}")
        # Cleanup PDF on failure as well
        if temp_pdf_path and temp_pdf_path.exists():
            temp_pdf_path.unlink()
        return None