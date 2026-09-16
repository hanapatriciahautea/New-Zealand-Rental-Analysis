import pandas as pd

listings = pd.read_csv("listings.csv") ##

print(listings.head()) ##print the first 5 rows of the dataframe


print(listings.shape) ##print the number of rows and columns in the dataframe
print(listings.columns) ##print the column names in the dataframe
print(listings.info()) ##print information about the dataframe
