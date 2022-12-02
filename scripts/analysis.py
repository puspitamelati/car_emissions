import pandas as pd
import numpy as np
import altair as alt
from pyodide.http import open_url

alt.renderers.set_embed_options(theme='#f1efea')
#alt.themes.enable('#f1efea')

url = "https://raw.githubusercontent.com/puspitamelati/car_emissions/main/dataset/Sample_CO2.csv"
df = pd.read_csv(open_url(url))

#data cleaning
df.dropna()
df = df.drop(columns=['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11' ], index=None)
df.columns = ['Model', 'Produsen', 'Model_1', 'Vehicle Class', 'Engine_Size', 'Cylinders','Transmission', 'Fuel', 'Fuel_Consumption', 'CO2_Emissions']

df['Rank'] = df['CO2_Emissions'].rank()
df['Rank_Produsen'] = df.groupby(['Produsen'])['CO2_Emissions'].rank()

#add selection
selec = alt.selection_multi(encodings=['y'])

#grafik Rata-rata Emisi CO2 tiap Kelas Kendaraan
v_class = alt.Chart(df, title = 'Rata-rata Emisi CO2 tiap Kelas Kendaraan').mark_bar().encode(
    alt.Y('Vehicle Class'),
    alt.X('average(CO2_Emissions):Q',
          axis=alt.Axis(title='Rata-rata Emis CO2')),
    color = alt.condition(selec, alt.value("#2F4F4F"), alt.value("grey"))
).properties(width = 400
).add_selection(selec)

#konsumsi bahan bakar dan emisi CO2 tiap banyaknya Silinder
cylind_cons = alt.Chart(df).mark_bar(color = '#2F4F4F').encode(
    alt.X('Cylinders:O'),
    alt.Y('average(Fuel_Consumption):Q',
         axis=alt.Axis(labelColor='#2F4F4F', titleColor='#2F4F4F'))
).properties(width = 400)

cylind_emis = alt.Chart(df).mark_line(color='black', interpolate='monotone').encode(
    alt.X('Cylinders:O'),
    alt.Y('average(CO2_Emissions)', 
          axis=alt.Axis(labelColor='black', titleColor='black'))  
).properties(width = 400)

#Gabungkan cylind_cons dan cylin_emis 
cylind = alt.layer(cylind_cons, cylind_emis).resolve_scale(
    y = 'independent' 
).properties(
    title = "Rata-rata Konsumsi Bahan Bakar dan Rata-rata Emisi CO2 tiap Silinder"
).add_selection(selec
).transform_filter(
    selec)

#emisi dan konsumsi bahan bakar tiap jenis transmisi
transmission_cons= alt.Chart(df).mark_bar(color = '#2F4F4F').encode(
    alt.X('Transmission'),
    alt.Y('average(Fuel_Consumption):Q',
          axis=alt.Axis(labelColor='#2F4F4F', titleColor='#2F4F4F')) 
).properties(width = 400)

transmission_emis= alt.Chart(df).mark_line(color = 'black', interpolate='monotone').encode(
    alt.X('Transmission'),
    alt.Y('average(CO2_Emissions):Q',
          axis=alt.Axis(labelColor='black', titleColor='black')) 
).properties(width = 400)

#gabungkan transmission_cons dan transmission_emis 
transmission = alt.layer(transmission_cons, transmission_emis).resolve_scale(
    y = 'independent' 
).properties(
    title = "Rata-rata Konsumsi Bahan Bakar dan Rata-rata Emisi CO2 tiap Jenis Transmisi"
).add_selection(selec
).transform_filter(
    selec)

#emisi dan konsumsi bahan bakar tiap jenis bahan bakarnya
fuel_cons = alt.Chart(df).mark_bar(color = '#2F4F4F').encode(
    alt.X('Fuel'),
    alt.Y('average(Fuel_Consumption):Q',
          axis=alt.Axis(labelColor='#2F4F4F', titleColor='#2F4F4F')) 
).properties(width = 400)

fuel_emis = alt.Chart(df).mark_line(color = 'black', interpolate = 'monotone').encode(
    alt.X('Fuel'),
    alt.Y('average(CO2_Emissions)',
          axis=alt.Axis(labelColor='black', titleColor='black')) 
).properties(width = 400)

fuel = alt.layer(fuel_cons, fuel_emis).resolve_scale(
    y = 'independent' 
).properties(
    title = "Rata-rata Konsumsi Bahan Bakar dan Rata-rata Emisi CO2 tiap Jenis Bahan Bakar"
).add_selection(selec
).transform_filter(
    selec)

#pengaruh ukuran mesin terhadap konsumsi energi
engine = alt.Chart(df, title='Pengaruh Ukuran Mesin terhadap Konsumsi Energi').mark_line(color = '#2F4F4F').encode(
    alt.X('Engine_Size'),
    alt.Y('average(Fuel_Consumption):Q')  
).properties(width = 400)

#pengaruh konsumsi energi terhadap emisi CO2
fuel_emission = alt.Chart(df, title ='Pengaruh Konsumsi Energi terhadap Emisi CO2 ').mark_line(color='#2F4F4F').encode(
    alt.X('Fuel_Consumption:Q'),
    alt.Y('average(CO2_Emissions):Q'),
).properties(width = 400
).add_selection(selec
).transform_filter(
    selec)

alt.vconcat(v_class & fuel_emission & engine | cylind & transmission & fuel)