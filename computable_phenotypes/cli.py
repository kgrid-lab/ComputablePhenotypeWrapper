#!/usr/bin/env python3

import argparse
import json
import sys
from io import StringIO

import computable_phenotypes.utils_mssql.utils as mssql_utils
import computable_phenotypes.utils_sqlite.utils as sqlite_utils
from computable_phenotypes.utils import is_csv, is_json

def main():
    parser = argparse.ArgumentParser(
        description="""**Classify patients and return inclusion encounters:**
    This api could be used to process multiple patients data, including their
    encounters and diagnoses and to classify them for Nephrotic Syndrome. It 
    receives patient data in either JSON or CSV format, applies computable 
    phenotype, and returns a list of inclusion encounters.  For more detail 
    on the implementation and input data format please check our GitHub repository.
    
    **Sample input data:**
    Sample input data (CSV and JSON) can be found in the GitHub repository under 
    the 'input_test_data' folder: [Link to GitHub Repository](https://github.com/kgrid-lab/nephroticsyndrome-computablephenotype/tree/main/input_test_data)

    **Implementation:**
    The implementation of this app is available on GitHub:
    [Link to GitHub Repository](https://github.com/kgrid-lab/ComputablePhenotypeWrapper)

    **Returns:**
    List of inclusion encounters that meet the criteria.
        """,
        epilog="""
    Examples:
    python -m nephroticsyndrome_computablephenotype.cli input_test_data/sample_input.json
    classify input_test_data/sample_input.json (see readme to configure)
    input_test_data/sample_input.json | classify
    input_test_data/sample_input.json | classify > ouput.json
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "filename",
        nargs="?",
        type=str,
        help="The file that contains patient data in either JSON or CSV format.",
    )
    
    parser.add_argument(
        "--db_type",
        type=str,
        required=False,  # Use required=False if you want it to be optional
        help="The type of database to use. Your options are 'sqlite' and 'sql_server'. sqllite does not require any environment preparation while sql server needs to be installed and setup for sql_server.",
    )

    args = parser.parse_args()

    if args.filename:
        try:
            with open(args.filename, "rb") as file:
                content = file.read()
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        content = sys.stdin.buffer.read()

    if is_csv(content):
        if args.db_type == "sql_server":
            print(mssql_utils.process_csv(StringIO(content.decode("utf-8"))))
        else:
            print(sqlite_utils.process_csv(StringIO(content.decode("utf-8"))))

    elif is_json(content):
        patients_list = json.loads(content)
        if args.db_type == "sql_server":
            print(mssql_utils.process_json(patients_list))
        else:
            print(sqlite_utils.process_json(patients_list))

    else:
        print("Input data must be json or csv")

if __name__ == "__main__":
    main()


# Make the script executable:
# On Unix/Linux/macOS:
# chmod +x cli.py

# run using
# python cli.py myfile.txt
# or if made executable using
# ./cli.py myfile.txt

# To use it as a command named classify anywhere from the command line:

# a. Move the cli.py file to a directory that is on your system's PATH, or b. Add the directory where cli.py is located to your system's PATH, or c. Create a symbolic link to cli.py in a directory that is already on your PATH (e.g., /usr/local/bin/).

# On Unix/Linux/macOS:
# ```sh
# ln -s /path/to/cli.py /usr/local/bin/cli
# ```
# Note that `/usr/local/bin/` is usually in your PATH. The specific location where you should link your script might vary.
# If you don't want to move or modify the PATH, you can add an alias in your shell configuration file (like .bashrc or .zshrc):

# alias classify='/path/to/cli.py'
# After adding the alias, you may need to reload the shell configuration using source ~/.bashrc or restart your terminal.

#  call using cat input_test_data/sample_input.json | classify > ouput.json
