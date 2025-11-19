"""
Inspired by https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/
"""

import hmac
import cv2
import streamlit as st
import numpy as np
from datasets import load_dataset

# Check if 'key' already exists in session_state
# If not, then initialize it
if "random_b" not in st.session_state:
    st.session_state["random_b"] = 0.5
if "random_d" not in st.session_state:
    st.session_state["random_d"] = 0.5
if "dataset" not in st.session_state:
    st.session_state["dataset"] = None
if "image_names" not in st.session_state:
    st.session_state["image_names"] = []


@st.cache_resource
def load_image_dataset():
    """Load the dataset from Hugging Face and cache it"""
    try:
        dataset = load_dataset("amithjkamath/exampleimages", split="train")
        return dataset
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None


def main_loop():

    st.title("Image Registration Demo")
    st.subheader(
        "This app allows you to play with parameters of the transformation matrix!"
    )
    st.text(
        "Change the values in the sidebar to modify the parameters of the transformation matrix"
    )
    st.text(
        " and try to make the 'Registered' image be as close to the original as possible."
    )

    # Load dataset
    with st.spinner("Loading images from dataset..."):
        dataset = load_image_dataset()

    if dataset is None:
        st.error("Failed to load dataset. Please try again later.")
        st.stop()

    # Create image selector
    st.sidebar.markdown("---")
    st.sidebar.subheader("Image Selection")

    # Get image indices and create labels
    image_options = [f"Image {i+1}" for i in range(len(dataset))]
    selected_image_idx = st.sidebar.selectbox(
        "Choose an image:", range(len(dataset)), format_func=lambda x: image_options[x]
    )

    # Load the selected image from dataset
    selected_sample = dataset[selected_image_idx]
    original_image = selected_sample["image"]

    # Convert PIL image to numpy array for OpenCV
    original_image = np.array(original_image)

    st.sidebar.markdown("---")

    # Matrix input section in main area
    st.subheader("🔧 Transformation Matrix Editor")
    st.markdown(
        """
    Adjust the transformation matrix below. The matrix transforms the deformed image back to match the original.
    Try to make the 'Registered' image match the 'Original' image as closely as possible!
    """
    )

    # Create a 3-column layout for the matrix
    st.markdown("### Transformation Matrix")

    # Row 1
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input(
            "T[0,0]",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.05,
            key="a",
            help="Scale X-axis",
        )
    with col2:
        b = st.number_input(
            "T[0,1]",
            min_value=-5.0,
            max_value=5.0,
            value=0.0,
            step=0.05,
            key="b",
            help="Shear Y→X",
        )
    with col3:
        c = st.number_input(
            "T[0,2]",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=1.0,
            key="c",
            help="Translate X",
        )

    # Row 2
    col4, col5, col6 = st.columns(3)
    with col4:
        d = st.number_input(
            "T[1,0]",
            min_value=-5.0,
            max_value=5.0,
            value=0.0,
            step=0.05,
            key="d",
            help="Shear X→Y",
        )
    with col5:
        e = st.number_input(
            "T[1,1]",
            min_value=0.0,
            max_value=5.0,
            value=1.0,
            step=0.05,
            key="e",
            help="Scale Y-axis",
        )
    with col6:
        f = st.number_input(
            "T[1,2]",
            min_value=-50.0,
            max_value=50.0,
            value=0.0,
            step=1.0,
            key="f",
            help="Translate Y",
        )

    # Row 3 (fixed values)
    col7, col8, col9 = st.columns(3)
    with col7:
        st.text_input("T[2,0]", value="0.0", disabled=True, key="g")
    with col8:
        st.text_input("T[2,1]", value="0.0", disabled=True, key="h")
    with col9:
        st.text_input("T[2,2]", value="1.0", disabled=True, key="i")

    st.markdown("---")

    st.text(
        "Click on 'Randomize Transformation' to randomize the transform to estimate!"
    )
    if st.button("Randomize Transformation"):
        random_b = np.random.random_sample() * 2.0
        st.session_state.random_b = random_b
        random_d = np.random.random_sample() * 2.0
        st.session_state.random_d = random_d

        test_tform = np.float32(
            [[1.0, random_b, 20.0], [random_d, 1.0, -20.0], [0.0, 0.0, 1.0]]
        )
    else:
        test_tform = np.float32(
            [
                [1.0, st.session_state.random_b, 20.0],
                [st.session_state.random_d, 1.0, -20.0],
                [0.0, 0.0, 1.0],
            ]
        )

    # Get image dimensions for transformation
    img_height, img_width = original_image.shape[:2]

    deformed_image = cv2.warpPerspective(
        original_image, test_tform, (img_width, img_height), flags=cv2.INTER_LINEAR
    )
    tform = np.float32([[a, b, c], [d, e, f], [0.0, 0.0, 1.0]])

    registered_image = cv2.warpPerspective(
        deformed_image, tform, (img_width, img_height), flags=cv2.INTER_LINEAR
    )

    st.markdown("---")

    # Create side-by-side layout for matrix display and image comparison
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # Display the current transformation matrix
        st.markdown("### 📊 Your Current Matrix")
        matrix_display = f"""
        ```
        ┌                           ┉
        │ {a:8.3f}  {b:8.3f}  {c:8.3f} │
        │ {d:8.3f}  {e:8.3f}  {f:8.3f} │
        │ {0:8.3f}  {0:8.3f}  {1:8.3f} │
        └                           ┘
        ```
        """
        st.markdown(matrix_display)

        st.markdown("### 🎯 Solution")
        st.text("Reveal the correct transformation:")
        if st.button("🔍 Reveal Transform", type="primary"):
            st.success("Correct transformation matrix:")
            inv_tform = np.linalg.inv(test_tform)

            solution_matrix = f"""
            ```
            ┌                                        ┉
            │ {inv_tform[0][0]:8.3f}  {inv_tform[0][1]:8.3f}  {inv_tform[0][2]:8.3f} │
            │ {inv_tform[1][0]:8.3f}  {inv_tform[1][1]:8.3f}  {inv_tform[1][2]:8.3f} │
            │ {inv_tform[2][0]:8.3f}  {inv_tform[2][1]:8.3f}  {inv_tform[2][2]:8.3f} │
            └                                        ┘
            ```
            """
            st.markdown(solution_matrix)

    with right_col:
        st.markdown("### 🖼️ Image Comparison")

        st.text("Original vs. Deformed")
        st.image([original_image, deformed_image], width=150)

        st.text("Original vs. Registered")
        st.image([original_image, registered_image], width=150)


if __name__ == "__main__":
    main_loop()
