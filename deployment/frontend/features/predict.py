import streamlit as st
import requests
from PIL import Image
from configparser import ConfigParser
from io import BytesIO
import matplotlib.pyplot as plt

config = ConfigParser()
config.read("./config.ini")

if config['DEFAULT']['prod'] == 'True':
    URL = config['PRODUCTION']['URL']
else:
    URL = config['DEVELOPMENT']['URL']

def run():
    st.title("Image Predictor")
    
    with st.form(key="image_predictor"):
        uploaded_file = st.file_uploader(
            label="Image", accept_multiple_files=False)
        
        submitted = st.form_submit_button(label="Predict")
        
    if submitted:
        if uploaded_file is not None:
            # bytes_data = uploaded_file.getvalue()
        
            files = {'file': uploaded_file}
            post = requests.post(f'{URL}/predict', files=files)
            
            if post.status_code == 200:
                res = post.json()
                
                st.write(f'Prediction {res["prediction"]}')
                
                get = requests.get(f'{URL}/{res["similar"]}')
                
                if get.status_code == 200:
                    fig, axes = plt.subplots(1,2, layout="constrained")
                    for title, image, ax in zip(
                        ["Uploaded", "Similar"],
                        [Image.open(BytesIO(uploaded_file.getvalue())),
                         Image.open(BytesIO(get.content))],
                        axes.ravel()):
                        ax.imshow(image)
                        ax.set_title(title)
                    
                    st.pyplot(fig)