import streamlit as st
import streamlit.components.v1 as components
from Constantes import *
from PIL import Image


st.set_page_config(page_title='Mathias Rostagno\'s portfolio' ,layout="wide",page_icon='bar_chart')

st.subheader('Mathias Rostagno - Data Analyst')
st.write(infosperso['Intro'])
Certification = Image.open('data/Certification.png')
st.image(Certification, caption='Professional Certification')

with st.sidebar:
    components.html(embed_component['linkedin'], height=215)

st.sidebar.write('📧: mathias.rostagno@gmail.com')
pdfFile = open('data/Mathias_Rostagno_Resume.PDF', 'rb')
st.sidebar.download_button('download resume', pdfFile, file_name='Mathias_Rostagno_Resume.PDF',mime='pdf')
