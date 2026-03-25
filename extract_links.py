import imaplib
import email
import re
from email.header import decode_header

# Function to extract HTTP/HTTPS links from text
def extract_links(text):
    # Regex pattern to match HTTP and HTTPS URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`[\]]+'
    urls = re.findall(url_pattern, text)
    return urls

# Gmail IMAP server details
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Get user credentials
username = input("Enter your Gmail username: ")
password = input("Enter your Gmail password (or app password if 2FA is enabled): ")

# Sender to search for (replace with actual sender)
sender = 'noreply@swelist.com'

try:
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    
    # Login
    mail.login(username, password)
    
    # Select the mailbox (inbox)
    mail.select('inbox')
    
    # Search for emails from the specified sender, sorted by date descending
    # Gmail supports SORT
    status, data = mail.sort('(DATE)', 'UTF-8', 'FROM', sender)
    
    if status == 'OK' and data[0]:
        # Get the most recent email ID
        latest_email_id = data[0].split()[-1]
        
        # Fetch the email
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        
        if status == 'OK':
            # Parse the email
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # Extract the body
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    elif part.get_content_type() == "text/html":
                        # For HTML, we can still extract links, but for simplicity, treat as text
                        html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        body += html_content
            else:
                body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Extract links
            links = extract_links(body)
            
            # Print the links
            if links:
                print("Extracted links:")
                for link in links:
                    print(link)
            else:
                print("No HTTP/HTTPS links found in the email body.")
        else:
            print("Failed to fetch the email.")
    else:
        print(f"No emails found from {sender}.")
    
    # Logout
    mail.logout()

except Exception as e:
    print(f"An error occurred: {e}")