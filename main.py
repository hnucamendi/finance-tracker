import gspread
import csv
import time
import re
import glob
import os

# TODO:
# - Automate getting monthly data

acc = gspread.service_account()

sheet = acc.open("personal-finances")
pendingFiles = glob.glob("./finance/*.csv")

# Testing
# sheet = acc.open("personal-finances-test")
# pendingFiles = glob.glob("./test-data/*.csv")

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def turnToList(strings):
    arr = []
    if strings == "" or strings == "all":
        arr = list(["apple", "discover", "bofa"])
    elif re.search(".*,\d*", strings):
        strings = strings.replace(" ", "")
        arr = list(strings.split(","))
    elif re.search("[ ]", strings):
        arr = list(strings.split(" "))
    elif re.search("-", strings):
        arr = list(strings.split("-"))
    elif len(strings) > 0:
        arr = list()
        arr.append(strings)
    else:
        print(strings + " was not converted to list")
    defineProcess(arr)


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
    month = re.search("[\d].!*",dateString).group(0)
    match month:
        case "01":
            month = months[0]
        case "02":
            month = months[1]
        case "03":
            month = months[2]
        case "04":
            month = months[3]
        case "05":
            month = months[4]
        case "06":
            month = months[5]
        case "07":
            month = months[6]
        case "08":
            month = months[7]
        case "09":
            month = months[8]
        case "10":
            month = months[9]
        case "11":
            month = months[10]
        case "12":
            month = months[11]
    return month

def removePayments(floatNum, bank):
    if bank == "bofa" and floatNum < 0:
        floatNum *= -1
        return floatNum
    elif bank == "bofa" and floatNum > 0:
        return 0

    if bank == "income" and floatNum < 0:
        return 0
    elif bank == "income" and floatNum > 0:
        return floatNum

    if floatNum < 0:
        return 0
    return floatNum


def loadFile(file, cfg):
    transactions = []
    wksName = ""
    with open(file, mode='r') as csv_file:
        next(csv_file)
        print(cfg["cfg"])
        if cfg["cfg"] == "income":
            for _ in range(6):
                next(csv_file)
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if cfg["cfg"] == "income":
                wksName = sheet.worksheet("income")
            else:
                wksName = sheet.worksheet(re.search("\d{4}", row[0]).group(0))
            date = row[cfg["date"]]
            txtDate = textDate(row[cfg["date"]])
            name = row[cfg["name"]]
            if cfg["cfg"] == "bofa" or cfg["cfg"] == "income":
                row[cfg["amount"]] = stringToFloat(row[cfg["amount"]])
            amount = removePayments(float(row[cfg["amount"]]), cfg["cfg"])
            category = row[cfg["category"]]
            rounded = addTotal(float(row[cfg["amount"]]))
            bank = cfg["cfg"]
            transaction = ((txtDate, date, name, amount, category, rounded, bank, wksName))
            transactions.append(transaction)
        return transactions


def loadCSV(rows, cfg={"txtDate": 0, "date": 1, "name": 2, "amount": 3, "category": 5, "rAmount": 4, "cfg": 6}):
    for row in rows:
        # print([row[cfg["txtDate"]], row[cfg["date"]], row[cfg["name"]], row[cfg["amount"]],row[cfg["category"]], row[cfg["rAmount"]], row[cfg["cfg"]]], 2)
        row[7].insert_row([row[cfg["txtDate"]], row[cfg["date"]], row[cfg["name"]], row[cfg["amount"]],row[cfg["category"]], row[cfg["rAmount"]], row[cfg["cfg"]]], 2)
        time.sleep(2)

def defineProcess(banks):
    for file in pendingFiles:
        for bank in banks:
            if bank == "bofa":
                bofa = re.search("(.+)_4764.csv", file)
                if bofa:
                    rows = loadFile(file, {"category": 1, "amount": 4, "name": 2, "date": 0, "cfg": "bofa"})
                    loadCSV(rows)
                    os.remove(file)
            if bank == "apple":
                apple = re.search(".*Apple(.+).csv", file)
                if apple:
                    rows = loadFile(file, {"category": 4, "amount": 6, "name": 2, "date": 0, "cfg": "apple"})
                    loadCSV(rows)
                    os.remove(file)
            if bank == "discover":
                discover = re.search(".*Discover(.+).csv", file)
                if discover:
                    rows = loadFile(file, {"category": 4, "amount": 3, "name": 2, "date": 0, "cfg": "discover"})
                    loadCSV(rows, {"txtDate": 0, "date": 1, "name": 2, "amount": 3, "rAmount": 4, "category": 5, "cfg": 6})
                    os.remove(file)
            if bank == "income":
                income = re.search(".*stmt(.+).csv", file)
                if income:
                    rows = loadFile(file, {"category": 3, "amount": 2, "name": 1, "date": 0, "cfg": "income"})
                    loadCSV(rows)
                    os.remove(file)

print("Available Input: bofa, discover, apple, income, all")
turnToList(input("Enter Config: "))
