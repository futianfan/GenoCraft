import pandas as pd
import numpy as np
from numpy.random import randint, normal

# Generate list of fake protein names
proteins = ['ALB','AGT','APOA1','APOB','B2M','CALM1','CA2','CAT','C3','SERPINA5','CKM','CYP3A4','FTL','FGA','GAST','GCG','GPX1','HBA1','HIST1H1B','HIST1H2AB','HIST1H2BB','HIST1H3A','HIST1H4A','IGHA1','IGHG1','IGHD','IGHE','IGHM','INS','IFNG','KRT1','LTF','LIPA','LYZ','MB','OXT','PGA5','PRTN3','PRL','F2','REN','RNASE1','ALB','HTR2A','SOM','TSHB','TF','PRSS1','GC','VWF','ACTB','TPM1','TNNT2','TTN','MYH7','COL1A1','ELN','FN1','LAMA2','ITGAV','CDH1','SELP','CD79A','HSP90AA1','KRT5','TUBB','DYNC1H1','KIF5B','MYH6','TNNC1','VIM','LDHA','EGFR','GNAQ','JUN','SLC2A1','IGHG1','GH1','IFNG','HIST1H2BJ','HNRNPA1','SRSF2','HSPA5','RPL7','CYCS','PEX5','CTSD','CALR','GOLGB1','CETN2','KRT8','PER1','PTEN','TP53','ESR1','MAPK1','AKT1','MTOR','STAT3','SRC']

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
df.to_csv('protein_expression.csv')
