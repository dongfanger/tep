import os

from run import open_allure_report


def pytest_sessionfinish(session):
    allure_report_dir = session.config.getoption('allure_report_dir')
    if allure_report_dir:
        html_dir = os.path.join(allure_report_dir, 'html')
        os.system(f'mkdir {html_dir}')
        os.system(f"allure generate {allure_report_dir} -o {html_dir}")
        if open_allure_report:
            os.system(f"allure open {html_dir}")