from .base import BaseContentHandler
import os
import subprocess
import shutil
from urllib.parse import urlparse

class GitHubHandler(BaseContentHandler):
    def handle(self, url, output_dir):
        parsed_url = urlparse(url)
        repo_name = parsed_url.path.split('/')[-1]
        project_folder = os.path.join(output_dir, "external_resources", repo_name)
        
        # Remove the directory if it already exists
        if os.path.exists(project_folder):
            shutil.rmtree(project_folder)
            print(f"Removed existing directory: {project_folder}")
        
        # Clone the repository
        try:
            subprocess.run(['git', 'clone', url, project_folder], check=True)
            print(f"Repository {repo_name} cloned into {project_folder}")
        except subprocess.CalledProcessError:
            print(f"Failed to clone repository: {url}")