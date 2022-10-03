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
    st.text("Change the values in the sidebar to modify the parameters of the transformation matrix")
    st.text(" and try to make the 'Registered' image be as close to the original as possible.")

    a = st.sidebar.number_input("a", key="a", min_value=0.0, max_value=5.0, value=1.0, step=0.25)
    b = st.sidebar.number_input("b", key="b", min_value=-5.0, max_value=5.0, value=0.0, step=0.25)
    c = st.sidebar.number_input("c", key="c", min_value=-50.0, max_value=50.0, value=0.0, step=5.0)
    d = st.sidebar.number_input("d", key="d", min_value=-5.0, max_value=5.0, value=0.0, step=0.25)
    e = st.sidebar.number_input("e", key="e", min_value=0.0, max_value=5.0, value=1.0, step=0.25)
    f = st.sidebar.number_input("f", key="f", min_value=-50.0, max_value=50.0, value=0.0, step=5.0)

    original_image = Image.open("rawimage.png")
    original_image = np.array(original_image)

    test_tform = np.float32([[1.0, 0.5, 20.0], [0.0, 2.0, -20.0], [0.0, 0.0, 1.0]])
    deformed_image = cv2.warpPerspective(original_image, test_tform, (768, 768), flags=cv2.INTER_LINEAR)
    tform = np.float32([[a, b, c], [d, e, f], [0.0, 0.0, 1.0]])

    registered_image = cv2.warpPerspective(deformed_image, tform, (768, 768), flags=cv2.INTER_LINEAR)

    st.text("The tranformation matrix is defined as: ")
    st.text("\t a, b, c")
    st.text("\t d, e, f")
    st.text("\t 0, 0, 1")
    st.text("and the default values are the identity matrix.")

    st.text("Original Image vs. Deformed Image")
    st.image([original_image, deformed_image], width=200)

    st.text("Original Image vs. Registered Image")
    st.image([original_image, registered_image], width=200)


if __name__ == '__main__':
    main_loop()
