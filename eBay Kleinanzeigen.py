#!/usr/bin/env python
# coding: utf-8

# 
#  #                                      eBay Kleinanzeigen
#  

# The aim of this project is to clean the data and analyze the included used car listings from a classifieds section of the German eBay website. The dataset can be found on data.world

# In[245]:


import pandas as pd
import numpy as np

# Importing Pandas and Numpy libraries


# In[246]:


# Reading the autos.csv file into pandas

autos = pd.read_csv('C:\\Users\koraim\\OneDrive - Dell Technologies\\Desktop\\Data Science\\Datasets\\autos.csv', encoding= "Windows-1252")


# In[247]:


# Exploring the dataset, especially the first 5 rows

autos.head()
autos.info()


# In[248]:


autos # Exploring the first and last five rows of pandas object "autos"


# The dataset consists of 20 columns and 50,000 data points. Some columns contain null values like the vehicleType, powerPS, notRepairedDamage. Also the dataset naming convention is camel case instead of snake case.

# In[249]:




autos.columns  # printing an array which consists of the exisiting column names

autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'powerPS', 'model',
       'kilometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']    # Columns names changed to snakecase


autos.head()


# We started data cleaning by converting the column names from camelcase into snakecase.

# We will now do some basic data explortion using the df.describe() and series.value_counts()  , we will look out for:
# 
# * Numeric data stored as text
# * Columns where most/all the values are the same and see if we can drop them from our analysis.
# 

# In[250]:


autos.describe(include='all')
autos['price'].value_counts()

autos.rename(columns={'kilometer':'odemeter_km'}, inplace=True) # We changed the name of column kilometer to odemeter_km

autos["odemeter_km"].head()


# As we continue to observe our dataset here, it seems *seller* and *price* columns have only 2 unique values. Also the *nr_of_pictures* column has 0 values.
# 
# The *price* column has 1421 values of $0. We may want to leave out those rows before we prceed with our analysis.
# 
# So let's start by cleaning the **price** column:

# In[251]:


#cleaning the price column:

autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )
autos["price"].head()






# The **price** column is in good shape now, we shift towards the **odemeter** column and clean it as well:

# In[252]:


#Cleanng the odemeter_km column:
autos["odemeter_km"] = (autos["odemeter_km"]
                          .str.replace("km","")
                          .str.replace(",","")
                          .astype(int)
                          )
autos["odemeter_km"].head()


# We will now proceed by dropping columns(**seller, offer_type and nr_of_pictures**)`as they have same unique values or 0.

# In[253]:


#Removing the seller, offer_type and nr_of_pictures columns from our dataset:

autos = autos.drop(["seller","offer_type","nr_of_pictures"],axis=1)




# Let's continue exploring the dataset, we will now investigate the values itself and check if we have any unrealistic ones:

# In[254]:



autos.describe()


# As we continue to investigate the data, we start with the **price** column:

# In[255]:


# checking the values of the price column:

print(autos['price'].unique().shape) #to see the unique values

autos['price'].describe() # to check max/min/mean


# In[256]:


# changing the format to show floats with 1 decimal place:
pd.options.display.float_format = '{:,.1f}'.format
autos['price'].describe()


# In[257]:


values = autos['price'].value_counts()
values.sort_index(ascending=False).head(20) # Sorting the values of column price in descending order


# We have some values above 350,000 which could be considered as outliers. Also the the values above 1 million seem very odd.

# In[258]:


values.sort_index(ascending=True).head(20) # Exploring the other way


# We will consider any value less than 1$ and above 350,000 as outlier so proceeding with removing them:

# In[259]:


autos = autos[autos["price"].between(1,350000)] #Keeping the price values which is between 1 and 350,000


# Then, we will switch to the odemeter_km column and check its values and remove any outliers as well:

# In[260]:


print(autos["odemeter_km"].value_counts().sort_index(ascending=True).head(30)) #Exploring the data in the odemeter column

pd.options.display.float_format = '{:,.1f}'.format

autos["odemeter_km"].describe()


# We will leave the **odemeter_km** as it is as I cant see any outlier value. Moving on now to the date columns and check their data ranges:

# In[261]:


autos["registration_year"].describe()


# It seems we have unrelaistic year values here as the minimum is 1000. Maximum year value is 9999 which way ahead in the future as well so we will remove the outliers of the year range 1900-2016:

# In[262]:


autos = autos[autos["registration_year"].between(1900,2016)] #keeping only years between 1900 and 2016

print(autos['registration_year'].describe())


# Now, we will have a look on which of the car brands have highest price, we will begin to explore the brand column as follows:

# In[263]:


brands = autos["brand"].value_counts(normalize=True) # We check the brands of the listings, and how big is its representation
print(brands)
print(brands.index)


# In[ ]:





# The German manufactures represent 50% of the top 10 brands in the car listings. VW is the most popular, followed by BMW, Opel, Mercedes and last but not least Audi. 
# 
# Lots of brands do not have significant percentage of listings, so we will remove any brand which have lessa than 5% representation in the following step.

# In[264]:


common_brands = brands[brands > 0.05].index
print(common_brands)


# In[266]:


brands_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos['brand'] == brand]
    mean_price = brand_only['price'].mean()
    brands_mean_prices[brand] = int(mean_price)

brands_mean_prices
    
    


# So between our top 5 brands, Audi is in the top regarding average price. VW is in between which may explain its popularity.
