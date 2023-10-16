## Local Installation

The source code is provided as a Python package, and it can be simply installed with `pip`.
In Python it is common to work within virtual environments, so that the system installation does not become cluttered and the dependencies stay separate. We also provide instructions for these steps.

The required Python version is 3.9 or 3.10. Verify your Python version by executing the command `python --version`. These versions are currently available in most Linux distributions via the default package manager.
If these are not available, install the required version by following the instructions in [pyenv](https://github.com/pyenv/pyenv).

There are two ways to create the virtual environment and install the package.
The first is with [Poetry](https://python-poetry.org/). Poetry is a tool for developing Python packages. If this is installed in your system, running `poetry install` from the current directory will create a separate virtual environment and install all dependencies. In this case, you may proceed to section *Running*.

The other alternative is to manually create a virtual environment and install the dependencies within.
The commands to create the virtual environment, activate it and then install the package are:

    python -m venv <path>
    source <path>/bin/activate
    pip install .

where `<path>` can be any path of your preference, such as `.venv`

### Running

To execute both the notebooks and parts of this package, it is necessary to enter the virtual environment for each new shell.
Depending on the installation method, the commands are `poetry shell` or `source <path>/bin/activate`.
Now, we can now lauch the notebooks server with `python -m notebook notebooks` from the current directory. Follow the instructions in the browser.