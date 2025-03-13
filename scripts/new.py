#!/usr/bin/python
# encoding=utf-8

import os
import shutil

if __name__ == '__main__':
    new_project_name = 'demo'

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(base_path))
    new_project_path = os.path.join(os.path.dirname(base_path), new_project_name)
    if os.path.exists(new_project_path):
        shutil.rmtree(new_project_path)
    os.system(f'tep new {new_project_name}')
