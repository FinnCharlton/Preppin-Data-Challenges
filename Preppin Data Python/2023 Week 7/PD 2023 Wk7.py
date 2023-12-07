#Challenge:
#https://preppindata.blogspot.com/2023/02/2023-week-7-flagging-fraudulent.html

#Import Packages
import pandas as pd

#Import Data
accHolders = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 7/Account Holders.csv")
accInfo = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 7/Account Information.csv")
transDetail = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 7/Transaction Detail.csv")
transPath = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 7/Transaction Path.csv")

#Rename Fields in Transaction Path table
transPath = transPath.rename(columns={"Account_To":"Account To","Account_From":"Account From"})

#Filter Out Nulls in Account Holder ID Field
accInfo= accInfo.dropna(subset="Account Holder ID")

#Split Joint Accounts to Rows
accInfo["Account Holder ID"] = accInfo["Account Holder ID"].str.split(',')
accInfo = accInfo.explode("Account Holder ID").reset_index()

#Ensure Phone Numbers start with 07
accHolders["Contact Number"] = accHolders["Contact Number"].astype(str).str.pad(11,"left","0")

#Join Account Info Tables
accHolders["Account Holder ID"] = accHolders["Account Holder ID"].astype(str)
accJoined = pd.merge(accHolders,accInfo,how="inner",on="Account Holder ID")

#Join Transcation Tables
transJoined = pd.merge(transDetail,transPath,how="inner",on="Transaction ID")

#Join remaining
allJoined = pd.merge(transJoined,accJoined,how = "inner", left_on = transJoined["Account To"], right_on= accJoined["Account Number"])

#Filter to large transactions from non-Platinum accounts
output = allJoined.loc[(allJoined["Cancelled?"]!="Y") & (allJoined["Value"]>1000) & (allJoined["Account Type"]!="Platinum")]

output.to_csv("Preppin Data Python/2023 Week 7/PD 2023 Wk7 Output")