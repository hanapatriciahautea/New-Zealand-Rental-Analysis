'''Explain what programme is mean to do'''

#placeholder: add any constants here

import pandas as pd
import matplotlib.pyplot as plt

def create_histogram(dataframe, column_name):
    '''Create a histogram for a specified column in the "listings" dataframe.'''
    plt.hist(dataframe[column_name].dropna(), bins=60)
    plt.xlabel(column_name)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column_name}')
    plt.grid(axis='y')
    plt.show()

    #source 1: https://www.geeksforgeeks.org/python/matplotlib-pyplot-hist-in-python/
    #source 2: https://matplotlib.org/stable/tutorials/pyplot.html
    #source 3: https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html

def main():
    '''
    Main function to execute the program.    
    This function reads the listings data and creates a histogram for a specified column.
    '''
    listings = pd.read_csv("listings.csv") #reads csv data into "listings" dataframe
    listings['days_since_last_review'] = 1 #adds a new column to the dataframe with a default value of 1

    create_histogram(listings, 'price') # Create a histogram for price
    create_histogram(listings, 'days_since_last_review') # Create a histogram for days since last review

main()