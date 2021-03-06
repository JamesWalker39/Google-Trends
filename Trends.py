#pip install pytrends
import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from matplotlib import style

#connect to google
pytrends = TrendReq(hl='en-US', tz=360)

#key term
kw = input("Please enter a google search: " )

#payload
kw_list = [kw]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='US')

#Search for trend and return df
IBR_df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=False, inc_geo_code=False)
IBR_df2 = IBR_df[ IBR_df[kw] != 0 ]
IBR_df2.reset_index(inplace=True)
IBR_df2.sort_values(by=kw, ascending=False, inplace=True)
# IBR_df2["geoName"] = IBR_df2["geoName"].str.slice(0,-3)
IBR_df2.head()

fig = plt.figure()
ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 2, colspan=1)

x = IBR_df2['geoName'].head(10)
y = IBR_df2[kw].head(10)
ax1.bar(x,y,color ='#8B0000')
ax1.set_xticklabels(x, rotation=90)
ax1.tick_params(labelsize='8')

plt.title('Top 10 States Searching for '+ kw)
plt.ylabel('Rel. Prop Searches')
plt.grid(True, color='k', linestyle ='-', linewidth = 0.2)
plt.legend()


# Interest over time


IOT_df = pytrends.interest_over_time()
IOT_df.drop(columns='isPartial', inplace=True)
IOT_df.head()
x = IOT_df.index
y = IOT_df[kw]

ax2 = plt.subplot2grid((8,1), (3,0), rowspan = 2, colspan=1)
ax2.plot(x,y, color='b')

plt.style.use('ggplot')
plt.ylabel('Rel. Prop Searches')
plt.title(kw +' Searches Over Time')
plt.grid(True, color='k', linestyle ='-', linewidth = 0.2)

#blank df for text
ax3 = plt.subplot2grid((8,1), (6,0), rowspan = 2, colspan=1)
ax3.axis('off')


##keywords similar & return df
keywords = pytrends.suggestions(kw)
Sug_df = pd.DataFrame(keywords)
Sug_df.drop(columns='mid', axis=1, inplace=True)
Sug_df.set_index('title', inplace=True)

suggestedList = Sug_df.index.tolist()
ax3.annotate(suggestedList[0]+"\n"+suggestedList[1]+"\n"+suggestedList[2]+"\n"+suggestedList[3]+"\n"+suggestedList[4], (0,0),
                 xytext=(0, 0), textcoords='axes fraction', color='#6a6a6a')

plt.title(kw +' Suggested Searches')

plt.show()
                 




