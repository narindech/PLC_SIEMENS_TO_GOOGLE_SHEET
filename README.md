# PLC SIEMENS TO GOOGLE SHEET
## Introduction

This repo demonstrates how to read data from SIEMENS PLC and store in google sheet via Google Sheet API.
Please be noticed, it requires Google API enabled and PLC program uploaded into either PLCSIM or real hardware device. Also, your PLC should be configured properly in order to be seen by python program in the same network as well.

## Prerequisites
> 1. PLCSIM Advanced v4
> 2. TIA portal v17
> 3. snap7 (Python library)
> 4. Google Sheet API enabled with OAuth2.0 authentication

### Note.
Please make sure you place your python script in the host which lives in same network as your PLC.

## How to setup your virtual environment.

1. Check if you have `virtualenv` installed in your environment. If not, try to install it first by running this command `pip install virtualenv`.
2. If you have it installed and you never have an virtual environment running before, please create a new one by running this command `virtualenv venv`. **Keep in mind that, you should go to your desire directory first before run this command**. You can replace `venv` with any name you want.

## Start virtualenv
1. Go to the directory where your virtual environment lives.
2. Then, run this command `.\venv\Scripts\activate` to start your environment. You can replace `venv` with your environment's name.
3. If it runs correctly, you should see `(venv)` in front of your command line.

## How to install dependencies
> 1. Make sure virtual environment is running.
> 2. Run this command `pip install -r requirements.txt`

## How to run script
> 1. go to your project directory.
> 2. Run this command `python main_google_sheet.py`