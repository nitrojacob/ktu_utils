# ktu\_utils
Utility scripts to help APJAKTU teachers with tasks like result analysis

## Scripts
result\_analysis.py

Perform KTU result analysis on an xls student marks downloaded from app.ktu.edu.in
Output is fixed width tables with result summary. Output is written to console.
The script requires one positional argument which is the xls file generated from
KTU-Login(app.ktu.edu.in) > Results > Semester Grade Card Report > ... > Export as XLS

Setup (Ubuntu):
You need to install python3, and python3-pip from package manager

sudo apt install python3 python3-pip


You have to install pandas and xlrd

sudo pip3 install pandas xlrd

Usage:

./result\_analysis.py Results.xls
