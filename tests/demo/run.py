from tep.libraries.Run import Run

if __name__ == '__main__':
    settings = {
        "path": ["test_demo.py"],  # Path to run, relative path to case
        "report": False,  # Output test report or not
        "report_type": "pytest-html"  # "pytest-html" "allure"
    }
    Run(settings)
