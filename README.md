# AMP_Duplicate_Endpoint_Removal


## Introduction
 
You've successfully deployed AMP for Endpoints and it is now running on your system.  Great!  You may find that a duplicate endpoint is appearing in your AMP database.  This tool can be used as a workaround to remove that duplicate.


## Disclaimer

This is not an officially supported tool and was developed as a side project, not as an official release by Cisco.  Any support received will be on an as-available timeframe and feature requests may not be fulfilled.

## Installation
 
No installation is required.  The tool can be downloaded or cloned from GitHub.  If you'd like to make an EXE, you can do so with [PyInstaller](https://www.pyinstaller.org/):
> pyinstaller --onefile --console --icon amp-icon.ico .\amp_dup_removal.py

Current executable has been included in the files above for ease of use.

## Usage
 
To start the tool, ensure that you have an instance of AMP running and run the amp_dup_removal.py script.  Otherwise, if you have an executable (.exe) that you generated from PyInstaller, just right-click the executable and select Open.  You'll be presented with the console interface.

At that point, you will be prompted to enter:

amp_api_key - this is the API key that can be obtained from the AMP console.\
amp_client_id - your client ID to access the AMP console.\
amp_group - the AMP group you want to search and remove duplicate endpoints.

The tool identifies duplicates based upon the endpoint hostname.  It will tell you up front how many devices were found in the group and out of those devices, which ones are actually duplicates.  Once it finds a duplicate, it will then check the "last seen" date for each of them.  The duplicate endpoint with the older date will be removed.  You will be prompted each time to confirm the removal operation.  Whether you select "y" or "n", the tool will proceed to check for another duplicate endpoint.

## Screenshot of tool

![](/images/amp_dup_endpoint_console.png)
