#!/bin/bash

# install the project as a local package to have
# visibility of other modules
python -m pip install -e .

# run the main application
python -B ./src/main.py