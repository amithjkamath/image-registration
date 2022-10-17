"""
Inspired by https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/
"""

import cv2
import streamlit as st
import numpy as np
from PIL import Image

# Check if 'key' already exists in session_state
# If not, then initialize it
if 'random_b' not in st.session_state:
    st.session_state['random_b'] = 0.5
if 'random_d' not in st.session_state:
    st.session_state['random_d'] = 0.5


def main_loop():
    st.title("Image Registration Demo")
    st.subheader(
        "This app allows you to play with parameters of the transformation matrix!")
    st.text("Change the values in the sidebar to modify the parameters of the transformation matrix")
    st.text(
        " and try to make the 'Registered' image be as close to the original as possible.")

    a = st.sidebar.number_input(
        "a", key="a", min_value=0.0, max_value=5.0, value=1.0, step=0.25)
    b = st.sidebar.number_input(
        "b", key="b", min_value=-5.0, max_value=5.0, value=0.0, step=0.25)
    c = st.sidebar.number_input(
        "c", key="c", min_value=-50.0, max_value=50.0, value=0.0, step=5.0)
    d = st.sidebar.number_input(
        "d", key="d", min_value=-5.0, max_value=5.0, value=0.0, step=0.25)
    e = st.sidebar.number_input(
        "e", key="e", min_value=0.0, max_value=5.0, value=1.0, step=0.25)
    f = st.sidebar.number_input(
        "f", key="f", min_value=-50.0, max_value=50.0, value=0.0, step=5.0)

    original_image = Image.open("rawimage.png")
    original_image = np.array(original_image)

    st.text(
        "Click on 'Randomize Transformation' to randomize the transform to estimate!")
    if st.button('Randomize Transformation'):
        random_b = np.random.random_sample() * 2.0
        st.session_state.random_b = random_b
        random_d = np.random.random_sample() * 2.0
        st.session_state.random_d = random_d

        test_tform = np.float32([[1.0, random_b, 20.0],
                                 [random_d, 1.0, -20.0],
                                 [0.0, 0.0, 1.0]])
    else:
        test_tform = np.float32(
            [[1.0, st.session_state.random_b, 20.0],
             [st.session_state.random_d, 1.0, -20.0],
             [0.0, 0.0, 1.0]])

    deformed_image = cv2.warpPerspective(
        original_image, test_tform, (768, 768), flags=cv2.INTER_LINEAR)
    tform = np.float32([[a, b, c], [d, e, f], [0.0, 0.0, 1.0]])

    registered_image = cv2.warpPerspective(
        deformed_image, tform, (768, 768), flags=cv2.INTER_LINEAR)

    st.text("The tranformation matrix is defined as: ")
    st.text("\t a, b, c")
    st.text("\t d, e, f")
    st.text("\t 0, 0, 1")
    st.text("and the default values are the identity matrix.")

    st.text("Original Image vs. Deformed Image")
    st.image([original_image, deformed_image], width=200)

    st.text("Original Image vs. Registered Image")
    st.image([original_image, registered_image], width=200)

    st.text("The tranformation matrix you've created is: ")
    st.text("\t" + f'{a:8.3f}' + ", " + f'{b:8.3f}' + ", " + f'{c:8.3f}')
    st.text("\t" + f'{d:8.3f}' + ", " + f'{e:8.3f}' + ", " + f'{f:8.3f}')
    st.text("\t" + f'{0:8.3f}' + ", " + f'{0:8.3f}' + ", " + f'{1:8.3f}')

    st.text("Click the 'Reveal Transform' button to find out the right answer:")
    if st.button('Reveal Transform'):
        st.text("The tranformation matrix to use is: ")
        inv_tform = np.linalg.inv(test_tform)
        st.text("\t" + f'{inv_tform[0][0]:8.3f}' + ", " +
                f'{inv_tform[0][1]:8.3f}' + ", " + f'{inv_tform[0][2]:8.3f}')
        st.text("\t" + f'{inv_tform[1][0]:8.3f}' + ", " +
                f'{inv_tform[1][1]:8.3f}' + ", " + f'{inv_tform[1][2]:8.3f}')
        st.text("\t" + f'{inv_tform[2][0]:8.3f}' + ", " +
                f'{inv_tform[2][1]:8.3f}' + ", " + f'{inv_tform[2][2]:8.3f}')


if __name__ == '__main__':
    main_loop()
