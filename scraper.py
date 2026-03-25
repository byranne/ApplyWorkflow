import requests
from bs4 import BeautifulSoup

def scrape_and_filter_job(url):
    try:
        # Standard User-Agent header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;x x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the HTML
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract visible text
        text = soup.get_text()
        
        # Clean the text: strip extra whitespace and convert to lowercase
        cleaned_text = ' '.join(text.split()).lower()
        
        # Tier 1 Filter: Absolute Rejections
        tier1_keywords = ['apprenticeship', 'full-time', 'full time']
        for kw in tier1_keywords:
            if kw in cleaned_text:
                print(f"Rejected: Contains '{kw}'")
                return None
        
        # Tier 2 Filter: Grad-Student Check
        grad_keywords = ['master', "master's", 'ms ', 'phd', 'ph.d']
        undergrad_keywords = ['bachelor', 'bs ', 'b.s', 'undergrad']
        
        has_grad = any(kw in cleaned_text for kw in grad_keywords)
        has_undergrad = any(kw in cleaned_text for kw in undergrad_keywords)
        
        if has_grad and not has_undergrad:
            print("Skipping: Grad-only role")
            return None
        
        # If passes all filters, return the cleaned text
        return cleaned_text
    
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Test the function with a sample URL
    # Replace with a real job URL from simplify.jobs for actual testing
    test_url = "https://simplify.jobs/p/4475bfac-4218-4b36-9bec-5ebb2c6694a0/Degree-Apprenticeship-in-Data--AI?utm_source=swelist"  # Simple test page; change to a real job URL
    result = scrape_and_filter_job(test_url)
    if result:
        print("Test passed. Extracted text preview:", result[:200] + "...")
    else:
        print("Test filtered out or error occurred.")
