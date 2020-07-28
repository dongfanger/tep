import os
import shutil

from tep.funcs import current_date

project_dir = os.path.dirname(os.path.abspath(__file__))

api_dir = os.path.join(project_dir, 'api')

testcases_dir = os.path.join(project_dir, 'testcases')

datafiles_dir = os.path.join(project_dir, 'datafiles')

reports_dir = os.path.join(project_dir, 'reports')

log_file = os.path.join(reports_dir, current_date() + '.log')

api_record_file = os.path.join(reports_dir, "api-record-" + current_date() + ".csv")

allure_report_dir = os.path.join(reports_dir, 'report-' + current_date())

# choose path to run tests
run_dir = os.path.join(testcases_dir, '')

# open allure test report automatically after testing
open_allure_report = 1

if __name__ == '__main__':

    if os.path.exists(allure_report_dir):
        shutil.rmtree(allure_report_dir)
    os.makedirs(allure_report_dir)

    os.system(f'pytest -v {run_dir} --alluredir {allure_report_dir}')
