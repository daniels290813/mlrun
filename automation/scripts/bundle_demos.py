import os
import tarfile
from git import Repo
import shutil

# List of repositories to archive
repos = [
    {"url": "https://github.com/mlrun/demo-azure-ML.git", "name": "demo-azure-ML"},
    {"url": "https://github.com/mlrun/demo-ssfraud.git", "name": "demo-fraudss"},
    {"url": "https://github.com/mlrun/demo-fraud.git", "name": "demo-fraud"},
    # Add more repositories as needed
]

# Directory where repositories will be cloned and extracted
temp_dir = "demos"

# Create the temporary directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Clone each repository and extract its contents to the temporary directory
for repo_info in repos:
    print(f"cloning {repo_info['url']} with name {repo_info['name']} to {temp_dir}")
    repo_url = repo_info["url"]
    repo_name = repo_info["name"]

    # Clone the repository
    try:
        repo = Repo.clone_from(repo_url, os.path.join(temp_dir, repo_name))
    except Exception as e:
        print(f"could not clone repo {repo_url}")
        print(e)
    
# Create a tar archive of the temporary directory
with tarfile.open("demos.tar", "w") as tar:
    tar.add(temp_dir, arcname=os.path.basename(temp_dir))

print("Archive created successfully!")

# Cleanup: Delete the temporary directory
shutil.rmtree(temp_dir)
