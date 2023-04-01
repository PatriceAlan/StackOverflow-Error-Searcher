import requests
import subprocess
import webbrowser


def run_test(test_file):
    """
    This function executes the given Python test file and checks for errors.
    If it contains errors, it filters out the error type and error message from the Traceback.
    Otherwise, it prints "No errors found" on the console.
    """
    # Execute the test file using Popen method from the subprocess module
    process = subprocess.Popen(['python', test_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the stdout and stderr output from the executed command
    stdout, stderr = process.communicate()

    # Check if there is any error
    if process.returncode != 0:
        # Decode the binary object to UTF-8 string
        error_output = stderr.decode('utf-8')

        # Filter the error type and error message from the Traceback
        error_lines = error_output.strip().split('\n')
        error_type, error_message = error_lines[-1].split(':', 1)

        # Print the error type and error message
        print(f"Error: {error_type.strip()} - {error_message.strip()}")
    else:
        # No errors found
        print("No errors found")


url = "https://api.stackexchange.com/2.3/search"
params = {

    # "pagesize": 10,  # number of items to return per page
    "order": "desc",
    "sort": "votes",
    "tagged": "",
    # "answers": "1",
    "intitled": run_test('sample.py'),
    "site": "stackoverflow"
}
response = requests.get(url=url, params=params)
if response.ok:
    data = response.json()
    for item in data["items"]:
        if item["is_answered"]:
            webbrowser.open_new_tab(item["link"])
            # print(item["link"])
else:
    print("Error:", response.status_code, response.reason)
