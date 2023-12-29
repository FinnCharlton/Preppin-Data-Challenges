#Import Packages
import pandas as pd

#Import Input Data
df = pd.read_csv("C:\\Users\\FinnCharlton\\Github Repos\\Preppin-Data-Challenges\\Preppin Data Python\\2023 Week 9\\PD 2023 Wk9 Output.csv")

#Change Transaction Date Field  to datetime
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])

#Aggregate for one value per day
dfAgg = df.groupby(["Account Number","Transaction Date"]).agg({"Value":"sum","Current Balance":"last"}).reset_index()

#Create date scaffold
dateRange = pd.date_range(start='2023-01-31',end='2023-02-14')
dateRange_df = pd.DataFrame({"Transaction Date":dateRange})

#Create unique list of account numbers
accNumbers = pd.DataFrame(df["Account Number"].unique()).rename(columns={0:"Account Number"})

#Join Account Numbers to Date scaffold
scaffold = pd.merge(accNumbers,dateRange_df,how="cross")

#Join to date scaffold
dfJoined = pd.merge(left=scaffold,right=dfAgg,how="left",on=["Account Number","Transaction Date"])

#Fill down null balance values
dfJoined["Current Balance"].fillna(method='pad',inplace=True)

#Create input variable to choose date
dateChoice = input("Please choose the date you wish to view. Use YYYY-MM-DD format: ")
while True:
    while True:
        try:
            dateChoiceParsed = pd.to_datetime(dateChoice)
            break
        except:
            print()
            dateChoice = input("Please enter a date in YYYY-MM-DD format: ")
    if dateChoiceParsed >= pd.to_datetime("2023-01-31") and dateChoiceParsed <= pd.to_datetime("2023-02-14"):
        break
    else:
        dateChoice = input("Choose a date between 2023-01-31 and 2023-02-14: ")

#Filter output based on input variable
dfFiltered = dfJoined.loc[(dfJoined["Transaction Date"] == dateChoiceParsed)]

#Create output file name and output filtered table
outputFileName = f"C:\\Users\\FinnCharlton\\Github Repos\\Preppin-Data-Challenges\\Preppin Data Python\\2023 Week 10\\PD 2023 Wk 10 {dateChoiceParsed.date()}.csv"
dfFiltered.to_csv(outputFileName)
