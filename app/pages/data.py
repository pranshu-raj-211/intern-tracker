from taipy import Gui
from taipy.gui import builder as tgb
import pandas as pd
import os


all_jobs = pd.DataFrame()

# TODO : refactor to use DRY


def get_paths(directories):
    """
    Generator function to yield all the paths of the files in the directories."""
    for directory in directories:
        for filename in os.listdir(directory):
            yield os.path.join(directory, filename)


def get_data(path):
    """
    Function to yield the data from the files."""
    df = pd.read_csv(path)
    return df


with tgb.Page() as data_page:
    """
    Shows the tabular data of all scraped jobs."""
    # TODO : Move to different page, data
    tgb.text("Jobs scraped from indeed on March 10th, 2024")
    tgb.table("{all_jobs}")



directories = ["data/cleaned/2024_03_11/"]
# TODO : add support for multiple sources, especially in data loading part
for path in get_paths(directories):
    data = get_data(path)
    all_jobs = pd.concat([all_jobs, data])


Gui(data_page).run(debug=True, use_reloader=True)
