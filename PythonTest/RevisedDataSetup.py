### This script is used for creating one combined CSV out of many and organizing the data before we train our model
### Author: Joe O'Neill

import os
import glob
import pandas as pd
import re

# Change into the directory containing the original CSV datasets
def set_directory(directory):
    os.chdir(directory)


# Creates a dataframe out of an input of a .csv file
def get_dataframe(input_file):
    # Create a dataframe out of the new dataset
    df = pd.read_csv(input_file)
    return df

# Attempts to find the area of a project by parsing the description for numeric values followed by ' sf'
# If no matching values are found then the size is set to 0
# If several matching values are found it takes the largest value
def add_project_size(df, output_file):
    # Expression to find all numbers followed by sf in the description after removing commas
    area = lambda x: re.findall('\d+\s[s][f]', str(x).replace(',', ''))
    df['project_size'] = df['description'].apply(area)
    # Expression to strip the sf from the number and use the highest number as the project size
    max_value = lambda y: 0 if len(y) == 0 else max([int(s.strip(' sf')) for s in y])
    df['project_size'] = df['project_size'].apply(max_value)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return df

# Takes the data frame and adds a relevance score
def add_relevance_score(df, output_file):
    # Create a new column for a 'Relevance Score' and default the value to 0
    df['relevance_score'] = 0

    ''' 
    Assign a relevance score to each project based on the max size of projects available.
    Since projects less than or equal to 50000 square feet are not considered by our client,
    we leave their relevance score at 0.
    '''
    largest_project_size = df['project_size'].max()
    df.loc[df['project_size'] > 50000, 'relevance_score'] = (df['project_size'] / largest_project_size) * 100

    # Produce a final CSV with adjusted relevance scores that we can use for training and testing data
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

def main():
    set_directory("original_csvs")
    df = get_dataframe("filtered.csv")
    df2 = add_project_size(df, "../data/size_extracted_data.csv")
    add_relevance_score(df2, '../data/complete_data.csv')

# # Execute main on initialization
if __name__ == '__main__':
    main()
