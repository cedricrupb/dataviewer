"""
Core functionality for the dataviewer package.
"""
import streamlit as st
from datasets import load_dataset
import json
import os
import re
from .llm import Claude, GPT4

class DataViewer:
    def __init__(self, llm=None):
        """Initialize DataViewer with a language model.
        
        Args:
            llm: Language model instance (Claude or GPT4)
        """
        self.data = None
        self.dataset_name = None
        self.llm = llm
        self.progress_callback = None
        
    @classmethod
    def from_environment(cls):
        """Create DataViewer instance based on available API keys."""
        if os.getenv('ANTHROPIC_API_KEY'):
            return cls(llm=Claude(os.getenv('ANTHROPIC_API_KEY')))
        elif os.getenv('OPENAI_API_KEY'):
            return cls(llm=GPT4(os.getenv('OPENAI_API_KEY')))
        else:
            raise ValueError(
                "No API keys found. Please set either ANTHROPIC_API_KEY "
                "or OPENAI_API_KEY environment variable."
            )

    def load_dataset(self, dataset_url):
        """Load a dataset from Hugging Face and its README."""
        self.dataset_name = dataset_url
        self.data = load_dataset(dataset_url)
        
        # Try to get dataset card/README
        try:
            from huggingface_hub import hf_hub_download
            from pathlib import Path
            
            # Try to download README.md or dataset_card.md
            try:
                readme_path = hf_hub_download(
                    repo_id=dataset_url,
                    filename="README.md",
                    repo_type="dataset"
                )
            except Exception:
                try:
                    readme_path = hf_hub_download(
                        repo_id=dataset_url,
                        filename="dataset_card.md",
                        repo_type="dataset"
                    )
                except Exception:
                    readme_path = None
            
            if readme_path:
                self.dataset_readme = Path(readme_path).read_text()
            else:
                self.dataset_readme = None
            
        except Exception:
            self.dataset_readme = None

    def _clean_code(self, code):
        """Remove markdown code block markers and clean up the code.
        
        Args:
            code (str): Code potentially containing markdown markers
            
        Returns:
            str: Cleaned code
        """
        # Remove ```python or ``` markers from start and end
        code = code.strip()
        code = re.sub(r'^```\w*\n', '', code)
        code = re.sub(r'\n```$', '', code)
        return code

    def _get_viewer_path(self, split="train"):
        """Get the path for the viewer file.
        
        Args:
            split (str): Dataset split to visualize
            
        Returns:
            str: Path to the viewer file
        """
        return f"view_{self.dataset_name.replace('/', '_')}_{split}.py"

    def set_progress_callback(self, callback):
        """Set a callback to be called when long operations complete."""
        self.progress_callback = callback

    def generate_viewer(self, split="train", extra_prompt="", force=False):
        """Generate and save a Streamlit viewer for the dataset.
        
        Args:
            split (str): Dataset split to visualize
            extra_prompt (str): Additional requirements for the visualization
            force (bool): Whether to force regeneration of existing viewer
            
        Returns:
            str: Path to the viewer file
        """
        if self.data is None:
            raise ValueError("No dataset loaded")
        if self.llm is None:
            raise ValueError("No language model configured")
        
        viewer_path = self._get_viewer_path(split)
        
        # Check if viewer already exists and force is False
        if os.path.exists(viewer_path) and not force:
            print(f"Using existing viewer at {viewer_path}")
            print("Use --force to regenerate the viewer")
            return viewer_path
            
        # Get sample instance and features
        sample = self.data[split][0]
        features = {k: str(type(v)) for k, v in sample.items()}
        
        # Format example instance, handling different data types appropriately
        def format_value(v):
            if isinstance(v, (str, int, float, bool)):
                return str(v)
            elif isinstance(v, (list, tuple)):
                return f"[list with {len(v)} elements]"
            elif isinstance(v, dict):
                return "{dict with keys: " + ", ".join(v.keys()) + "}"
            else:
                return f"[{type(v).__name__}]"
        
        example_instance = {k: format_value(v) for k, v in sample.items()}
        
        # Create base prompt with optional extra requirements and README
        base_prompt = """Generate a Streamlit Python script to visualize instances from a dataset.
        The script must define a function called 'display_instance' that takes a single parameter 'instance' 
        and visualizes it appropriately.
        
        Dataset Information:
        {readme}
        
        The instance has these features and types: {features}
        
        Here's an example instance from the dataset:
        {example}
        
        Requirements:
        - Create a function called 'display_instance(instance)' that handles the visualization
        - Display all fields appropriately (text, images, audio, etc.)
        - Make it visually appealing with proper headers and sections
        - Handle all data types properly
        - Use st.columns where appropriate for layout
        - Don't include any navigation controls (they're handled elsewhere)
        - Do not include markdown code block markers (```)
        - Consider the dataset's purpose and content when designing the visualization
        - Use the example instance as a guide for formatting and layout
        {extra_requirements}
        
        The function will be called with the current instance at the end of the script.
        Only respond with the raw Python code, no explanations."""

        readme_section = (
            f"Dataset README:\n{self.dataset_readme}"
            if self.dataset_readme
            else "No README available for this dataset."
        )

        prompt = base_prompt.format(
            features=json.dumps(features, indent=2),
            readme=readme_section,
            example=json.dumps(example_instance, indent=2),
            extra_requirements=f"\nAdditional requirements:\n{extra_prompt}" if extra_prompt else ""
        )
        
        system_message = """You are a Python expert specializing in Streamlit and data visualization.
        Create visualizations that are appropriate for the dataset's purpose and content.
        Provide only raw Python code without markdown formatting."""
        
        # Generate code using the configured LLM
        viewer_code = self._clean_code(
            self.llm.generate_code(prompt, system_message)
        )
        
        # Signal completion
        if self.progress_callback:
            self.progress_callback()
        
        # Define the viewer template
        viewer_template = """
import streamlit as st
import random
from datasets import load_dataset

# Cache the dataset loading
@st.cache_resource
def get_dataset():
    return load_dataset("{dataset_name}")

# Get the dataset
dataset = get_dataset()
split = "{split}"
data = dataset[split]

# Session state for index tracking
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Navigation controls
st.title("Dataset Viewer: {dataset_name}")

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

st.write(f"Showing instance {{st.session_state.current_index}} of {{len(data) - 1}}")

# Get current instance
instance = data[st.session_state.current_index]

{viewer_code}

# Always call display_instance with current instance
display_instance(instance)
"""
        
        # Save the generated viewer
        with open(viewer_path, "w") as f:
            f.write(viewer_template.format(
                dataset_name=self.dataset_name,
                split=split,
                viewer_code=viewer_code
            ))
        
        return viewer_path
        
    def run_viewer(self, split="train", extra_prompt="", force=False):
        """Generate and run the Streamlit viewer.
        
        Args:
            split (str): Dataset split to visualize
            extra_prompt (str): Additional requirements for the visualization
            force (bool): Whether to force regeneration of existing viewer
        """
        viewer_path = self.generate_viewer(split, extra_prompt=extra_prompt, force=force)
        os.system(f"streamlit run {viewer_path}")

    def display(self):
        """Display the loaded data."""
        if self.data is None:
            raise ValueError("No data loaded")
        return str(self.data) 