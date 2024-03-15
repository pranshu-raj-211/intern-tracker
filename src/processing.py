import os
import pandas as pd


directories = ['data/raw/indeed/', 'data/raw/yc']
required_columns = set(['title', 'company', 'salary', 'location', 'link', 'date', 'query', 'source'])

# TODO: add aggregation of jobs - return a single csv file for all


def get_paths(directories):
    '''
    Generator function to yield all the paths of the files in the directories.'''
    for directory in directories:
        for filename in os.listdir(directory):
            yield os.path.join(directory, filename)


def get_data(path):
    '''
    Function to yield the data from the files.'''
    df = pd.read_csv(path)
    return df


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{"apply"}</a>'


def process_data(data, path, source):
    data = data.drop_duplicates()
    data['source'] = source
    if source =='indeed':
        data['link']=data['link'].apply(lambda x:'https://in.indeed.com' + str(x))
    elif source =='yc':
        data['link'] = data['link'].apply(lambda x: 'https://www.ycombinator.com/jobs/role' + str(x))
    # add source hostname to link
    
    data.style.format({'link':make_clickable})
    columns = set(data.columns)
    if columns!=required_columns:
        absent_columns = required_columns-columns
        if 'salary' in absent_columns:
            data['salary']='Not Specified'

    if 'duration' in columns:
        data=data.drop(columns=['duration'])
    return data

# TODO : parse dates, remove jobs older than 20 days or so
# TODO : if all required columns not present, init with empty values


if __name__ == '__main__':
    for path in get_paths(directories):
        data = get_data(path)
        source = str(os.path.dirname(os.path.dirname(path))).split('data/')[1]
        data = process_data(data, path, source)
        path = str(path).replace('raw', 'cleaned')
        data.to_csv(path, index=False)
