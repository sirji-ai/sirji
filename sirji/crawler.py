import os
import requests
from bs4 import BeautifulSoup
import PyPDF2
import subprocess
from urllib.parse import urlparse

def crawl_url(url):
    """
    Crawls a given URL and handles the content based on its type:
    - Web page: Extracts and prints the title.
    - PDF: Reads the first page and prints its content.
    - GitHub repo: Clones the repo into a specified directory.
    """
    # Determine the content type from the URL
    if url.endswith('.pdf'):
        crawl_pdf(url)
    elif 'github.com' in url:
        clone_github_repo(url)
    else:
        crawl_web_page(url)

def crawl_web_page(url):
    """Fetches and prints the title of a web page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Web page text: {soup.get_text()}")

def crawl_pdf(url):
    """Downloads and reads the first page of a PDF."""
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    with open('temp.pdf', 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        print("Contents of the PDF file are:")
        for page in reader.pages:
            print(page.extract_text())

    os.remove('temp.pdf')  # Clean up the temporary file

def clone_github_repo(url):
    """Clones a GitHub repository into a specific directory."""
    parsed_url = urlparse(url)
    repo_name = parsed_url.path.split('/')[-1]
    project_folder = f"workspace/{repo_name}"
    if not os.path.exists(project_folder):
        os.makedirs(project_folder)
    subprocess.run(['git', 'clone', url, project_folder], check=True)
    print(f"Repository {repo_name} cloned into {project_folder}")

