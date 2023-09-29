"""
This module provides a post-install script for a Python package.

The script performs the following tasks:
1. Installs the `transformers[torch]` package using pip.
2. Modifies the `chromadb` package to use `pysqlite3` instead of the default `sqlite3`.
"""

import subprocess
import os
import sys


def add_pysqlite3_to_chroma():
    """
    Modifies the `chromadb` package to use `pysqlite3` instead of the default `sqlite3`.

    This function searches for the line "import sqlite3" in the `__init__.py` file of
    the `chromadb` package and replaces it with the provided multi-line string to use `pysqlite3`.
    """
    # Path to the chromadb __init__.py file
    chromadb_init_path = os.path.join(
        sys.prefix, "lib", "python3.10", "site-packages", "chromadb", "__init__.py"
    )

    # Code to replace
    replacement_code = """
__import__('pysqlite3')
import sys
import pysqlite3 as sqlite3
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
"""

    # Read the file content
    with open(chromadb_init_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    # Search for the line and replace
    for index, line in enumerate(content):
        if line.strip() == "import sqlite3":
            content[index] = replacement_code
            break

    # Write the modified content back to the file
    with open(chromadb_init_path, "w", encoding="utf-8") as file:
        file.writelines(content)

    print("Modified chroma to use pysqlite3 successfully!")


def pip_install_transformers_torch():
    """
    Installs the `transformers[torch]` package using pip.

    This function uses the subprocess module to run the pip install command for
    `transformers[torch]`. It checks the return code to ensure successful installation.
    """
    result = subprocess.run(["pip", "install", "transformers[torch]"], check=True)
    if result.returncode != 0:
        print("Error installing transformers[torch].")
        sys.exit(1)
    else:
        print("Installed transformers[torch] successfully!")


def main():
    """
    The main function of the post-install script.
    """
    pip_install_transformers_torch()
    add_pysqlite3_to_chroma()


if __name__ == "__main__":
    main()
