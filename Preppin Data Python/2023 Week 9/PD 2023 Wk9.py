#Challenge:
#https://preppindata.blogspot.com/2023/03/2023-week-9-customer-bank-statements.html

#Import Packages
import pandas as pd

#Import Data
accInfo = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 9/Account Information.csv")
transDetail = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 9/Transaction Detail.csv")
transPath = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 9/Transaction Path.csv")

#Remove cancelled transactions
transDetail = transDetail.loc[transDetail["Cancelled?"] == 'N']

#Join Transaction tables
transJoined = pd.merge(transDetail,transPath, how="inner", on="Transaction ID")

#Separate outgoing transactions, and join account information
transOutgoing = transJoined.drop("Account_To",axis=1).rename(columns={"Account_From":"Account Number"})
outgoingJoined = pd.merge(transOutgoing,accInfo.drop(["Balance Date"],axis=1),how="inner",on="Account Number")

# #Reverse sign of outgoing transactions
outgoingJoined["Value"] = -outgoingJoined["Value"]

#Separate incoming transactions, and join account information
transIncoming = transJoined.drop("Account_From",axis=1).rename(columns={"Account_To":"Account Number"})
incomingJoined = pd.merge(transIncoming,accInfo.drop(["Balance Date"],axis=1),how="inner",on="Account Number")

#Union Data streams
fullTransList = pd.concat([outgoingJoined,incomingJoined])

#Union Balance as of Jan 31st
balances = accInfo.rename(columns={"Balance Date":"Transaction Date"})
balances["Value"] = 0
fullTransList = pd.concat([fullTransList,balances])

#Sort and calculate running sum
fullTransList = fullTransList.sort_values(["Account Number","Transaction Date","Value"])
fullTransList["Running Sum"] = fullTransList.groupby("Account Number")["Value"].cumsum()
fullTransList["Current Balance"] = fullTransList["Running Sum"] + fullTransList["Balance"]

#Form Output
output = fullTransList[["Account Number","Transaction Date","Value","Current Balance"]]

output.to_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 9/PD 2023 Wk9 Output.csv")