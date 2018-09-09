
# coding: utf-8

# In[48]:

import pandas as pd
import numpy as np
import os, re


# In[73]:

demo = pd.read_csv(os.path.join("C:/","users","CJ","desktop","Demographics (OSLAS).txt"), 
                   sep="\t", 
                   usecols=[x for x in range(13)])


# In[74]:

demo['Postal Code'] = demo['Postal Code'].apply(lambda x: re.search(r'\d{6}', str(x).replace(' ', '')).group(0) if len(str(x).replace(' ', '')) == 6 and re.search(r'\d{6}', str(x).replace(' ', '')) != None else '')


# In[75]:

demo['Postal Code'] = demo['Postal Code'].apply(lambda x: str(x)[:2] if len(x) == 6 else x)


# In[76]:

demo['Postal Code']


# In[78]:

demo.to_csv(os.path.join("C:/","users","CJ","desktop","Demographics (OSLAS) anonymized.txt"), 
            index=False, 
            sep="\t")


# In[ ]:



