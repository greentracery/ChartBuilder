#!/usr/bin/env bash

# Create virtual environment:
python3.8 -m venv ../v38

# Activate virtual environment:
source ../v38/bin/activate

#  Check python & pip version, package list:
python -V
pip -V
pip list

# (optional) upgrade pip:
pip install --upgrade pip

# (optional) install requirements
#pip install -r requirements.txt

pip install dist/ChartBuilder-1.0.tar.gz

pip list
