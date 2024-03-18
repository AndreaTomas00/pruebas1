import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
import streamlit as st

alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Ofertes global",
    layout = "wide"
)
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
make_sidebar()

st.write("# Global ofertes cardíaques")

data = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")



#resp_filter = st.multiselect("Selecciona tipus d'oferta", options=['Acceptat i trasplantat', 'Acceptat i no trasplantat', 'No acceptat i no trasplantat', 'No acceptat i trasplantat',
                                # ], default=['Acceptat i trasplantat', 'Acceptat i no trasplantat', 'No acceptat i no trasplantat', 'No acceptat i trasplantat',
                                # ])
resp_filter2 = st.sidebar.multiselect("Selecciona Urgència oferta", options=['Urg 0', 'Urg 1', 'Electiu'], default=['Urg 0', 'Urg 1', 'Electiu'] )
resp_filter3= st.sidebar.multiselect("Selecciona el tipus de donant", options=['ME', 'DAC'], default=['ME', 'DAC'])
#data = data1[data1['RESULTAT'].isin(resp_filter)]
data = data[data['HOSPI TX']!='ONT']

data = data[data['URGENCIA'].isin(resp_filter2)]
data = data[data['TIPUS'].isin(resp_filter3)]
color_scale = alt.Scale(domain=['Acceptat i trasplantat', 'Acceptat i no trasplantat',
                                'No acceptat i no trasplantat', 'No acceptat i trasplantat'],
                        range=['#09AC42', '#A9EAC0',  '#EE8E81', '#AC220F'])

chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPI TX:N', title='Hospital trasplantador', axis=alt.Axis(labelAngle=0), 
            scale=alt.Scale(domain=['BLLV', 'HCP', 'SANT PAU', 'VHMI'])),
    y=alt.Y('count():Q', title='Acumulatiu', scale=alt.Scale(domain=[0,50])),
    color=alt.Color('RESULTAT:N',  title='Categoria',
                    scale=color_scale, sort="ascending"),  # Ensure the sorting is based on the custom order
    tooltip=[alt.Tooltip('HOSPI TX:N', title='Hospital trasplantador'), alt.Tooltip('count():Q', title='Valor'),alt.Tooltip('RESULTAT:N', title='Resposta') ],
).properties(
    width=900,
    height=600,
)

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
