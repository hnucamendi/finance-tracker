from traceback import print_list
import gspread
import csv
import time
import re
import glob
import os

# TODO:
# - Parse Data and organize by month

acc = gspread.service_account()
# sheet = acc.open("personal-finances")
# pendingFiles = glob.glob("./finance/*.csv")

# Testing
sheet = acc.open("personal-finances-test")
pendingFiles = glob.glob("./test-data/*.csv")

months = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def addTotal(data):
    data = round(data)
    sum = 0
    if data < 0:
        return 0
    sum += data
    return sum


def stringToFloat(numString):
    if re.search(".*,\d*", numString):
        numString = re.sub(r",", "", numString)
    if not re.search("[.]\d{1,2}", numString):
        numString += ".00"
    return numString


def textDate(dateString):
    #     # "01/21/2122"
    #     for i in range(len(months)):
    #         match dateString:
    #             case i:
    #                 return months[i]
    time.sleep(.01)
    # print(dateString)

def parseDataMonthly(list, monthString, monthInt):
    # print(list)
    # print(monthString)
    month = []
    # for row in list:
    #     print("row")
    #     print(row)
    #     print("montString")
    #     print(monthString)
    #     if row[0] == monthString:
    #         month.append(row)
    # print(month)
    for i in range(len(list)):
        # print(list[i][0])
        match list[i][0]:
            case "January":
                month = list
                print(month)
            case "February":
                month = list
                print(month)
            case "March":
                month = list
                print(month)
            case "April":
                month = list
                print(month)
            case "May":
                month = list
                print(month)
            case "June":
                month = list
                print(month)
            case "July":
                month = list
                print(month)
            case "August":
                month = list
                print(month)
            case "September":
                month = list
                print(month)
            case "October":
                month = list
                print(month)
            case "November":
                month = list
                print(month)
            case "December":
                month = list
                print(month)


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
            # txtDate = textDate(row[cfg["date"]])
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
        parsedTransactions = parseDataMonthly(transactions,txtDate, date)
        return transactions, parsedTransactions


def loadCSV(rows, cfg={"date": 0, "name": 1, "amount": 2, "category": 4, "rAmount": 3, "cfg": 5}):
    for row in rows:
        # print([row[cfg["date"]], row[cfg["name"]], row[cfg["amount"]],row[cfg["category"]], row[cfg["rAmount"]], row[cfg["cfg"]]], 2)

        row[6].insert_row([row[cfg["date"]], row[cfg["name"]], row[cfg["amount"]],row[cfg["category"]], row[cfg["rAmount"]], row[cfg["cfg"]]], 2)
        time.sleep(2)


for file in pendingFiles:
    bofa = re.search(".*stmt(.+).csv", file)
    apple = re.search(".*Apple(.+).csv", file)
    discover = re.search(".*Discover(.+).csv", file)

    if discover:
<<<<<<< Updated upstream
        rows = loadFile(
            file, {"category": 4, "amount": 3, "name": 2, "date": 0, "cfg": "discover"})
        loadCSV(rows, {"date": 0, "name": 1, "amount": 2,
                "category": 3, "rAmount": 4, "cfg": 5})
        os.remove(file)
    elif apple:
        rows = loadFile(
            file, {"category": 4, "amount": 6, "name": 2, "date": 0, "cfg": "apple"})
=======
        rows, monthly = loadFile(file, {"category": 4, "amount": 3, "name": 2, "date": 0, "cfg": "discover"})
        loadCSV(rows, {"txtDate": 0,"date": 1, "name": 2, "amount": 3, "category": 4, "rAmount": 5, "cfg": 6})
        # os.remove(file)
    elif apple:
        rows, monthly = loadFile(file, {"category": 4, "amount": 6, "name": 2, "date": 0, "cfg": "apple"})
>>>>>>> Stashed changes
        loadCSV(rows)
        os.remove(file)
    elif bofa:
        rows, monthly = loadFile(
            file, {"category": 0, "amount": 2, "name": 1, "date": 0, "cfg": "bofa"})
        loadCSV(rows)
        os.remove(file)
    else:
        # time.sleep(1)
        os.remove(file)
