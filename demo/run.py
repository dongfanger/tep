from tep import run

if __name__ == '__main__':
    run({
        "path": ["report"],  # Relative path to tests, file or directory
        "report": 1  # Generate html report, 0: False, 1: True
    })
