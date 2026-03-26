import html

def generate_html_dashboard(jobs_list):
    # Calculate stats
    total_jobs = len(jobs_list)
    intern_count = sum(1 for job in jobs_list if 'intern' in job['title'].lower() or 'intern' in job['description'].lower())
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Today's Jobs</title>
    <style>
        body {{
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #ffffff;
        }}
        .jobs {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .card {{
            background-color: #1e1e1e;
            border-radius: 8px;
            padding: 20px;
            margin: 10px;
            width: 300px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        .card h2 {{
            margin-top: 0;
            color: #ffffff;
        }}
        .card a {{
            color: #4fc3f7;
            text-decoration: none;
        }}
        .card a:hover {{
            text-decoration: underline;
        }}
        button {{
            background-color: #4fc3f7;
            color: #121212;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #29b6f6;
        }}
    </style>
</head>
<body>
    <h1>Today's Jobs ({total_jobs} total, {intern_count} internships)</h1>
    <div class="jobs">
"""

    for job in jobs_list:
        title = job.get('title', 'No Title')
        url = job.get('url', '#')
        description = job.get('description', 'No Description')
        description_escaped = html.escape(description)
        html_content += f"""
        <div class="card">
            <h2>{html.escape(title)}</h2>
            <a href="{html.escape(url)}" target="_blank">{html.escape(url)}</a>
            <button onclick="navigator.clipboard.writeText('{description_escaped}')">Copy Description</button>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    with open('Today_Jobs.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML dashboard 'Today_Jobs.html' generated successfully.")

if __name__ == "__main__":
    # Sample jobs list for testing
    jobs_list = [
        {
            "title": "Software Engineer Intern",
            "url": "https://simplify.jobs/p/example1",
            "description": "Develop software applications. Requires knowledge of Python and JavaScript."
        },
        {
            "title": "Data Analyst",
            "url": "https://simplify.jobs/p/example2",
            "description": "Analyze datasets and create reports. Experience with SQL preferred."
        }
    ]
    generate_html_dashboard(jobs_list)
