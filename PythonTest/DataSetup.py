### This script is used for creating one combined CSV out of many and organizing the data before we train our model
### Author: Joe O'Neill

import os
import glob
import pandas as pd

# Change into the directory containing the original CSV datasets
def set_directory(directory):
    os.chdir(directory)

# Create a master CSV with data from all the provided files
def create_combined_csv(output_file):
    # Use glob to get all files with a .csv extension in a list
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #Combine all the files in the list using pandas
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ], sort=False)

    # Export the combined data to a single csv in the data folder
    combined_csv.to_csv(output_file, index=False, encoding='utf-8-sig')

# Remove all duplicated data from a the CSV
def remove_duplicate_rows(input_file, output_file):
    # Create a dataframe out of the new dataset
    df = pd.read_csv(input_file)

    # Remove all duplicated rows
    df.drop_duplicates(subset=None, inplace=True)

    # Create a new CSV out of the data frame with all duplicates removed
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    return df

# Takes the data frame after duplicates have been removed and adds a relevance score
def add_relevance_score(df, output_file):
    # Create a new column for a 'Relevance Score' and default the value to 0
    df['relevance_score'] = 0

    # Convert the OBJECTIDs from strings into numerical values
    df['OBJECTID'] = df['OBJECTID'].str.replace(",", "").astype(float)

    ''' 
    Assign a relevance score to each project based on the max size of projects available.
    Since projects less than or equal to 50000 square feet are not considered by our client,
    we leave their relevance score at 0.
    '''
    largest_project_size = df['OBJECTID'].max()
    df.loc[df['OBJECTID'] > 50000, 'relevance_score'] = (df['OBJECTID'] / largest_project_size) * 100

    # Produce a final CSV with adjusted relevance scores that we can use for training and testing data
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

def main():
    set_directory("original_csvs")
    create_combined_csv("../data/combined_csv.csv")
    df = remove_duplicate_rows('../data/combined_csv.csv', '../data/clean_output.csv')
    add_relevance_score(df, '../data/complete_data.csv')

# # Execute main on initialization
# if __name__ == '__main__':
#     main()
