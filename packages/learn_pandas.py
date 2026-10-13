import pandas as pd
"""a="bhavi"
print(a[0:5])
b=pd.Series(a)
print(b)
data={
    "users" : ["bheem","raju","jagu","chutki"],
    "roll.no" : [12,15,36,4.2]
}"""
#print(data.keys())


df=pd.read_csv("./ecommerce.csv")
print(df.iloc[0:5])