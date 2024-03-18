import os
import requests
from bs4 import BeautifulSoup
import PyPDF2
from markdownify import markdownify as md
import subprocess
import shutil
from urllib.parse import urlparse

def crawl_urls(urls, output_dir):
    """
    Crawls a list of URLs and handles the content based on its type:
    - Web page: Converts to Markdown and saves.
    - PDF: Converts text to Markdown and saves.
    - GitHub repo: Clones the repo.
    """
    for url in urls:
        if url.endswith('.pdf'):
            crawl_pdf(url, output_dir)
        elif 'github.com' in url:
            clone_github_repo(url, output_dir)
        else:
            crawl_web_page(url, output_dir)

def crawl_web_page(url, output_dir):
    """Fetches a web page, converts it to Markdown, and saves."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    markdown_content = md(str(soup), heading_style="ATX")
    save_content(markdown_content, url, output_dir, 'md')

def crawl_pdf(url, output_dir):
    """Downloads a PDF, reads its text, converts to Markdown, and saves."""
    response = requests.get(url)
    temp_pdf_path = os.path.join(output_dir, 'temp.pdf')
    with open(temp_pdf_path, 'wb') as f:
        f.write(response.content)
    with open(temp_pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text_content = '\n'.join(page.extract_text() for page in reader.pages if page.extract_text())
    markdown_content = md(text_content)  # Basic conversion, might need manual editing
    save_content(markdown_content, url, output_dir, 'md')
    os.remove(temp_pdf_path)  # Clean up the temporary file

def clone_github_repo(url, output_dir):
    """Clones a GitHub repository into the external_resources directory within the specified output directory.
    Overwrites the directory if it already exists."""
    parsed_url = urlparse(url)
    repo_name = parsed_url.path.split('/')[-1]
    project_folder = os.path.join(output_dir, "external_resources", "github_repos", repo_name)
    
    # Remove the directory if it already exists
    if os.path.exists(project_folder):
        shutil.rmtree(project_folder)
        print(f"Removed existing directory: {project_folder}")
    
    # Create the directory and clone the repository
    os.makedirs(project_folder)
    subprocess.run(['git', 'clone', url, project_folder], check=True)
    print(f"Repository {repo_name} cloned into {project_folder}")


def save_content(content, url, output_dir, extension):
    """Saves the given content to a file in the specified directory."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "index"
    filename = f"{filename}.{extension}"
    output_path = os.path.join(output_dir, "external_resources", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {output_path}")
