import os
import pandas as pd


directories = ["data/raw/indeed/", "data/raw/yc"]
required_columns = [
    "title",
    "company",
    "salary",
    "location",
    "link",
    "date",
    "query",
    "source",
]
dataframes = []

# TODO: add aggregation of jobs - return a single csv file for all


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


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'


def process_data(data, source):
    data = data.drop_duplicates()
    data = data.dropna(axis=0, subset=["title", "link"])

    data["source"] = source
    if source == "indeed":
        data["link"] = data["link"].apply(lambda x: "https://in.indeed.com" + str(x))
    elif source == "yc":
        data["link"] = data["link"].apply(
            lambda x: "https://www.ycombinator.com/jobs/role" + str(x)
        )
    # add source hostname to link

    columns = set(data.columns)
    if columns != set(required_columns):
        absent_columns = set(required_columns) - columns
        if "salary" in absent_columns:
            data["salary"] = "Not Specified"

    if "duration" in columns:
        data = data.drop(columns=["duration"])

    # set column order to a standard order
    data = data[required_columns]

    # Substitute 'Not Specified' where salary is NaN
    data["salary"] = data["salary"].fillna("Not Specified")

    return data


# TODO : parse dates, remove jobs older than 20 days or so
# TODO : if all required columns not present, init with empty values


if __name__ == "__main__":
    for path in get_paths(directories):
        data = get_data(path)
        source = source = os.path.basename(os.path.dirname(path))
        data = process_data(data, source)
        path = str(path).replace("raw", "cleaned")
        #data.to_csv(path, index=False)
        dataframes.append(data)
    if len(dataframes) != 0:
        aggregated_data = pd.concat(dataframes, ignore_index=True)
        print(len(aggregated_data))
        aggregated_data.to_csv("data/processed/aggregate.csv",index=False)
    else:
        print('No dataframes to aggregate')