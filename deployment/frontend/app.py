import streamlit as st
from features import predict, captcha

navigation = st.sidebar.selectbox(
    label='Pilih Halaman', options=('Predict', 'Captcha'))

if navigation == 'Predict':
    predict.run()
elif navigation == 'Captcha':
    captcha.run()