import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime

primary_color = "#00AADB"

st.set_page_config(
    page_title="Zuważalność",
    page_icon=":bar_chart:",
    layout="wide",
)


zmienne = ['PLEC','WIEK4','tematyka','wielkosc','Zauważalność']
reklama = pd.read_csv('12_reklama.txt', usecols = zmienne, sep = '\t', decimal = ",")
reklama = reklama[reklama['tematyka']!='dodatki']
#reklama = reklama[reklama['tematyka']!='męskie']
reklama = reklama[reklama['tematyka']!='magazyny specjalistyczne']

st.markdown("<h1 style='margin-top: -70px; text-align: center;'>Zuważalność</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([2,2])
with col1:
    Płeć = st.radio("Wybierz płeć:", ['Wszyscy', 'Kobiety', 'Mężczyźni'], horizontal=True, index =0)
    Wiek = st.multiselect("Wybierz grupę wiekową:", ['15-29', '30-39', '40-49', '50-59'], default=['15-29', '30-39', '40-49', '50-59'])
    if Wiek == []:
        Wiek = ['15-29', '30-39', '40-49', '50-59']
with col2:
    obrazek = "ZAUW.jpg"
    st.image(obrazek, caption='',  width = 650)

if Płeć == 'Kobiety':
    reklama = reklama[reklama['PLEC']==2]
if Płeć == 'Mężczyźni':
    reklama = reklama[reklama['PLEC']==1]
if '15-29' not in Wiek:     
    reklama = reklama[reklama['WIEK4']!=1]
if '30-39' not in Wiek:     
    reklama = reklama[reklama['WIEK4']!=2]
if '40-49' not in Wiek:     
    reklama = reklama[reklama['WIEK4']!=3]
if '50-59' not in Wiek:     
    reklama = reklama[reklama['WIEK4']!=4]

df_1 = reklama[reklama['wielkosc'] == '1/2 Page'].groupby('tematyka').agg({'Zauważalność': 'mean'}).round(1)
df_2 = reklama[reklama['wielkosc'] == 'Full Page'].groupby('tematyka').agg({'Zauważalność': 'mean'}).round(1)
df_3 = reklama[reklama['wielkosc'] == 'Double Page'].groupby('tematyka').agg({'Zauważalność': 'mean'}).round(1)
df = pd.DataFrame(pd.concat([df_1,df_2,df_3], axis = 1))
df.columns = ['1/2 strony', 'Pełna strona', 'Rozkładówka']

df = df.applymap(lambda x: str('{:,.1f}%'.format(x)).replace('.',','))
df.iloc[6,2] = '-'

if Płeć == 'Mężczyźni':
    df.iloc[2,2] = '-'
df = df.reset_index()
df.index = df.index  + 1


df = df.style.set_table_styles([
    {'selector': 'td.col0', 'props': [('text-align', 'left')]},  # Wyrównaj pierwszą kolumnę do lewej
    {'selector': 'td', 'props': [('text-align', 'center')]},  # Pozostałe komórki wyrównaj do środka
])

html_table = df.to_html()
html_table = f"<div style='margin: auto;'>{html_table}</div>"


styled_table = f"""
<style>
    table {{
        width: 100%;
        margin: auto;
        overflow-x: auto;
    }}
    th, td {{
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
        white-space: nowrap;  /* Unikaj przerywania tekstu na wielu linijkach */
    }}
</style>
{html_table}
"""

# Wyświetl sformatowaną tabelę
st.markdown(styled_table, unsafe_allow_html=True)

