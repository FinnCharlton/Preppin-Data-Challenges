#Challenge
#https://preppindata.blogspot.com/2023/02/2023-week-6-dsb-customer-ratings.html

#Import Packages
import pandas as pd

#Import data to DataFrame
df = pd.read_csv("C:\\Users\\FinnCharlton\\Github Repos\\Preppin-Data-Challenges\\Preppin Data Python\\2023 Week 6\\DSB Customer Survery.csv")

#Get Column Name List and Unpivot
colNames = df.columns.values.tolist()[1:]
df = pd.melt(df,id_vars="Customer ID",value_vars=colNames)

#Split Name Field
df[["Type","Question"]] = df["variable"].str.split(pat=" - ",expand=True)

#Repivot
df = df.pivot(columns="Type",index=["Customer ID","Question"],values="value")

df = df.reset_index(names=["Customer ID","Question"])

#Exclude Overall Values
df = df.loc[(df.Question != "Overall Rating")]

#Average Rating per platform per customer
avgRating = df.groupby("Customer ID").agg({"Mobile App":"mean","Online Interface":"mean"})

#Differences
avgRating["delta"] = avgRating["Mobile App"] - avgRating["Online Interface"]

#Categorisation Function
def categorise(value):
    if value <=-2:
        return "Mobile Superfan"
    elif value <=-1:
        return "Mobile Fan"
    elif value <1:
        return "Neutral"
    elif value <2:
        return "Online Fan"
    else:
        return "Online Superfan"

#Apply Categorisation
avgRating["Category"] = avgRating["delta"].apply(categorise)


#Percent of Total
counts = avgRating.groupby("Category").agg({"Category":"count"})
counts["Total"] = int(avgRating.agg({"Category":"count"}))
counts["Percent Of Total"] =round((counts["Category"] / counts["Total"])*100,1)

#Filter for Output
output= counts.filter(items=["Type","Percent Of Total"])
output = output.reset_index()


output.to_csv("C:/Users/FinnCharlton/Github Repos/Preppin-Data-Challenges/Preppin Data Python/2023 Week 6/PD 2023 Wk6 Output")
