import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
from util import classify, set_background

# Set background
set_background('./bgrd/bg.jpg')

# Define CSS for the title, header, image name, and text boxes
st.markdown(
    """
    <style>
    .title-box, .header-box, .filename-box, .box {
        border: 1px solid #000;
        padding: 10px;
        border-radius: 5px;
        background-color: #333;
        color: white;
        margin-top: 20px;
    }
    .title-box {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }
    .header-box {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .filename-box {
        text-align: center;
        font-size: 18px;
    }
    .box h2, .box h3 {
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True
)

# Set title
st.markdown('<div class="title-box">Casting Quality Control</div>', unsafe_allow_html=True)

# Set header
st.markdown('<div class="header-box">Please upload a Casting Product Image</div>', unsafe_allow_html=True)

# Upload file
file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

# Load classifier
model = load_model('./modelcast.h5')

# Load class names
with open('./model/label.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]

# Display image and classification results
if file is not None:
    image = Image.open(file).convert('RGB')
    st.image(image, use_column_width=True)
    
    # Display image file name
    st.markdown(f'<div class="filename-box">Uploaded file: {file.name}</div>', unsafe_allow_html=True)

    # Classify image
    class_name, conf_score = classify(image, model, class_names)

    # Write classification in a box
    st.markdown(f"""
    <div class="box">
        <h2>{class_name}</h2>
        <h3>score: {int(conf_score * 1000) / 10}%</h3>
    </div>
    """, unsafe_allow_html=True)
