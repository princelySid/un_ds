# %%
from datetime import date
from turtle import shape
import pandas as pd
# %%
def get_date_data(dataframe, date_column):
    '''
    Create columns with date data from the data:
        month
        weekday
        day_of_month
        week_of_year
    '''
    date_column = str(date_column)

    dataframe[date_column] = pd.to_datetime(dataframe[date_column])

    dataframe['year'] = dataframe[date_column].dt.strftime('%Y')
    dataframe['month'] = dataframe[date_column].dt.strftime('%b')
    dataframe['weekday'] = dataframe[date_column].dt.strftime('%a')
    dataframe['day_of_month'] = dataframe[date_column].dt.strftime('%d')
    dataframe['week_of_year'] = dataframe[date_column].dt.strftime('%U')
    # dataframe['hour'] = dataframe[date_column].dt.strftime('%H')
# %%
raw = pd.read_csv('mwi_precipitation_adm2.csv')
# %%
del raw['Unnamed: 0']

# %%
dated = raw.copy()
dated['less_2'] = dated['total_prec']<2
get_date_data(dated, 'date')
dated.sort_values(by=['pcode', 'date'], inplace=True)
# %%
dated['start'] = dated['less_2'].ne(dated['less_2'].shift())
dated['streak_id'] = dated['start'].cumsum()
sc = dated[dated['less_2']==True]
(sc['streak_id'].value_counts().reset_index(drop=True)>=14).value_counts()
# %%
q2 = dated[(dated['month']=='Jan')| (dated['month']=='Feb')| (dated['month']=='Dec') ]
q2 = q2[q2['less_2'] == True]
q2fill = q2.groupby(['pcode', 'year'])['streak_id'].count().rename('counts').reset_index()
print(q2fill.shape)
q2fill2 = q2fill[q2fill['counts']>=14]
print(q2fill.shape)
# %%
q2fill2['year'].nunique()
# %%
q2s = q2['streak_id'].value_counts().rename('streak_size').reset_index()
q2s14 = q2s[q2s['streak_size']>=14]
# %%
dated[dated['streak_id'].isin(q2s14['index'])]['year'].nunique()
# %%
dated['year'].nunique()
# %%
dated[dated['streak_id'].isin(q2s14['index'])].groupby('year')['pcode'].nunique()
