import pathlib

import pytest

def create_positive_tests(success: int, filepath: pathlib.Path):
    content = """
import pytest

def test_number():
    assert 5 == 5
    
def test_string():
    assert 'hello' == 'hello'
    
"""
    with open(str(filepath), 'w') as file:
        file.write(content)








def create_pytest_report(report_path, success: int, failed: int):
    test_path = report_path / "tests"
    test_path.mkdir()
    create_positive_tests(success, test_path / "test_pos.py")
    #create_negative_tests(failed)
    #run_pytest

    return ""
