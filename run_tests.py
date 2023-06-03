import sys
import os
import pytest

# Get the command-line arguments after the script name
pytest_args = sys.argv[1:]

# Check if a specific test is provided
if "--test" in pytest_args:
    # Get the index of the "--test" argument
    index = pytest_args.index("--test")

    # Get the specific test in the format "test_file.py::test_function" from the next argument
    specific_test = pytest_args[index + 1]

    # Remove the "--test" argument and the specific test from the pytest arguments
    del pytest_args[index : index + 2]

    # Split the specific test by '::' to separate the file path and the test
    parts = specific_test.split("::")

    # Check if the file path is provided
    if len(parts) > 1:
        file_path = parts[0]

        # Get the absolute path of the test file
        abs_file_path = os.path.abspath(file_path)

        # Construct the test path with the absolute file path and the test function
        test_path = "::".join([abs_file_path] + parts[1:])

        # Append the modified test path to the pytest arguments
        pytest_args.append(test_path)
    else:
        pytest_args.append(os.path.abspath(parts[0]))

# Run pytest with the provided arguments
pytest.main(pytest_args)
