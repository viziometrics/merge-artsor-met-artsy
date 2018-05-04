import pandas as pd
import re

bc = ['BCE', 'B.C.', 'B. C.', 'BC']
def get_latest(date):
    if isinstance(date, basestring):
        regex = re.compile(r"\d{3,4}")
        match = regex.findall(date)
        isBC = ""
        if any(x in date for x in bc):
            isBC = "-"
        if len(match) == 1:
            return isBC + str(match[0])
        elif len(match) == 2:
            first = int(match[0])
            second = int(match[1])
            if first < second:
                return isBC + str(first)
            else:
                return isBC + str(second)
    return ""

def get_earliest(date):
    if isinstance(date, basestring):
        regex = re.compile(r"\d{3,4}")
        match = regex.findall(date)
        isBC = ""
        if any(x in date for x in bc):
            isBC = "-"
        if len(match) == 1:
            return isBC + str(match[0])
        elif len(match) == 2:
            first = int(match[0])
            second = int(match[1])
            if first > second:
                return isBC + str(first)
            else:
                return isBC + str(second)
    return ""



# read files into panda
artstor = pd.read_csv("artstor.tsv", sep='\t', low_memory=False)
met = pd.read_csv("met.csv", low_memory=False)
artsy = pd.read_csv("artsy.csv", low_memory=False)

# select columns that we want
artstor = artstor[['filename', 'Title', 'Creator', 'Date.Latest', 'Date.Earliest',
                   'Material', 'Source', 'Description', 'ARTstorBrowseClass', 'Type']]
met = met[['Object Number', 'Object Number', 'Title', 'Artist Display Name',
           'Object Date', 'Object Begin Date', 'Object End Date', 'Medium', 'Classification', 'Object Name']]
artsy = artsy[['id', 'id', 'title', 'date',
               'category', 'medium']]

# Fill column of which source
artstor['data_source'] = 'artstor'
met['data_source'] = 'met'
artsy['data_source'] = 'artsy'

# rename colums
artstor.columns = ['filename', 'title', 'creator', 'time_latest', 'time_earliest',
                   'material', 'artstor-source', 'artstor description', 'artstor_browse_class', 'artstor_type', 'data_source']
met.columns = ['filename', 'img_id', 'title', 'creator', 'time', 'time_latest',
               'time_earliest', 'medium', 'met_classification', 'met_object_name', 'data_source']
artsy.columns = ['filename', 'img_id', 'title',
                 'time', 'artsy_category', 'medium', 'data_source']

# Special case just for Arsty
artsy['time_latest'] = artsy['time'].apply(get_latest)
artsy['time_earliest'] = artsy['time'].apply(get_earliest)


# merge dataframes
merge = pd.concat([artstor, met, artsy])

# write to csv
merge.to_csv("merge.tsv", sep='\t', encoding='utf-8', index=False)

