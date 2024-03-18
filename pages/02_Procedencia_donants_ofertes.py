import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Procedència donants ofertes cardiaques",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Procedència donants ofertes cardiaques")

data = pd.read_csv("cor.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")

color_procedencia = alt.Scale(domain=["VHMI", "SANT PAU", "HCP", "BLLV", "POOL", "BALEARS", "ONT"],
                        range=['#FFFC9B', '#FDE767', '#FFD966', '#F3B95F',   '#FF8000',  '#BBD2EC',  '#3E77B6' ]
                        )


# Create a mapping dictionary
mapping = {'POOL': 1, 'BLLV': 2, 'HCP': 3, 'SANT PAU': 4, 'VHMI': 5, 'ONT': 6, 'BALEARS': 7}

# Add a new column to the DataFrame based on the mapping
data['HOSPI_PROCEDENCIA_CODE'] = data['HOSPI PROCEDENCIA'].map(mapping)
data['MONTH'] = pd.to_datetime(data['DATA'], format='%d/%m/%y').dt.month
mapping2 = {1: 'Gener', 2:'Febrer', 3: 'Març', 4: 'Abril', 5: 'Maig', 6: 'Juny', 7: 'Juliol', 8: 'Agost', 9:'Setembre', 10: 'Octubre', 11:'Novembre', 12:'Desembre'}
data['MES']=data['MONTH'].map(mapping2)

# Create the bar chart
chart_propis = alt.Chart(data).mark_bar().encode(
    x=alt.X('ORGANITZACIO:N', title='Organització de procedència', axis=alt.Axis(labelAngle=0), 
            scale=alt.Scale(domain=['OCATT', 'ONT'])),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('HOSPI PROCEDENCIA:N', scale=color_procedencia, title='Categoria',
                    sort=["SANT PAU", "BLLV", "HCP",  "VHMI", "POOL", "BALEARS", "ONT"]),  # Ensure the sorting is based on the custom order
    tooltip=[alt.Tooltip('HOSPI PROCEDENCIA:N', title='Procedència'), alt.Tooltip('count():Q', title='Valor')],
    order = 'HOSPI_PROCEDENCIA_CODE:Q'
).transform_aggregate(groupby=['UCIO', 'HOSPI PROCEDENCIA', 'ORGANITZACIO', 'HOSPI_PROCEDENCIA_CODE']).properties(
    width=900,
    height=600,
)


text_propis = alt.Chart(data).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('ORGANITZACIO:N'),
    y = alt.Y('count():Q'),
    text=alt.Text('count():Q', format='.0f'),
    color = alt.value("black"),
).transform_aggregate(groupby=['UCIO', 'HOSPI PROCEDENCIA', 'ORGANITZACIO', 'HOSPI_PROCEDENCIA_CODE'])


final_propis = ((chart_propis+text_propis)).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)

st.altair_chart(final_propis)
# st.write('#')
# st.write('#')

# st.altair_chart(line)
