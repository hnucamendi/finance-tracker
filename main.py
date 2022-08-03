import pandas as pd

data = pd.read_csv("test-data.csv")

def roundData(data):
  list = []
  for i in range(len(data)):
    list.append(round(data[i]))
  return list

def removePayments(data):
  list = []
  data = roundData(data)
  for i in range(len(data)):
    if data[i] < 0:
      continue
    list.append(data[i])
  return list

def addTotal(data):
  data = removePayments(data.Amount)
  sum = 0
  for i in range(len(data)):
    sum += data[i]
  return sum

header = ["Amount", "Amount2"]
writedata = [[addTotal(data), addTotal(data)]]
writedata = pd.DataFrame(writedata,columns=header)
writedata.to_csv('new-data',index=False)

# header = ["name", "amount"]
# writedata = [[data[0], data[1]]]
# writedata = pd.DataFrame(writedata,columns=header)
# writedata.to_csv('new-data',index=False)
