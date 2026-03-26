# SWEList Application Workflow

I built a script that enhances my workflow when applying to internships on SWEList. This script scrapes through the latest email for the day and collects all the job links only. It then filters through the postings disregarding the apprenticeships, fulltime, and grad only positions. It generates an Html file that details the title of a position, provides the specific link, and a copyable description of a role. 

Using the description you talor your resume accordingly. 

The organizeResume script helps me quickly rename my resume and archive past resumes I used in a seperate folder. Because I make my resume changes in LATEX on Overleaf, the script speeds up my workflow by taking the latest pdf downloaded in my downloads folder and moving it to the done folder with the correct name and then archives my old one. When the script is done we simply submit resume in the done folder to the job posting.


## Features

- **Email Link Extraction**: Pulls job links from labeled Gmail emails (from `noreply@swelist.com`)
- **Smart Job Filtering**: Rejects apprenticeships, grad-only roles, and full-time positions based on job title
- **Job Dashboard**: Generates an interactive HTML dashboard with job cards, clickable links, and copy-to-clipboard descriptions
- **Resume Organization**: Automatically organizes downloaded resumes with collision detection and archiving
- **Dashboard Stats**: Displays internship count and total job count at a glance

## Setup

### Requirements
```bash
pip install beautifulsoup4 requests
```

### Gmail Setup
1. Enable IMAP in Gmail settings
2. If using 2-factor authentication, generate an app password
3. Update `extract_links.py` sender address if needed

## Usage

### Full Workflow (Email → Dashboard)
```bash
python3 main.py
```
- Extracts job links from your Gmail inbox
- Scrapes and filters each job page
- Generates `Today_Jobs.html` with all valid internships

### Test HTML Generator (No Scraping)
```bash
python3 main.py test
```
- Quickly validates the dashboard without fetching URLs

### Organize Resumes
```bash
python3 organizeResumes.py
```
- Finds most recent PDF in Downloads
- Prompts for company name
- Saves as `First_Last_Resume_CompanyName.pdf` in ResumeDone
- Moves old resumes to ArchivedResumes
- Detects naming conflicts and prompts for alternatives

## File Structure

| File | Purpose |
|------|---------|
| `extract_links.py` | Connects to Gmail, extracts simplify.jobs URLs |
| `scraper.py` | Fetches job pages, filters by title keywords |
| `generate_html.py` | Creates interactive HTML dashboard |
| `main.py` | Orchestrates full workflow; includes test mode |
| `organizeResumes.py` | Manages resume downloads and archiving |
| `Today_Jobs.html` | Generated dashboard (output) |

## How It Works

1. **Extract**: Pulls latest email from `noreply@swelist.com` and finds all `simplify.jobs/p/` links
2. **Filter**: Checks job titles against exclusion keywords (`apprentice`, `graduate`, `phd`, `master`, `full-time`)
3. **Scrape**: Extracts clean job description text from HTML body
4. **Generate**: Creates styled dashboard with clickable links and copy buttons
5. **View**: Open `Today_Jobs.html` in browser to browse jobs

## Dashboard Features

- **Copy Button**: One-click description copy to clipboard with "Copied!" confirmation
- **Direct Links**: Click to open job posting in new tab
- **Job Stats**: See total jobs and internship count at the top
- **Dark Mode**: Sleek dark theme for easy reading

## Notes

- Job scraping includes 1-second delays between pages to avoid server strain
- Resumes are named `First_Last_Resume_{CompanyName}.pdf` for easy organization
- All filters are based on job **title** keywords to avoid false positives from company bios
- Copies are case-insensitive for robustness
