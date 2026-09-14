import subprocess
import os

package_lst = [
    "uv==0.7.11"
    ,"mlflow==2.22.1"
    ,"langchain==0.3.25"
    ,"langgraph==0.3.4"
    ,"databricks-agents==0.22.1"
    ,"databricks-langchain==0.5.1"
    ,"pydantic==2.11.5"
    ,"unitycatalog-langchain==0.2.0"
    ]


def download_all_wheels(package_lst):
    download_dir = "downloaded_wheels"
    os.makedirs(download_dir, exist_ok=True)

    for package_name in package_lst:

        print(f"Downloading {package_name}...")
            
        subprocess.run([
            "pip", "download", package_name,
            "--dest", download_dir,
            "--only-binary=:all:",   
            "--prefer-binary"
            ])
        
        print(f"Downloaded {package_name} to {download_dir}")


download_all_wheels(package_lst)

