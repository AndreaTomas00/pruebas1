import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Global trasplataments cardíacs",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Global trasplataments cardíacs")

color_urg = alt.Scale(domain=["Urg 0", "Urg 1", "Electiu"],
                        range=['#D46B77', '#FFA04D', '#5895c2' ]
                        )

data1 = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")

orden = ["Urg 0", "Urg 1", "Electiu"]

data = data1[data1['RESULTAT']=='Acceptat i trasplantat']
data = data[data['HOSPI TX']!='ONT']

mapping = {"Urg 0": 0, "Urg 1": 1, "Electiu": 2}
data['CODE'] = data['URGENCIA'].map(mapping)
resp_filter3= st.sidebar.multiselect("Selecciona el tipus de donant", options=['ME', 'DAC'], default=['ME', 'DAC'])
data = data[data['TIPUS'].isin(resp_filter3)]
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPI TX:N', title='Hospital trasplantador', axis=alt.Axis(labelAngle=0), 
            scale=alt.Scale(domain=['BLLV', 'HCP', 'SANT PAU', 'VHMI'])),
    y=alt.Y('count():Q', scale=alt.Scale(domain=[0,22])),
    color=alt.Color('URGENCIA:N', scale=color_urg, title='Categoria'), 
    order = "CODE:Q",
    tooltip = [alt.Tooltip('HOSPI TX:N', title='Hospital trasplantador'), alt.Tooltip('count():Q', title='Valor'), alt.Tooltip('URGENCIA:N', title='Urgència oferta')],
).properties(width=800, height=600)

text = alt.Chart(data).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('HOSPI TX:N'),
    y = alt.Y('count():Q'),
    text=alt.Text('count():Q', format='.0f'),
    color = alt.value("black"),
)

final = (chart + text).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)


st.altair_chart(final)
