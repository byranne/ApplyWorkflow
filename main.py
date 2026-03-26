import time
from extract_links import get_latest_job_links
from scraper import scrape_and_filter_job
from generate_html import generate_html_dashboard

def main():
    print("Starting job link extraction...")
    urls = get_latest_job_links()
    print(f"Found {len(urls)} job URLs.")
    
    valid_jobs = []
    for i, url in enumerate(urls, 1):
        print(f"Processing job {i}/{len(urls)}: {url}")
        result = scrape_and_filter_job(url)
        if result[0] is not None:
            page_title, clean_text = result
            job_dict = {"title": page_title, "url": url, "description": clean_text}
            valid_jobs.append(job_dict)
            print(f"Added valid job: {page_title}")
        else:
            print("Job filtered out.")
        time.sleep(1)
    
    print(f"Total valid jobs: {len(valid_jobs)}")
    if valid_jobs:
        generate_html_dashboard(valid_jobs)
    else:
        print("No valid jobs to generate dashboard.")

if __name__ == "__main__":
    main()
