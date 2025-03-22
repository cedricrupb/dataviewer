
import streamlit as st
import random
from datasets import load_dataset

# Cache the dataset loading
@st.cache_resource
def get_dataset():
    return load_dataset("mnist")

# Get the dataset
dataset = get_dataset()
split = "train"
data = dataset[split]

# Session state for index tracking
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Navigation controls
st.title("Dataset Viewer: mnist")

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    if st.button("⬅️ Previous"):
        st.session_state.current_index = (st.session_state.current_index - 1) % len(data)

with col2:
    if st.button("Random 🎲"):
        st.session_state.current_index = random.randint(0, len(data) - 1)

with col3:
    if st.button("Next ➡️"):
        st.session_state.current_index = (st.session_state.current_index + 1) % len(data)

with col4:
    st.session_state.current_index = st.number_input(
        "Go to index", 
        min_value=0, 
        max_value=len(data) - 1, 
        value=st.session_state.current_index
    )

st.write(f"Showing instance {st.session_state.current_index} of {len(data) - 1}")

# Get current instance
instance = data[st.session_state.current_index]

import streamlit as st
from PIL import Image
import numpy as np

def display_instance(instance):
    """
    Display an instance from the dataset with image and label.
    
    Parameters:
    instance (dict): A dictionary containing 'image' (PIL Image) and 'label' (int)
    """
    st.header("Instance Visualization")
    
    # Create two columns for layout
    col1, col2 = st.columns([3, 1])
    
    # Display the image in the first column
    with col1:
        st.subheader("Image")
        if instance["image"] is not None:
            st.image(instance["image"], width=200)#, use_container_width=True)
        else:
            st.warning("No image available for this instance.")
    
    # Display the label in the second column
    with col2:
        st.subheader("Label Information")
        st.metric("Class Label", instance["label"])
        
        # Optional: You could add more information about the label here
        # For example, if you have a mapping of label to class name
        # label_names = {0: "Cat", 1: "Dog", ...}
        # st.write(f"Class Name: {label_names.get(instance['label'], 'Unknown')}")
    
    # Additional information section
    st.subheader("Additional Details")
    
    # Image properties
    if instance["image"] is not None:
        img_width, img_height = instance["image"].size
        st.write(f"Image Dimensions: {img_width} × {img_height} pixels")
        st.write(f"Image Format: {instance['image'].format}")
        st.write(f"Image Mode: {instance['image'].mode}")
    
    # You could add more visualizations here if needed
    # For example, a histogram of pixel values
    if instance["image"] is not None and hasattr(instance["image"], "histogram"):
        st.subheader("Image Histogram")
        hist_data = instance["image"].histogram()
        st.bar_chart(hist_data)

# The function will be called with the current instance at the end of the script.
# This part would be handled by the calling code, but we include a placeholder
# for demonstration purposes:
# display_instance(current_instance)

# Always call display_instance with current instance
display_instance(instance)
