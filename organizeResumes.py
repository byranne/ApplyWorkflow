import os
import shutil
from pathlib import Path

def main():
    # Step 1: Define folder paths relative to home directory
    home = Path.home()
    downloads = home / "Downloads"
    resume_done = home / "Desktop" / "ResumeDone"
    archived_resumes = home / "Desktop" / "ArchivedResumes"
    
    # Create ResumeDone and ArchivedResumes folders if they don't exist
    resume_done.mkdir(parents=True, exist_ok=True)
    archived_resumes.mkdir(parents=True, exist_ok=True)
    
    # Step 2: Get the Company/Role name from user input
    role_name = input("Enter the Company/Role name for this resume: ").strip()
    
    # Step 3: Archive existing BryanWongCV.pdf if it exists
    current_cv = resume_done / "BryanWongCV.pdf"
    if current_cv.exists():
        archived_name = f"BryanWongCV_{role_name}.pdf"
        archived_path = archived_resumes / archived_name
        shutil.move(str(current_cv), str(archived_path))
        print(f"Archived existing resume as: {archived_name}")
    else:
        print("No existing BryanWongCV.pdf found to archive.")
    
    # Step 4: Find the most recently created .pdf file in Downloads
    pdf_files = list(downloads.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in Downloads folder.")
        return
    
    # Get the most recent PDF
    most_recent_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
    
    # Step 5: Rename and move the most recent PDF to ResumeDone as BryanWongCV.pdf
    new_cv_path = resume_done / "BryanWongCV.pdf"
    shutil.move(str(most_recent_pdf), str(new_cv_path))
    
    # Step 6: Print success message
    print(f"Successfully moved and renamed {most_recent_pdf.name} to BryanWongCV.pdf in ResumeDone folder.")

if __name__ == "__main__":
    main()
