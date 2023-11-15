## Setup

1. Setup virtual environment (once):  
`python3 -m venv venv`
2. Enter virtual environment mode:  
`. venv/bin/activate`
3. Install dependencies (once):  
`pip3 install -r requirements.txt`

To save a new requirements.txt file after installing new dependencies:  
`pip3 freeze > requirements.txt`

## Prepare for running after setup:
1. Enter virtual environment mode:  
`. venv/bin/activate`
2. See `Usage` below


## Usage

### prepare input and output folders, and csv file with input config
Script expects that input video files will be located 3 levels higher in directory tree, there will be multiple (any amount) of directories, where each directory will contain any amount of files on the 1 level.   
input file contains name of directory, name of file, and start/end merls in seconds to cut out of the input file. 
The same fiel can be listed multiple times with different marks. If one of marks is omited - start or end of the video is used as limit. 


If some output files already exist - they will be skipped, That's why it's safe to run script again in case it failed of stopped, or input filewas updated 

### 
```bash
python main.py
```