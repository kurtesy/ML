# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 23:04:48 2018

@author: npatel
"""

"""Basic imports and setup for data analysis"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 20)

"""Read and refine base raw data"""
companies = pd.read_csv(r'C:\Users\npatel\Desktop\Upgrad\companies.txt', sep='\t', lineterminator='\n', encoding='ISO-8859-1')
rounds2 = pd.read_csv(r'C:\Users\npatel\Desktop\Upgrad\rounds2.csv', encoding='ISO-8859-1')

"""Join round2 and companies data"""
print(companies.head())
x = pd.unique(rounds2['company_permalink'].str.lower()).tolist()
y = pd.unique(companies.str.lower()).tolist()
companies['permalink'] = companies['permalink'].str.lower()
rounds2['company_permalink'] = rounds2['company_permalink'].str.lower()
print(list(set(x).difference(set(y))))
print(companies.columns)
print(rounds2.columns)
master_frame = pd.merge(rounds2, companies, how='left', left_on='company_permalink', right_on='permalink')

"""Funding Analysis and Spark Fund Requirements"""
print(master_frame)
funding_frame = master_frame[['funding_round_type', 'raised_amount_usd']]
avg_summary_funding_frame = funding_frame.groupby(funding_frame['funding_round_type'], as_index=False).mean()
print(avg_summary_funding_frame)
avg_summary_funding_frame.plot.bar(x='funding_round_type', y='raised_amount_usd')
plt.savefig(r'C:\Users\npatel\Desktop\Upgrad\output.jpeg')
print(avg_summary_funding_frame[(5000000<=avg_summary_funding_frame.raised_amount_usd) & (avg_summary_funding_frame.raised_amount_usd<=15000000)])

"""Top 9 countries for FT: Venture"""
venture_frame = master_frame[(master_frame.funding_round_type == 'venture')]
top9 = venture_frame.groupby(venture_frame['country_code']).sum().nlargest(9,'raised_amount_usd')
print(top9)
plt.figure()
top9.plot(kind='bar')

"""Sector Mapping and Primary category listing"""
master_frame['category_list'] = master_frame['category_list'].str.split('|')
master_frame['primary_sector'] = master_frame.category_list.str[0]
mapping = pd.read_csv(r'C:\Users\npatel\Desktop\Upgrad\mapping.csv', encoding='ISO-8859-1')
sector_list = mapping.columns.tolist()[1:]
sector_list.remove('Blanks')
for sector in sector_list:
    mapping[sector] = mapping[sector].apply(lambda z: sector if z==1 else '')
mapping['main_sector'] =  mapping[sector_list[0]]
for sector in sector_list[1:]:
    mapping['main_sector'] = mapping['main_sector'] + mapping[sector]
mapping = mapping.drop(columns=sector_list+['Blanks'])
master_sector_frame = pd.merge(master_frame, mapping, how='left', left_on='primary_sector', right_on='category_list')

"""Sector Analysis 1 and 2, FT: Venture, Top 3 sectors country wise"""
master_sector_frame = master_sector_frame.dropna()

# Country: USA, FT: venture
D1 = master_sector_frame[(master_sector_frame['country_code'] == 'USA') & (master_sector_frame['funding_round_type'] == 'venture')]
D1_sector_investments = D1.groupby('main_sector').agg({'funding_round_type':'count',
                                                      'raised_amount_usd': 'sum'}).reset_index().rename(columns={'funding_round_type':'investment_count',
                                                                                                                 'raised_amount_usd': 'total_investments'})
D1 = pd.merge(D1, D1_sector_investments, how='left', left_on='main_sector', right_on='main_sector')
print(D1_sector_investments['investment_count'].sum())
print(D1_sector_investments['total_investments'].sum())
print(D1_sector_investments.nlargest(8,'investment_count'))

D1_sector_investments = D1_sector_investments.nlargest(3,'investment_count')
D1_sector_investments['country'] = D1_sector_investments.investment_count.apply(lambda x: 'USA')
print(D1[D1.main_sector=='Cleantech / Semiconductors'].nlargest(1,'raised_amount_usd'))

# Country: GBR, FT: venture
D2 = master_sector_frame[(master_sector_frame['country_code'] == 'GBR') & (master_sector_frame['funding_round_type'] == 'venture')]
D2_sector_investments = D2.groupby('main_sector').agg({'funding_round_type':'count',
                                                      'raised_amount_usd': 'sum'}).reset_index().rename(columns={'funding_round_type':'investment_count',
                                                                                                                 'raised_amount_usd': 'total_investments'})
D2 = pd.merge(D2, D2_sector_investments, how='left', left_on='main_sector', right_on='main_sector')
print(D2_sector_investments['investment_count'].sum())
print(D2_sector_investments['total_investments'].sum())
print(D2_sector_investments.nlargest(8,'investment_count'))
D2_sector_investments = D2_sector_investments.nlargest(3,'investment_count')
D2_sector_investments['country'] = D2_sector_investments.investment_count.apply(lambda x: 'GBR')
print(D2[D2.main_sector=='Cleantech / Semiconductors'].nlargest(1,'raised_amount_usd'))

# Country: CAN, FT: venture
D3 = master_sector_frame[(master_sector_frame['country_code'] == 'CAN') & (master_sector_frame['funding_round_type'] == 'venture')]
D3_sector_investments = D3.groupby('main_sector').agg({'funding_round_type':'count',
                                                      'raised_amount_usd': 'sum'}).reset_index().rename(columns={'funding_round_type':'investment_count',
                                                                                                                 'raised_amount_usd': 'total_investments'})
D3 = pd.merge(D3, D3_sector_investments, how='left', left_on='main_sector', right_on='main_sector')
print(D3_sector_investments['investment_count'].sum())
print(D3_sector_investments['total_investments'].sum())
print(D3_sector_investments.nlargest(8,'investment_count'))

D3_sector_investments = D3_sector_investments.nlargest(3,'investment_count')
D3_sector_investments['country'] = D3_sector_investments.investment_count.apply(lambda x: 'CAN')
print(D3[D3.main_sector=='Cleantech / Semiconductors'].nlargest(1,'raised_amount_usd'))

#Combine all the dataframe to for the top 3 counties to for the data set for plotting of final data for main sectors
# Main sectors as analysed are listed below
# 1. Other - Catgory = Education
# 2. 

pd.concat([D1_sector_investments[['investment_count', 'main_sector']],
           D2_sector_investments[['investment_count', 'main_sector']],
           D3_sector_investments[['investment_count', 'main_sector']]]).plot.bar(x='main_sector', y='investment_count')
    
plot_all = pd.DataFrame()

# Concluson for the sector analysis as a whole is that
