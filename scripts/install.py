#!/usr/bin/python
# encoding=utf-8

import os
import shutil
import subprocess

if __name__ == '__main__':
    version = "3.0.0"
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    site_packages_path = os.path.join(base_path, "venv", "lib", "python3.8", "site-packages")
    os.chdir(base_path)
    dist_path = os.path.join(base_path, "dist")
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
    os.system("poetry install --only main")
    os.system("poetry build")

    proc = subprocess.Popen(["pip", "uninstall", "tep"], stdin=subprocess.PIPE)
    proc.communicate(input="y".encode())
    os.chdir(site_packages_path)
    for name in os.listdir():
        if os.path.isdir(name) and name.startswith("tep"):
            shutil.rmtree(name)

    os.chdir(dist_path)
    os.system(f"pip install tep-{version}-py3-none-any.whl")
