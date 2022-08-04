import gspread
import csv
import time

file = "test-data.csv"

sa = gspread.service_account()
sh = sa.open("personalfinances")

def addTotal(data):
  data = round(data)
  sum = 0
  if data < 0:
    return 0
  sum += data
  return sum

def testFunc(file):
  transactions = []
  with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
      date = row[0]
      name = row[2]
      amount = float(row[3])
      category = row[4]
      rounded = addTotal(float(row[3]))
      transaction = ((date,name, amount, category, rounded))
      transactions.append(transaction)
    return transactions

wks = sh.worksheet("Sheet1")

rows = testFunc("test-data.csv")
for row in rows:
  wks.insert_row([row[0], row[1], row[2], row[4], row[3]],2)
  time.sleep(2)