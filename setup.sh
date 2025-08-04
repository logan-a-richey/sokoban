#!/bin/bash 

set -e 

echo "Starting Sokoban setup ..."

python3 -m venv venv
echo "venv - ok"

. venv/bin/activate 
echo "venv activation - ok"

sudo apt update 
sudo apt install python3-tk

pip install -r requirements.txt 
echo "requirements - ok"

./sokoban_app.py

