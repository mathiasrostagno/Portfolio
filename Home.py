# faire un README + requirement.txt
import streamlit as st
import streamlit.components.v1 as components

embed_components = {'linkedin' : """<script src="https://fr.linkedin.com/in/mathias-rostagno-901858a0?trk=profile-badge" async defer type= "text/javascript"></script> 
                    <div class="badge-base LI-profile-badge" data-locale="fr_FR" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="mathias-rostagno-901858a0" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://fr.linkedin.com/in/mathias-rostagno-901858a0?trk=profile-badge">Mathias Rostagno</a></div>
                    """}

st.title('Covid19 Analysis')
st.subheader('Mathias Rostagno - Data Analyst')

body = '##### Hi I am Mathias, a passionate Data analyst from France'
body2 = '##### I am currently developping an Analysis about the world impact of Covid19'


st.caption(body, unsafe_allow_html=True)
st.caption(body2, unsafe_allow_html=True)

with st.sidebar:
    components.html(embed_components['linkedin'], height=310)

