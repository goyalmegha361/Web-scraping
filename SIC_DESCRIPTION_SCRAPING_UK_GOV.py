#Import python libraries
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import time

#Read the policyholder names in pandas dataframe.
df = pd.read_excel('PolicyHolderName.xlsx')

data=pd.DataFrame()
desired_model_queries = df['Policy Holder Names']

for query in desired_model_queries:
    url = 'https://beta.companieshouse.gov.uk/search?q=' + query
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    try:
        link=soup.findAll('a', attrs={'href': re.compile("/company/[0-9]")})
        a=link[0].get('href')
        url2 = 'https://beta.companieshouse.gov.uk'+ a
        content = requests.get(url2)
        soup = BeautifulSoup(content.content, 'html.parser')
        sic_code=soup.find(id='sic0').get_text()    
        
    except Exception as e:
        sic_code='NA'
    data = data.append({'Policy Holder Names':query, 'Description':sic_code.strip()}, ignore_index=True) 

data = data[['Policy Holder Names', 'Description']]
    
#Output data to a CSV file.   
data.to_csv('SIC_description_output.csv')    

