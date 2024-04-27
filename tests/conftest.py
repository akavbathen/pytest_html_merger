import pathlib
import random
import string
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


def create_folder_name(base_name, num_letters=5):
    # Generate a random string of letters
    random_letters = ''.join(random.choices(string.ascii_letters, k=num_letters))

    # Append the random letters to the base folder name
    folder_name = f"{base_name}_{random_letters}"

    return folder_name

def create_pytest_report(report_path, success: int, failed: int):
    test_path: pathlib.Path = report_path / "tests"
    test_path.mkdir(exist_ok=True)

    base_folder_name = "tests"
    new_folder_name = create_folder_name(base_folder_name, 5)
    random_path: pathlib.Path = test_path / new_folder_name
    random_path.mkdir()

    create_positive_tests(success, random_path / "test_pos.py")
    create_negative_tests(failed, random_path / "test_neg.py")
    #run_pytest

    # TODO:: return report path
    return ""
