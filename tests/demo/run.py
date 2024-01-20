from tep.libraries.Run import Run

if __name__ == '__main__':
    settings = {
        "path": [r"test_flow.py"],  # Path to run, relative path to case
        "report": True,  # Output test report or not
    }
    Run(settings)
