import pathlib

import pytest

def create_positive_tests(success: int, filepath: pathlib.Path):

    content = """
import pytest

"""
    b = """
def test_number():
    assert 5 == 5
 """

    for i in range(success):
        content += b.replace("test_number", f"test_number_{i}")
    

    with open(str(filepath), 'w') as file:
        file.write(content)

def create_negative_tests(failed: int, filepath: pathlib.Path):
    content = """
    import pytest

    """
    b = """
    def test_number():
        assert 5 == 2
     """

    for i in range(failed):
        content += b.replace("test_number", f"test_number_{i}")

    with open(str(filepath), 'w') as file:
        file.write(content)

def create_pytest_report(report_path, success: int, failed: int):
    test_path = report_path / "tests"
    test_path.mkdir(exist_ok=True)
    create_positive_tests(success, test_path / "test_pos.py")
    create_negative_tests(failed, test_path / "test_neg.py")
    #create_negative_tests(failed)
    #run_pytest

    return ""
