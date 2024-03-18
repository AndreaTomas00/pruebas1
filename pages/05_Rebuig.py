import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Motius rebuig",
    layout = "wide"
)
make_sidebar()
st.sidebar.markdown("# Motius rebuig ")
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

filter_hospi = st.sidebar.multiselect("Selecciona hospital", options = ['BLLV', 'HCP', 'SANT PAU', 'VHMI'], default=['BLLV', 'HCP', 'SANT PAU', 'VHMI'])
resp_filter = st.sidebar.multiselect("Selecciona tipus d'oferta", options=['No acceptat i no trasplantat', 'No acceptat i trasplantat',], default=['No acceptat i no trasplantat', 'No acceptat i trasplantat'])
resp_filter2 = st.sidebar.multiselect("Selecciona Urgència oferta", options=['Urg 0', 'Urg 1', 'Electiu'], default=['Urg 0', 'Urg 1', 'Electiu'] )

st.write("# Motius rebuig")

cols = st.columns([2, 1, 2])
data1 = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")



data = data1[data1['RESULTAT'].isin(resp_filter)]
data = data[data['URGENCIA'].isin(resp_filter2)]
data = data[data['HOSPI TX'].isin(filter_hospi)]
data = data[data['HOSPI TX']!='ONT']

color_scale = alt.Scale(domain=['Alteració analítica','Alteració ecocardio/cateterisme', 'Altres causes', 'Antecedents', 'Crossmatch positiu', 'Diferència de talla/pes amb el receptor', 
                                'Edat del donant', 'Manca de proves (coronariografia)', 'Manca de receptor compatible', 'No disponibilitat logística', 'Problemes amb el candidat a receptor',  'Temps d\'isquèmia/Distància', 
                                'Un altre equip accepta abans'], range =[  # blue
    '#d53e4f',  # orange
    '#f46d43',  # green
    '#fdae61',  # red
    '#fee08b',  # purple # brown
    '#e0ee97',  # pink
    '#b4deae',  # gray
    '#66c2a5', 
    '#3288bd',
     '#5e4fa2' # olive
])

chart = alt.Chart(data).mark_bar().encode(
    y=alt.Y('MOTIU REBUIG:N', title="",  scale=alt.Scale(domain=['Alteració analítica','Alteració ecocardio/cateterisme', 'Altres causes', 'Antecedents', 'Crossmatch positiu', 'Diferència de talla/pes amb el receptor', 
                                'Edat del donant', 'Manca de proves (coronariografia)', 'Manca de receptor compatible', 'No disponibilitat logística', 'Problemes amb el candidat a receptor',  'Temps d\'isquèmia/Distància', 
                                'Un altre equip accepta abans']), axis=alt.Axis(labelAngle=0)),
    x=alt.X('count():Q', title='Acumulatiu', scale=alt.Scale(domain=[0,40])),
    color=alt.Color('MOTIU REBUIG:N', title='Categoria', legend=None,
                    scale=color_scale)
).properties(
    width=900,
    height=600,
)


text = alt.Chart(data).mark_text(align='center', baseline='middle', dx=13, fontSize=20).encode(
    y=alt.Y('MOTIU REBUIG:N'),
    x = alt.X('count():Q'),
    text=alt.Text('count():Q', format='.0f'),
    color = alt.value("black"),
)


final = ((chart+text)).configure_axis(
    labelFontSize=18,
    titleFontSize=20,
    labelLimit=1000
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)

st.altair_chart(final)
data = data.set_index('UCIO')
st.write(data[[ 'DATA', 'TIPUS', 'HOSPI TX', 'URGENCIA', 'MOTIU REBUIG', 'RESULTAT']])
# st.write('#')
# st.write('#')

# st.altair_chart(line)
