import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
import yaml
from yaml.loader import SafeLoader

with open('/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


from util import classify, set_background

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')



    set_background('./bgrd/bg.jpg')

    # set title
    st.title('Casting Quality Control')

    # set header
    st.header('Please upload a Casting Product Image')

    # upload file
    file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])


    # load classifier
    model = load_model('./modelcast.h5')

    # load class names
    with open('./model/label.txt', 'r') as f:
        class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
        f.close()


    # display image
    if file is not None:
        image = Image.open(file).convert('RGB')
        st.image(image, use_column_width=True)

        # classify image
        class_name, conf_score = classify(image, model, class_names)

        # write classification
        st.write("## {}".format(class_name))
        st.write("### score: {}%".format(int(conf_score * 1000) / 10))
