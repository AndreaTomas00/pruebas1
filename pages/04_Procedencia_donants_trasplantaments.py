import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar

alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Procedència donants trasplantaments cardíacs",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Procedència donants trasplantaments cardíacs")

data = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")


color_procedencia = alt.Scale(domain=["VHMI", "SANT PAU", "HCP", "BLLV", "POOL", "BALEARS", "ONT"],
                        range=['#FFFC9B', '#FDE767', '#FFD966', '#F3B95F',   '#FF8000',  '#BBD2EC',  '#3E77B6' ]
                        )


# Create a mapping dictionary
mapping = {'POOL': 1, 'BLLV': 2, 'HCP': 3, 'SANT PAU': 4, 'VHMI': 5, 'ONT': 6, 'BALEARS': 7}

# Add a new column to the DataFrame based on the mapping
data['HOSPI_PROCEDENCIA_CODE'] = data['HOSPI PROCEDENCIA'].map(mapping)

data = data[data['RESULTAT']=='Acceptat i trasplantat']

mapping2 = {"Urg 0": 0, "Urg 1": 1, "Electiu": 2}
data['CODE'] = data['URGENCIA'].map(mapping2)

resp_filter2 = st.sidebar.multiselect("Selecciona Urgència oferta", options=['Urg 0', 'Urg 1', 'Electiu'], default=['Urg 0', 'Urg 1', 'Electiu'] )
resp_filter3= st.sidebar.multiselect("Selecciona el tipus de donant", options=['ME', 'DAC'], default=['ME', 'DAC'])

data = data[data['URGENCIA'].isin(resp_filter2)]
data = data[data['TIPUS'].isin(resp_filter3)]

# Create the bar chart
chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPI TX:N', title='Hospital trasplantador', axis=alt.Axis(labelAngle=0), 
            scale=alt.Scale(domain=['BLLV', 'HCP', 'SANT PAU', 'VHMI', 'ONT'])),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('HOSPI PROCEDENCIA:N', scale=color_procedencia, title='Categoria',
                    sort=["SANT PAU", "BLLV", "HCP",  "VHMI", "POOL", "BALEARS", "ONT"]),  
    tooltip=[ alt.Tooltip('HOSPI PROCEDENCIA:N', title='Procedència'), alt.Tooltip('count():Q', title='Valor')],
    order = 'HOSPI_PROCEDENCIA_CODE:Q'
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


final = ((chart+text)).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)

st.altair_chart(final)

color_procedencia2= alt.Scale(domain=["Propi", "Pool OCATT", "ONT"],
                        range=['#F3B95F', '#FDE767', '#6895D2' ]
                        )

# Create a mapping dictionary
mapping2 = {'Propi': 1, 'Pool OCATT': 2, 'ONT': 3}

# Add a new column to the DataFrame based on the mapping
data['CODE2'] = data['PROCEDENCIA'].map(mapping2)

chart2 = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPI TX:N', title='Hospital trasplantador', axis=alt.Axis(labelAngle=0), 
            scale=alt.Scale(domain=['BLLV', 'HCP', 'SANT PAU', 'VHMI', 'ONT'])),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('PROCEDENCIA:N', scale=color_procedencia2, title='Categoria',
                    sort=["Propi", "Pool OCATT", "ONT"]),  
    tooltip=[ alt.Tooltip('PROCEDENCIA:N', title='Procedència'), alt.Tooltip('count():Q', title='Valor')],
    order = 'CODE2:Q'
).properties(
    width=900,
    height=600,
)

st.altair_chart(chart2)

# st.write('#')
# st.write('#')

# st.altair_chart(line)
