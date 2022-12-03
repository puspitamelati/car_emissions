import pandas as pd
import numpy as np
import altair as alt
from pyodide.http import open_url

url = "https://raw.githubusercontent.com/puspitamelati/car_emissions/main/dataset/Sample_CO2.csv"
df = pd.read_csv(open_url(url))

alt.renderers.set_embed_options(theme='light')

#data cleaning
df.dropna()
df = df.drop(columns=['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11' ], index=None)
df.columns = ['Model', 'Produsen', 'Model_1', 'Vehicle Class', 'Engine_Size', 'Cylinders','Transmission', 'Fuel', 'Fuel_Consumption', 'CO2_Emissions']

df['Rank'] = df['CO2_Emissions'].rank()
df['Rank_Produsen'] = df.groupby(['Produsen'])['CO2_Emissions'].rank()

selec = alt.selection_multi(encodings=['y'])

#Vehicle summary
#top 10 produsen and vehicle class with low carbon emissions

prod = alt.Chart(df, title='Rata-rata Emisi CO2 tiap Produsen Kendaraan').mark_bar(color = '#2F4F4F').encode(
    alt.Y('Produsen', sort='-x'),
    alt.X('average(CO2_Emissions)'),
    color = alt.condition(selec, alt.value("#2F4F4F"), alt.value("grey"))
).transform_filter(alt.FieldRangePredicate(field='Rank', range=[1, 15])
).add_selection(selec)

top = alt.Chart(df, title='Rata-rata Emisi CO2 tiap Kelas Kendaraan ').mark_bar(color='#2F4F4F').encode(
    alt.X('average(CO2_Emissions)',
         axis= alt.Axis(title='Rata-rata Emisi Karbon Dioksida')),
    alt.Y('Vehicle Class', sort='-x
         axis = alt.Axis(title='Produsen'))
).transform_filter(alt.FieldRangePredicate(field='Rank_Produsen', range=[1, 15])
).add_selection(selec
).transform_filter(selec)

prod|top
