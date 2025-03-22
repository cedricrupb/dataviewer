# Extra prompt: Create an extra button at the top of the page which redirects directly to the PR on Github. Note to obtain the pull request id you have to parse the instance id. The instance id has the following format: user__repo-pullRequestId.

import streamlit as st
import random
from datasets import load_dataset

# Cache the dataset loading
@st.cache_resource
def get_dataset():
    return load_dataset("princeton-nlp/SWE-bench")

# Get the dataset
dataset = get_dataset()
split = "train"
data = dataset[split]

# Session state for index tracking
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Navigation controls
st.title("Dataset Viewer: princeton-nlp/SWE-bench")

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
import re
import datetime

def display_instance(instance):
    # Extract PR information from instance_id
    pr_info = extract_pr_info(instance["instance_id"])
    
    # Create GitHub PR link button at the top
    if pr_info:
        user, repo, pr_id = pr_info
        pr_url = f"https://github.com/{user}/{repo}/pull/{pr_id}"
        st.button(f"View PR #{pr_id} on GitHub", on_click=lambda: st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{pr_url}\'" />', unsafe_allow_html=True))
    
    # Main header
    st.title("Instance Details")
    
    # Repository and instance information
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Repository")
        st.write(instance["repo"])
    with col2:
        st.subheader("Instance ID")
        st.write(instance["instance_id"])
    
    # Commit information
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Base Commit")
        st.code(instance["base_commit"], language="text")
    with col2:
        st.subheader("Environment Setup Commit")
        st.code(instance["environment_setup_commit"], language="text")
    
    # Problem statement
    st.header("Problem Statement")
    st.write(instance["problem_statement"])
    
    # Hints
    if instance.get("hints_text"):
        with st.expander("Hints", expanded=False):
            st.write(instance["hints_text"])
    
    # Patches
    st.header("Patches")
    
    tab1, tab2 = st.tabs(["Main Patch", "Test Patch"])
    
    with tab1:
        st.code(instance["patch"], language="diff")
    
    with tab2:
        st.code(instance["test_patch"], language="diff")
    
    # Test Results
    st.header("Test Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("FAIL → PASS")
        st.write(instance["FAIL_TO_PASS"])
    
    with col2:
        st.subheader("PASS → PASS")
        st.write(instance["PASS_TO_PASS"])
    
    # Metadata
    st.header("Metadata")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Created At")
        try:
            # Try to parse and format the date
            date_obj = datetime.datetime.fromisoformat(instance["created_at"].replace('Z', '+00:00'))
            st.write(date_obj.strftime("%Y-%m-%d %H:%M:%S UTC"))
        except:
            # If parsing fails, show the original string
            st.write(instance["created_at"])
    
    with col2:
        st.subheader("Version")
        st.write(instance["version"])

def extract_pr_info(instance_id):
    """Extract user, repo, and PR ID from instance_id"""
    pattern = r"([^_]+)__([^-]+)-(\d+)"
    match = re.match(pattern, instance_id)
    if match:
        user = match.group(1)
        repo = match.group(2)
        pr_id = match.group(3)
        return user, repo, pr_id
    return None

# The function will be called with the current instance at the end of the script.

# Always call display_instance with current instance
display_instance(instance)
