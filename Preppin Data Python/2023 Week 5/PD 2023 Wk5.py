#Challenge:
#https://preppindata.blogspot.com/2023/02/2023-week-5-dsb-ranking.html

# Import Packages
import pandas as pd
import numpy as np

# Import Data from CSV.
df = pd.read_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 5/PD 2023 Wk 5 Input.csv")

# Create Bank Code field by splitting Transaction Code field.
df["Bank Code"] = df["Transaction Code"].str.partition(sep='-')[0]

# Create Month of Transaction field.
df["Transaction Month"] = pd.to_datetime(df["Transaction Date"]).dt.month_name()

#Aggregate Value by Bank and Month.
bankMonthVal = df.groupby(["Transaction Month","Bank Code"]).agg({"Value":"sum"})

#Rank Banks by Value each Month. Join back to full dataset.
bankMonthRanks = bankMonthVal.groupby("Transaction Month").rank(ascending=False)
bankMonthRanks= bankMonthRanks.rename(columns={'Value':'Bank Rank per Month'})
df = pd.merge(df,bankMonthRanks,how='inner',on=["Bank Code","Transaction Month"])

#Calculate Average Rank per Bank. Join back to original dataset.
avgBankRank = bankMonthRanks.groupby("Bank Code").agg({"Bank Rank per Month":"mean"})
avgBankRank= avgBankRank.rename(columns={'Bank Rank per Month':'Avg Bank Rank'})
df = pd.merge(df,avgBankRank,how='inner',on="Bank Code")


# Calculate Average Transaction Value per Rank. Join back to original dataset.
avgValuePerRank = df.groupby("Bank Rank per Month").agg({"Value":"mean"})
avgValuePerRank= avgValuePerRank.rename(columns={'Value':'Avg Value per Rank'})
df = pd.merge(df,avgValuePerRank,how='inner',on="Bank Rank per Month")

#Select relevant fields
df = df[["Transaction Month","Bank Code","Value","Bank Rank per Month","Avg Value per Rank","Avg Bank Rank"]]

#Output result
df.to_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 5/PD 2023 Wk5 Output.csv")







