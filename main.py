import gspread
import csv
import time
import re
import glob
import os

acc = gspread.service_account()
sheet = acc.open("personal-finances")
pendingFiles = glob.glob("./test-data/*.csv")


def addTotal(data):
    data = round(data)
    sum = 0
    if data < 0:
        return 0
    sum += data
    return sum


def stringToFloat(numString):
    if re.search("-\d*", numString):
        numString = re.sub(r'.', '', numString, count=1)
    if re.search(".*,\d*", numString):
        numString = re.sub(r",", "", numString)
    if not re.search("[.]\d{1,2}", numString):
        numString += ".00"
    return numString


def loadFile(file, cfg):
    transactions = []
    wksName = ""
    with open(file, mode='r') as csv_file:
        if cfg["cfg"] == "bofa":
            for _ in range(7):
                next(csv_file)
        next(csv_file)
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            wksName = sheet.worksheet(re.search("\d{4}", row[0]).group(0))
            date = row[cfg["date"]]
            name = row[cfg["name"]]
            if cfg["cfg"] == "bofa":
                row[cfg["amount"]] = stringToFloat(row[cfg["amount"]])
            amount = float(row[cfg["amount"]])
            category = row[cfg["category"]]
            rounded = addTotal(float(row[cfg["amount"]]))
            bank = cfg["cfg"]
            transaction = (
                (date, name, amount, category, rounded, bank, wksName))
            transactions.append(transaction)
        return transactions


for file in pendingFiles:
    bofa = re.search(".*stmt(.+).csv", file)
    apple = re.search(".*Apple(.+).csv", file)
    discover = re.search(".*Discover(.+).csv", file)

    if discover:
        rows = loadFile(
            file, {"category": 4, "amount": 3, "name": 2, "date": 0, "cfg": "discover"})
        for row in rows:
            # print([row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            row[6].insert_row(
                [row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            time.sleep(2)
        time.sleep(1)
        # os.remove(file)
    elif apple:
        rows = loadFile(
            file, {"category": 4, "amount": 6, "name": 2, "date": 0, "cfg": "apple"})
        for row in rows:
            # print([row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            row[6].insert_row(
                [row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            time.sleep(2)
        time.sleep(1)
        # os.remove(file)
    elif bofa:
        rows = loadFile(
            file, {"category": 0, "amount": 2, "name": 1, "date": 0, "cfg": "bofa"})
        for row in rows:
            # print([row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            row[6].insert_row(
                [row[0], row[1], row[2], row[4], row[3], row[5]], 2)
            time.sleep(2)
        time.sleep(1)
        # os.remove(file)
    else:
        os.remove(file)
