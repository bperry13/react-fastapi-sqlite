#!/bin/bash
#must be ran from project root directory

#create virtual environment
if [ -d "env/" ]; then 
        echo "Directory exists." 
else 
        python3 -m venv env
fi

#start virtual environment
source env/bin/activate
#install requirements
pip3 install -r requirements.txt
#change directory to FastAPI
cd FastAPI
#start the FastAPI server
uvicorn main:app --reload