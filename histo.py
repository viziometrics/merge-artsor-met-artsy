import pandas as pd
import matplotlib.pyplot as plt



merge = pd.read_csv("merge.tsv", sep='\t', low_memory=False)
merge = merge[pd.notnull(merge['time_earliest'])]


def saveFig(from_year, to_year):
    tmp = merge.loc[(merge['time_earliest'] < to_year) & (merge['time_earliest'] > from_year)]
    plt.hist(tmp['time_earliest'], bins=100, color = "blue",alpha=0.5)
    plt.savefig("earliest "+str(from_year)+" to " +str(to_year)+".png")
    plt.clf()

years =[ (-2000,2020), (0,2020), (1250, 2020),(1400, 2020), (1700, 2020)]
for x,y in years:
    saveFig(x,y)