import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime

primary_color = "#00AADB"

st.set_page_config(
    page_title="Zauważalność",
    page_icon=":bar_chart:",
    layout="wide",
)


zmienne = ['PLEC','WIEK4','tematyka','wielkosc','Zauważalność']
reklama = pd.read_csv('12_reklama.txt', usecols = zmienne, sep = '\t', decimal = ",")
reklama.columns = ['PLEC','WIEK4','Tematyka','wielkosc','Zauważalność']
reklama = reklama[reklama['Tematyka']!='dodatki']
reklama = reklama.replace('męskie','magazyny budowlane, magazyny motoryzacyjne, magazyny popularno-naukowe')
reklama = reklama.replace('magazyny specjalistyczne','magazyny budowlane, magazyny motoryzacyjne, magazyny popularno-naukowe')
reklama = reklama.replace('kobiece poradniki/hobbystyczne','magazyny kobiece poradnikowe, magazyny hobbystyczne')
reklama = reklama.replace('kobiece rozrywka/historie/people','magazyny poradniczo-rozrywkowe, magazyny people')
reklama = reklama.replace('społeczne','magazyny opinii (społeczno-polityczne)')
reklama = reklama.replace('telewizyjne','magazyny telewizyjne')

st.markdown("<h1 style='margin-top: -70px; text-align: center;'>Zauważalność reklam w prasie</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""<div style="font-size:20px; font-weight:bold">Średnia zauważalność reklam</div>""", unsafe_allow_html=True)
    st.markdown("""<div style="font-size:12px">(prawdopodobieństwo, że reklama będzie zauważona)</div>""", unsafe_allow_html=True)
    obrazek = "zauw.jpg"
    st.image(obrazek, caption='',  width = 690)

st.markdown("""<div style="font-size:20px; font-weight:bold">Średnia zauważalność reklam według grup celowych i tematyki</div>""", unsafe_allow_html=True)


Płeć = st.radio("Wybierz płeć:", ['Wszyscy', 'Kobiety', 'Mężczyźni'], horizontal=True, index =0)
Wiek = st.multiselect("Wybierz grupę wiekową:", ['15-29', '30-39', '40-49', '50-59'], default=['15-29', '30-39', '40-49', '50-59'])
if Wiek == []:
    Wiek = ['15-29', '30-39', '40-49', '50-59']

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

df_1 = reklama[reklama['wielkosc'] == '1/2 Page'].groupby('Tematyka').agg({'Zauważalność': 'mean'}).round(1)
df_2 = reklama[reklama['wielkosc'] == 'Full Page'].groupby('Tematyka').agg({'Zauważalność': 'mean'}).round(1)
df_3 = reklama[reklama['wielkosc'] == 'Double Page'].groupby('Tematyka').agg({'Zauważalność': 'mean'}).round(1)
df = pd.DataFrame(pd.concat([df_1,df_2,df_3], axis = 1))
df.columns = ['1/2 strony', 'Pełna strona', 'Rozkładówka']

df = df.applymap(lambda x: str('{:,.1f}%'.format(x)).replace('.',','))
df.iloc[6,2] = '-'

if Płeć == 'Mężczyźni':
    df.iloc[2,2] = '-'
df = df.reset_index()
df.index = df.index  + 1

df_styled = df.style.set_table_styles([
    {'selector': 'td.col0', 'props': [('text-align', 'left')]},  # Wyrównaj pierwszą kolumnę do lewej
    {'selector': 'th.index', 'props': [('text-align', 'center')]},  # Wyśrodkuj indeksy w pierwszej kolumnie
    {'selector': 'th, td', 'props': [('text-align', 'center')]},  # Pozostałe komórki wyrównaj do środka
    {'selector': 'th.col0', 'props': [('text-align', 'left')]}
])

html_table = df_styled.to_html()
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

st.markdown("""<div style="font-size:12px">Wskaźniki: Zauważalność reklamy (druk i e-wydania),  Dane eye tracking, Liczba przypadków = 13723</div>""", unsafe_allow_html=True)


