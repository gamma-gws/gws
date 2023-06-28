import shutil
import zipfile
import json
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def create_bin_folder():
    bin_path = Path("./bin")
    if not bin_path.exists():
        bin_path.mkdir()
        logging.info("Bin folder created")

def build_project():
    os.system("go build -o ./bin/gws.exe")
    logging.info("Project files built")

def read_repo_config():
    with open("gws-data.json", "r") as data_file:
        data = json.load(data_file)
        return data.get("repo_config")

def create_config_file(repo_config):
    config_data = {
        "port": ":8080",
        "domain": "localhost",
        "static_dir": "html",
        "tls_config": {
            "cert_file": "server.crt",
            "key_file": "server.key"
        },
        "repo_config": repo_config
    }

    with open("./bin/config.json", "w") as config_file:
        json.dump(config_data, config_file, indent=4)
    logging.info("Config created")

def copy_html_files():
    html_dest = Path("./bin/html")
    if html_dest.exists():
        shutil.rmtree(html_dest)
    shutil.copytree("html", html_dest)
    logging.info("Template code copied to bin")

def zip_bin_contents():
    release_zip_path = Path("./bin/Release.zip")
    if release_zip_path.exists():
        release_zip_path.unlink()

    with zipfile.ZipFile(release_zip_path, "w") as zip_file:
        for foldername, subfolders, filenames in os.walk("./bin"):
            for filename in filenames:
                if filename != "Release.zip":
                    file_path = Path(foldername) / filename
                    arcname = file_path.relative_to("./bin")
                    zip_file.write(file_path, arcname)

    logging.info("Content zipped to Release.zip")

def remove_gws_exe_tilde():
    gws_exe_tilde_path = Path("./bin/gws.exe~")
    if gws_exe_tilde_path.exists():
        gws_exe_tilde_path.unlink()
        logging.info("gws.exe~ file removed")

def main():
    try:
        create_bin_folder()
        build_project()
        repo_config = read_repo_config()
        create_config_file(repo_config)
        copy_html_files()
        zip_bin_contents()
        remove_gws_exe_tilde()
        logging.info("Build completed")
    except Exception as e:
        logging.error(f"Build failed: {e}")

if __name__ == "__main__":
    main()