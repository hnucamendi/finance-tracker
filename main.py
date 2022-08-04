import pandas as pd
import gspread
import csv
import time

file = "test-data.csv"

# data = pd.read_csv("test-data.csv")

# def roundData(data):
#   list = []
#   for i in range(len(data)):
#     list.append(round(data[i]))
#   return list

# def removePayments(data):
#   list = []
#   data = roundData(data)
#   for i in range(len(data)):
#     if data[i] < 0:
#       continue
#     list.append(data[i])
#   return list

# def addTotal(data):
#   data = removePayments(data.Amount)
#   sum = 0
#   for i in range(len(data)):
#     sum += data[i]
#   return sum

# header = ["Amount", "Amount2"]
# writedata = [[addTotal(data), addTotal(data)]]
# writedata = pd.DataFrame(writedata,columns=header)
# writedata.to_csv('new-data',index=False)

sa = gspread.service_account()
sh = sa.open("personalfinances")

def testFunc(file):
  transactions = []
  with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      date = row[0]
      name = row[2]
      amount = float(row[3])
      category = row[4]
      transaction = ((date,name, amount, category))
      # print(transaction)
      transactions.append(transaction)
    return transactions

wks = sh.worksheet("Sheet1")

rows = testFunc("test-data.csv")
# print(rows)
for row in rows:
  wks.insert_row([row[0], row[1],row[2],row[3]],1)
  # print([row[0], row[1],row[2],row[3]],1)
  time.sleep(2)

# header = ["name", "amount"]
# writedata = [[data[0], data[1]]]
# writedata = pd.DataFrame(writedata,columns=header)
# writedata.to_csv('new-data',index=False)

#Trans. Date,Post Date,Description,Amount,Category