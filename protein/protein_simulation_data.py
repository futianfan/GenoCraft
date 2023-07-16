import pandas as pd
import numpy as np
from numpy.random import randint, normal

# Generate list of fake protein names
proteins = ['PROT_'+str(i) for i in range(1,101)] 

# Create dataframe
df = pd.DataFrame(index=proteins, 
                  columns=['Patient_'+str(i) for i in range(1,51)])

# Add random expression values
for protein in df.index:
    for sample in df.columns:
        df.loc[protein,sample] = round(normal(loc=randint(100,150), scale=15),1)

# Introduce 50% missing data
for i in range(df.shape[0]):
    for j in range(df.shape[1]):
        if np.random.rand() < 0.5:
            df.iloc[i,j] = np.nan

# Display dataframe snippet            
df.head()

# Add random expression values 
for protein in df.index:
    for sample in df.columns:
        df.loc[protein,sample] = round(normal(loc=randint(100,150), scale=15),1)
        
# Display snippet

df.to_csv('protein_expression.csv')
