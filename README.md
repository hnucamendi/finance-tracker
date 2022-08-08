# Finance Tracker

Keep track of your finances across multiple banks in an easy way without having to worry about filling in an exel sheet by hand

## Supported Banks

- Bank of America Credit Cards
- Discover Credit Cards
- Apple Credit Card

## Setup

To set up this program you will to set up a couple of things:

- Google API access
- Download a zip of this code
- CSV files from all your banks

### Step 1: Google API Access

- go to [Google Cloud Console](https://console.cloud.google.com/getting-started)
- `APIs & Services` > you may need to create a project here
- `Create Credentials` > Service Account > Create > take note of the email generated for this service account
  - You should be prompted to download a file, keep track of this file (needed later)
- open up a `Google Sheets` Document
- Click on `Share` and add the email that you got for the service account
- Next step depends on the OS you are on
  - Windows
  - Press `windows key + R` > Type `%appdata%` > Enter
  - make a folder named `gspread` and put the txt file that was downloaded when creating the service account
  - rename the file to `service_account.json`
- Mac or Linux
  - open terminal and `cd ~/.config/` > `mkdir gspread && cd gspread` > `open .`
  - now with this file location open put the file into this folder and rename it to `service_account.json`

### Step 2: Downloading Code

- On the top of the GitHub page there is a `code` button > should be able to download the code from there
- once this is done open up the file in your code editor > make a folder named `finance` and put all the CSV data in here
- run by doing `python main.py` on windows or `python3 main.py` on linux or mac (in terminal)

## Next Steps

Watch all of the data get parsed into the CSV file that you allowed access to that service account.
In the future I would like to make this open to more banks and make the setup process a bit easier as well. For now its somewhat complex but its worth it!

## Version 1.1.0

- Written in Python
