import gspread
import csv
import time
import re
import glob
import os

# TODO:
# Make file selection possible based on Bank
# Make iteration for each file
# should be able to fill multiple files into sheets and seperate by year

# 07/21/2022

# file = "test-data.csv"

# import glob
# files = glob.glob("*.txt")           # get all the .txt files

# for file in files:                   # iterate over the list of files
#     with open(file, "r") as fin:     # open the file
#         # rest of the code


# import os
# arr = os.listdir()
# files = [x for x in arr if x.endswith('.txt')]

# for file in files:                   # iterate over the list of files
#     with open(file, "r") as fin:     # open the file
#        # rest of the code

# './test-data\\Apple Card Transactions - May 2022.csv'
# './test-data\\stmt(19).csv'
# './test-data\\Discover-Statement-20222307.csv'

acc = gspread.service_account()
sheet = acc.open("personal-finances")
pendingFiles = glob.glob("./test-data/*.csv")


# def loadFile(file, cfg):
#     if sheet.worksheet("sldfj"):
#         print(0)
#     if cfg == "discover":
#         sheet.worksheet("Sheet1")
#     if cfg == "apple":
#         print(0)
#     if cfg == "bofa":
#         print(0)

def addTotal(data):
    data = round(data)
    sum = 0
    if data < 0:
        return 0
    sum += data
    return sum


def loadFile(file, cfg):
    transactions = []
    ignore = ["Date", "Description", "Amount",
              "Running Bal.""Trans. Date", "Post Date", "Category"]
    sheet = ""
    with open(file, mode='r') as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file)
        # if cfg == bofa:
        #     csv_reader
        for row in csv_reader:
            sheet = re.search("\d{4}", row[0]).group(0)
            date = row[0]
            name = row[2]
            amount = float(row[3])
            category = row[4]
            rounded = addTotal(float(row[3]))
            transaction = ((date, name, amount, category, rounded))
            transactions.append(transaction)
        return transactions, sheet


for file in pendingFiles:
    bofa = re.search(".*stmt(.+).csv", file)
    apple = re.search(".*Apple(.+).csv", file)
    discover = re.search(".*Discover(.+).csv", file)

    if discover:
        rows, sheet = loadFile(file, "discover")
        for row in rows:
            # print([row[0], row[1], row[2], row[4], row[3]], 2)
            print(sheet)
            # sheet.insert_row([row[0], row[1], row[2], row[4], row[3]], 2)
            time.sleep(2)
        time.sleep(1)
        # os.remove(file)
    elif apple:
        time.sleep(1)
        # loadFile(file, "apple")
        # os.remove(file)
    elif bofa:
        time.sleep(1)
        # loadFile(file, "bofa")
        # os.remove(file)
    else:
        time.sleep(2)
        # os.remove(file)
