import streamlit as st 



st.set_page_config(page_title='Attendance System',layout='wide')
st.header('Attendance Face Recognition System using Machine Learning')

with st.spinner('Loading Models and Connecting to Redis DB'):
    import face_reco 

st.success('Models Loaded Successfully')
st.success('Redis DB Successfully Connected') 

