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
        
        # Remove navbar pollution: strip script, style, header, footer, nav, and aside tags
        for tag in soup.find_all(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        
        # Extract title
        page_title = soup.title.string.strip() if soup.title else "No Title"
        
        # Extract visible text
        text = soup.get_text(separator=' ')
        
        # Clean the text: strip extra whitespace and convert to lowercase
        cleaned_text = ' '.join(text.split()).lower()
        
        # FILTER: title exclusion keywords
        exclusion_keywords = ['apprentice', 'graduate', 'phd', 'ph.d', 'master', 'full-time', 'full time']
        title_lower = page_title.lower()

        for keyword in exclusion_keywords:
            if keyword in title_lower:
                print(f"Skipping: {keyword} found in title")
                return None, None

        # If no exclusion keywords in title, accept as valid internship
        return page_title, cleaned_text
    
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None