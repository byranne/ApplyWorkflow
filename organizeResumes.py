import os
import shutil
from pathlib import Path

def get_unique_resume_name(resume_done, archived_resumes):
    """Prompt user for company name and check for naming conflicts in BOTH directories."""
    while True:
        company_name = input("Enter the Company Name for the resume: ").strip()
        
        if not company_name:
            print("Company name cannot be empty. Please try again.")
            continue
        
        # Format the filename
        resume_filename = f"Bryan_Wong_Resume_{company_name}.pdf"
        resume_done_path = resume_done / resume_filename
        archived_path = archived_resumes / resume_filename
        
        # Check if this filename already exists in EITHER the done folder or archive
        if resume_done_path.exists():
            print(f"Resume with name '{resume_filename}' already exists in ResumeDone.")
            retry = input("Would you like to enter a different company name? (yes/no): ").strip().lower()
            if retry != 'yes' and retry != 'y':
                print("Skipping this resume.")
                return None
            continue
        
        if archived_path.exists():
            print(f"Resume with name '{resume_filename}' already exists in Archive.")
            retry = input("Would you like to enter a different company name? (yes/no): ").strip().lower()
            if retry != 'yes' and retry != 'y':
                print("Skipping this resume.")
                return None
            continue
        
        return resume_filename

def main():
    # Step 1: Define folder paths relative to home directory
    home = Path.home()
    downloads = home / "Downloads"
    resume_done = home / "Desktop" / "ResumeDone"
    archived_resumes = home / "Desktop" / "ArchivedResumes"
    
    # Create ResumeDone and ArchivedResumes folders if they don't exist
    resume_done.mkdir(parents=True, exist_ok=True)
    archived_resumes.mkdir(parents=True, exist_ok=True)
    
    # Step 2: Find the most recently created .pdf file in Downloads
    pdf_files = list(downloads.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in Downloads folder.")
        return
    
    # Get the most recent PDF
    most_recent_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
    print(f"Found most recent PDF: {most_recent_pdf.name}")
    
    # Step 3: Prompt user for company name and check for conflicts
    resume_filename = get_unique_resume_name(resume_done, archived_resumes)
    if resume_filename is None:
        return
    
    # Step 4: Move the newly downloaded PDF from Downloads to ResumeDone with new name
    resume_done_path = resume_done / resume_filename
    shutil.move(str(most_recent_pdf), str(resume_done_path))
    print(f"Successfully moved and renamed {most_recent_pdf.name} to {resume_filename} in ResumeDone folder.")
    
    # Step 5: Archive any existing resumes in ResumeDone folder to ArchivedResumes
    # (This effectively archives the old file and keeps the new one in ResumeDone)
    resume_done_files = list(resume_done.glob("*.pdf"))
    for pdf_file in resume_done_files:
        if pdf_file != resume_done_path:  # Don't move the file we just created
            archived_path = archived_resumes / pdf_file.name
            # If filename already exists in archive, skip it
            if not archived_path.exists():
                shutil.move(str(pdf_file), str(archived_path))
                print(f"Archived: {pdf_file.name}")
            else:
                print(f"Skipped archiving (already exists): {pdf_file.name}")

if __name__ == "__main__":
    main()
