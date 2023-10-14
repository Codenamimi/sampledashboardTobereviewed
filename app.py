#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import streamlit as st


# In[3]:


st.set_page_config(
    page_title="July 2023 Sales Dashboard", 
    page_icon=":bar_chart:", 
    layout="wide"
                  )


# In[7]:


df=pd.read_csv('Sample_72023 (2).csv')
print(df)


# In[8]:


import pandas as pd
import streamlit as st

df = pd.read_csv('Sample_72023 (2).csv')
st.dataframe(df)


# In[10]:


st.line_chart(df)


# In[ ]:





# In[3]:


pip install plotly-express

