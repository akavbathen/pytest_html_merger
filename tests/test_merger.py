import pathlib
import time

import pytest
import pytest_html_merger.main as phm
from bs4 import BeautifulSoup
from tests.conftest import create_pytest_report, TestPath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re



def test_title(custom_tmp_path: TestPath):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=2)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "merged"

        ]
    )

    with open(custom_tmp_path.result_file_name, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.select_one("#head-title").string
    assert title == "merged"


def test_h1_title(custom_tmp_path: TestPath):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=10, failed=2)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "merged"

        ]
    )

    with open(custom_tmp_path.result_file_name, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    title = soup.select_one("#title").string
    assert title == "merged"


def test_report_created(custom_tmp_path: TestPath):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=10, failed=2)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "html_report"

        ]
    )

    assert custom_tmp_path.result_file_name.exists()

def test_the_number_of_failures_indicated_in_the_report(custom_tmp_path, element=None):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=2, failed=2)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "html_report"

        ]
    )
    with open(custom_tmp_path.result_file_name, "r") as f:
        html_content: str = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    element = soup.find('span', class_='failed')
    text = element.get_text()

    parts = text.split(' ')
    res = (parts[0].strip())
    assert res == '3'



@pytest.mark.parametrize("payTest", [
    ("3.2.0"),        # test case 1
    ("4.1.1")   # test case 2

])
def test_checking_the_number_of_failed_and_success_records(custom_tmp_path: TestPath ,payTest):
    venv_path = custom_tmp_path.venv_path / f"venv{payTest}"

    create_pytest_report(venv_path, custom_tmp_path.input_path, success=2, failed=2)
    create_pytest_report(venv_path, custom_tmp_path.input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "html_report"

        ]
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{custom_tmp_path.result_file_name}'
    driver.get(file_path)

    elements_failed = driver.find_elements(By.CSS_SELECTOR, ".results-table-row.failed")
    elements_success = driver.find_elements(By.CSS_SELECTOR, ".results-table-row.passed")
    assert len(elements_failed) == 3 and len(elements_success) == 3


@pytest.mark.parametrize("payTest", [
    ("3.2.0"),        # test case 1
    ("4.1.1")   # test case 2

])
def test_Version_check_pytest(custom_tmp_path, payTest):
    start_time = time.time()
    subfolder: pathlib.Path = custom_tmp_path.tmp_path/ "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path.tmp_path/ "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path.venv_path / f"venv{payTest}"


    create_pytest_report(venv_path, input_path, success=2, failed=2)
    create_pytest_report(venv_path, input_path, success=1, failed=1)

    phm.main(
        [
            "--input",
            str(input_path),
            "-o",
            str(file_name),
            "-t",
            "html_report"

        ]
    )


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{file_name}'
    driver.get(file_path)

    p_element = driver.find_element(By.CSS_SELECTOR, 'p')
    texts = p_element.text
    version = texts[-5:]
    assert version == payTest

    end_time = time.time()
    duration = end_time - start_time
    print(f"The function took {duration} seconds to execute.")

def test_The_date_the_report_was_created(custom_tmp_path):
    today = datetime.today().date()

    subfolder: pathlib.Path = custom_tmp_path.tmp_path / "results"
    subfolder.mkdir(exist_ok=True, parents=True)
    file_name: pathlib.Path = subfolder / "result.html"

    input_path = custom_tmp_path.tmp_path / "input_reports"
    input_path.mkdir(exist_ok=True)
    venv_path = custom_tmp_path.venv_path / "venv4.1.1"

    create_pytest_report(venv_path, input_path, success=10, failed=2)
    create_pytest_report(venv_path, input_path, success=1, failed=1)
    phm.main(
        [
            "--input",
            str(input_path),
            "-o",
            str(file_name),
            "-t",
            "html_report"

        ]
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{file_name}'
    driver.get(file_path)

    p_element = driver.find_element(By.TAG_NAME, 'p')
    text = p_element.text
    pattern = r'^.+ (\d{2}-.+-\d{4})'
    match = re.search(pattern, text)
    date_str = match.group(1)

    date_obj = datetime.strptime(date_str, '%d-%b-%Y').date()
    assert date_obj == today


def test_Creating_and_testing_Skip(custom_tmp_path):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=10, failed=2, skip=1)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1, skip=2)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "html_report"

        ]
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{custom_tmp_path.result_file_name}'
    driver.get(file_path)

    c_element = driver.find_element(By.CLASS_NAME,"skipped")
    text_c_element = c_element.text
    number_of_test = text_c_element.split()[0]
    assert int(number_of_test) == 3

def test_Creating_and_testing_Eror(custom_tmp_path):
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1, skip=1, eror=1)
    create_pytest_report(custom_tmp_path.venv_path_4, custom_tmp_path.input_path, success=1, failed=1, skip=2, eror=1)
    phm.main(
        [
            "--input",
            str(custom_tmp_path.input_path),
            "-o",
            str(custom_tmp_path.result_file_name),
            "-t",
            "html_report"

        ]
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    file_path = f'file://{custom_tmp_path.result_file_name}'
    driver.get(file_path)

    e_element = driver.find_element(By.CLASS_NAME,"error")
    text_c_element = e_element.text
    number_of_test = text_c_element.split()[0]
    assert int(number_of_test) == 2
