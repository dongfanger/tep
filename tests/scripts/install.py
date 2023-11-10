#!/usr/bin/python
# encoding=utf-8

import os
import shutil
import subprocess

from tep import __version__

if __name__ == '__main__':
    tep_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    os.chdir(tep_path)
    dist_path = os.path.join(tep_path, "dist")
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
    os.system("poetry install --only main")
    os.system("poetry build")

    proc = subprocess.Popen(["pip", "uninstall", "tep"], stdin=subprocess.PIPE)
    proc.communicate(input="y".encode())
    os.chdir(r"/Users/wanggang888/Desktop/PycharmProjects/tep/venv/lib/python3.8/site-packages")
    for dir_name in os.listdir():
        if dir_name.startswith("tep"):
            shutil.rmtree(dir_name)

    os.chdir(dist_path)
    os.system(f"pip install tep-{__version__}-py3-none-any.whl")
