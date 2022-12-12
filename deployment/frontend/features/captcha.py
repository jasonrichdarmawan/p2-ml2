import streamlit as st
import requests
from configparser import ConfigParser
from PIL import Image
from io import BytesIO
from base64 import decodebytes
import matplotlib.pyplot as plt

config = ConfigParser()
config.read("./config.ini")

if config['DEFAULT']['prod'] == 'True':
    URL = config['PRODUCTION']['URL']
else:
    URL = config['DEVELOPMENT']['URL']
    
def req(target_uuid):
    r = requests.post(f'{URL}/captcha', json={'target_uuid': target_uuid})
    
    if r.status_code == 200:
        res = r.json()
        
        st.write(f'Prediction: {res["result"]}')

def run():
    st.title("Captcha")
    
    r = requests.get(f'{URL}/captcha')
    
    if r.status_code == 200:
        res = r.json()
        
        st.write(f'Select {res["target"]}')
        
        fig, axes = plt.subplots(6,4, layout="constrained", figsize=(15,15))
        
        for option, ax, index in zip(res['options'], axes.ravel(), range(23)):
            candidate_uuid = option[0]
            image_base64 = option[1]
            image = Image.open(BytesIO(decodebytes(bytes(image_base64, "ascii"))))
            ax.imshow(image)
            ax.set_title(index + 1)
            
        for ax in axes.ravel():
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        
        st.pyplot(fig)
        
        for index, option in enumerate(res['options']):
            candidate_uuid = option[0]
            st.button(label=f'Click image {index + 1}', key=index+1, on_click=req, kwargs={"target_uuid": candidate_uuid})