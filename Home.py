# faire un README + requirement.txt
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(page_title='Mathias Rostagno\'s portfolio' ,layout="wide",page_icon='bar_chart')

embed_component= {'linkedin': """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="fr_FR" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="mathias-rostagno-901858a0" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://fr.linkedin.com/in/mathias-rostagno-901858a0?trk=profile-badge"></a></div> """}


st.subheader('Mathias Rostagno - Data Analyst')
body = 'Hi I am Mathias, a passionate Data analyst from France and I am currently developping an Analysis about the world impact of Covid19'
st.write(body)


image = Image.open('data/Certification.png')
st.image(image, caption='Professional Certification')

with st.sidebar:
    components.html(embed_component['linkedin'],height=205)
st.sidebar.write('📧: mathias.rostagno@gmail.com')
pdfFile = open('data/Mathias_Rostagno_Resume.pdf', 'rb')
st.sidebar.download_button('download resume',pdfFile,file_name='Mathias_Rostagno_Resume.pdf',mime='pdf')