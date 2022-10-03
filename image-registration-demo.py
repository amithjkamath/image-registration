"""
Inspired by https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/
"""

import cv2
import streamlit as st
import numpy as np
from PIL import Image


def main_loop():
    st.title("Image Registration Demo")
    st.subheader("This app allows you to play with parameters of the transformation matrix!")
    st.text("Use the sliders in the sidebar to modify the parameters of the transformation matrix")
    st.text(" and try to make the 'Registered' image to be as close to the original as possible.")

    a = st.sidebar.slider("a", min_value=0.0, max_value=5.0, value=1.0)
    b = st.sidebar.slider("b", min_value=-1.0, max_value=1.0, value=0.0)
    c = st.sidebar.slider("c", min_value=-20.0, max_value=20.0, value=0.0)
    d = st.sidebar.slider("d", min_value=-1.0, max_value=1.0, value=0.0)
    e = st.sidebar.slider("e", min_value=0.0, max_value=5.0, value=1.0)
    f = st.sidebar.slider("f", min_value=-20.0, max_value=20.0, value=0.0)
    #g = st.sidebar.slider("g", min_value=-1.0, max_value=1.0, value=0.0)
    #h = st.sidebar.slider("h", min_value=-1.0, max_value=1.0, value=0.0)

    #image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
    #if not image_file:
    #    return None

    original_image = Image.open("rawimage.png")
    original_image = np.array(original_image)

    test_tform = np.float32([[1.0, 0.5, 5.0], [0.0, 2.0, -5.0], [0.0, 0.0, 1.0]])
    deformed_image = cv2.warpPerspective(original_image, test_tform, (512, 512), flags=cv2.INTER_LINEAR)
    tform = np.float32([[a, b, c], [d, e, f], [0.0, 0.0, 1.0]])

    registered_image = cv2.warpPerspective(deformed_image, tform, (512, 512), flags=cv2.INTER_LINEAR)

    st.text("Original Image vs. Deformed Image")
    st.image([original_image, deformed_image], width=200)

    st.text("Original Image vs. Registered Image")
    st.image([original_image, registered_image], width=200)


if __name__ == '__main__':
    main_loop()
