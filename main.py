import os
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


def test_generate_html_dashboard():
    """Quick test: don't rerun web scraping; just verify HTML generator output."""
    print("Running generate_html_dashboard test...")
    sample_jobs = [
        {
            "title": "Test Intern Role",
            "url": "https://simplify.jobs/p/test1",
            "description": "Test description for copy button check."
        }
    ]

    # Generate the HTML
    generate_html_dashboard(sample_jobs)

    # Verify file exists and contains expected elements
    out_path = "Today_Jobs.html"
    if not os.path.exists(out_path):
        raise AssertionError("Today_Jobs.html not created")

    content = open(out_path, "r", encoding="utf-8").read()
    assert "Test Intern Role" in content, "Job title not found in output"
    assert "Copy Description" in content, "Copy button missing"
    assert "Copied!" in content or "copyDescription" in content, "Copy script status handling missing"

    print("Test generate_html_dashboard passed!")


if __name__ == "__main__":
    main()
