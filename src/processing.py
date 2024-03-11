import os
import pandas as pd


directories = ['data/indeed/2024_03_11']
required_columns = ['title', 'company', 'location', 'link', 'date', 'query', 'source']

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


def process_data(data, path, source):
    data = data.drop_duplicates()
    filename = str(os.path.basename(path))[:-4]
    data['query'] = ' '.join(filename.split('_'))
    data['link'] = data['link'].apply(lambda x: 'https://www.ycombinator.com/jobs/role' + str(x))
    # add source hostname to link
    data['source'] = source
    return data

# TODO : parse dates, remove jobs older than 20 days or so

def save_data(data, path):
    data.to_csv(path, index=False)

if __name__ == '__main__':
    for path in get_paths(directories):
        data = get_data(path)
        source = str(os.path.dirname(os.path.dirname(path))).split('data/')[1]
        data = process_data(data, path, source)
        path = str(path).replace(source, f'cleaned_{source}')
        save_data(data, path)
