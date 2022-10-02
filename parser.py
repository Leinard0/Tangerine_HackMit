import json
import pandas as pd
from IPython.display import display
from IPython.display import HTML

#reading in data
dawndata_df = pd.read_json("dawndata1.json")
#convert both position and events as strings
dawndata_df["position"] = [','.join(map(str, l)) for l in dawndata_df["position"]]
dawndata_df["events"] = [json.dumps(d) for d in dawndata_df["events"]]
#made a series that says returns whether the position is repeated or not
duplicate = dawndata_df.duplicated(subset = ["userId", "position"], keep = False) #this is the series, add it to column
#make duplicate series into a column in dawndata_df
dawndata_df = dawndata_df.assign(duplicates = duplicate);
#clear out all rows where duplicate column is FALSE 
dawndata_df = dawndata_df.drop(dawndata_df[dawndata_df.duplicates == False].index)
#need to specify that the event is ping:1 (technically edgecase)
#ping_series = [dawndata_df["events"].str.contains('\"ping\": 1')]
dawndata_df = dawndata_df[dawndata_df["events"].str.contains('\"ping\": 1')]

#then find sum of all pings per user
count = dawndata_df.groupby(["userId"]).count()
count.rename(columns = {'time':'pingCount'}, inplace = True)
count = count[['pingCount']]
print("Final Ping Count for afk players:")
print(count)
count.to_html('visualize.html', classes='table table-stripped', justify='center')

#print(ping_series)
#if this value for any userId is greater than 5, return those users?

#prints out all the cleaned data based on userId
print("Above table baseed on data visualized below:")
userIDdata = dawndata_df.groupby(["userId"])
for key, item in userIDdata:
    print(userIDdata.get_group(key), "\n\n")