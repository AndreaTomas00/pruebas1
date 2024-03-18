import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Evolució ofertes i trasplantaments 2023",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

data = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")
data['MONTH'] = pd.to_datetime(data['DATA'], format='%d/%m/%y').dt.month

mapping2 = {1: 'Gener', 2:'Febrer', 3: 'Març', 4: 'Abril', 5: 'Maig', 6: 'Juny', 7: 'Juliol', 8: 'Agost', 9:'Setembre', 10: 'Octubre', 11:'Novembre', 12:'Desembre'}
data['MES']=data['MONTH'].map(mapping2)
data['MES'] = pd.Categorical(data['MES'], categories=['Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre'], ordered=True)


data.sort_values(by="MONTH", axis=0)
data['EXTRA'] ='Ofertes'

line = alt.Chart(data).mark_area().encode(
    x=alt.X('MES:O', title='Mes', axis=alt.Axis(labelAngle=0), sort=list(mapping2.values())),
    y = alt.Y('count():Q', scale=alt.Scale(domain=[0,30])),
    tooltip = ['MES:N',alt.Tooltip('count():Q', title='Valor')],
    color = alt.Color('EXTRA', scale = alt.Scale(domain=['Ofertes'], range=['#fdae61']), title='Categoria')
).properties(width=1000 ,title="")

data_ofertes = data[data['RESULTAT']=="Acceptat i trasplantat"]
data_ofertes['EXTRA'] ='Trasplantaments'

line2 = alt.Chart(data_ofertes).mark_area(color='#b4deae').encode(
    x=alt.X('MES:O', title='Mes', axis=alt.Axis(labelAngle=0), sort=list(mapping2.values()) ),
    y = alt.Y('count():Q', scale=alt.Scale(domain=[0,30])), 
    tooltip = ['MES:N',alt.Tooltip('count():Q', title='Valor')],
    color = alt.Color('EXTRA', scale = alt.Scale(domain=['Trasplantaments'], range=['#b4deae']), title='Categoria')
).properties(width=1000 ,title="")

final = alt.layer(line,line2).configure_title( fontSize=26).resolve_scale(color='independent')


color_procedencia = alt.Scale(domain=["VHMI", "SANT PAU", "HCP", "BLLV", "ONT"],
                        range=['#FFFC9B', '#FDE767', '#FFD966', '#F3B95F',  '#3E77B6' ]
                        )
color_tipo=alt.Scale(domain=['Adult', 'Infantil'], range=['#FFFC9B', '#FDE767'])
st.write("# Evolució ofertes i trasplantaments 2023")
st.altair_chart(final)

urg = [123, 7, 7, 4,20,15]
Hospis = ['ONT-Adult', 'BLLV', 'HCP', 'SANT PAU','ONT-Infantil', 'VHMI']
datos = pd.DataFrame()
datos['Hospital'] = Hospis
datos['count'] = urg
datos['code'] = [1,2,3,4,5,6]

chart = alt.Chart(datos).mark_bar(color='#3288bd').encode(
    x=alt.X('Hospital:N',  axis=alt.Axis(labelAngle=0), title="Tipus d'urgència", 
            scale=alt.Scale(domain=['ONT-Adult', 'BLLV', 'HCP', 'SANT PAU','ONT-Infantil', 'VHMI'])),
    y='count:Q',
    tooltip = ['Hospital', alt.Tooltip('count:Q', title='Valor')],
    order = 'code:Q'
).properties(width=1000 ,title="")

text_propis = alt.Chart(datos).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('Hospital:N'),
    y = alt.Y('sum(count):Q'),
    text=alt.Text('sum(count):Q', format='.0f'),
    order = 'code:Q',
    color = alt.value("black"),
)

total = (chart+text_propis).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)
st.write("# Total urgències 0")
st.altair_chart(total)
st.write("ONT-Adults i ONT-Infantil no inclouen les Urgències 0 de l'OCATT")

