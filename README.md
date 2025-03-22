# DataViewer for HuggingFace Datasets

A Python package for visualizing Hugging Face datasets using AI-generated Streamlit views. The package uses AI (Claude or GPT-4) to automatically generate custom visualization code for any dataset structure.

*:warning: Warning* At the moment, this project is mainly a playground for evaluating the code generation capabilities of recent large language models. Hence, use the implementation with caution.

## Examples
Here, a few examples of Streamlit Apps automatically generated for Huggingface datasets (using Claude 3.7 Sonnet).

### MNIST
![MNSIT Website](https://github.com/cedricrupb/dataviewer/blob/main/examples/mnist.png)

### SWE Bench (princeton-nlp/SWE-bench)

![SWE-Bench Nice](https://github.com/cedricrupb/dataviewer/blob/main/examples/swebench-nice.png)


*NOTE:* Generated with extra prompt: "Create an extra button at the top of the page which redirects directly to the PR on Github. Create an extra button at the top of the page which redirects directly to the PR on Github. Make it as visually appealing as possible. A user should think: 'Wow, this is a nice Streamlit App'." The button is fully functional and shows the original PR on Github.

## Installation

Clone the repository and install locally:

```bash
# Clone the repository
git clone https://github.com/cedricrupb/dataviewer.git
cd dataviewer

# Install in development mode
pip install -e .
```

## Requirements

- Python 3.7+
- One of the following API keys:
  - Anthropic API key (preferred, for Claude)
  - OpenAI API key (for GPT-4)
- Internet connection for accessing Hugging Face datasets

## Usage

### Command Line Interface

First, set your API key as an environment variable:

```bash
# Preferred: Use Claude
export ANTHROPIC_API_KEY='your-api-key'

# Alternative: Use GPT-4
export OPENAI_API_KEY='your-api-key'
```

Basic usage:
```bash
dataviewer mnist
```

Options:
```bash
# View a specific split
dataviewer mnist --split test

# Add custom visualization requirements
dataviewer mnist --prompt "Show images in grayscale and add a histogram of pixel values"

# Force regeneration of cached viewer
dataviewer mnist --force

# Combine options
dataviewer mnist --split test --prompt "Add confidence scores" --force
```

### Python API

```python
from dataviewer import DataViewer

# Initialize with available API key from environment
viewer = DataViewer.from_environment()

# Load a dataset
viewer.load_dataset("mnist")

# Generate and run the viewer
viewer.run_viewer(
    split="train",  # optional: dataset split
    extra_prompt="Show images in grayscale",  # optional: custom requirements
    force=False  # optional: force regeneration
)
```

## Features

- **Automatic Visualization**: Uses AI to generate custom Streamlit views based on dataset structure
- **Multiple AI Models**: Supports both Claude (preferred) and GPT-4
- **Dataset Navigation**: 
  - Previous/Next buttons
  - Random instance selection
  - Direct index input
- **Caching**:
  - Caches generated viewer code for faster startup
  - Force regeneration available when needed
  - Dataset caching for quick navigation
- **Customization**:
  - Custom visualization requirements via prompts
  - Support for different dataset splits
  - Handles various data types (text, images, audio, etc.)
- **User Interface**:
  - Clean and intuitive navigation
  - Progress indicators during generation
  - Informative status messages

## How It Works

1. Loads a dataset from Hugging Face
2. Analyzes the dataset structure
3. Uses AI to generate appropriate visualization code
4. Creates a standalone Streamlit app with:
   - Dataset navigation controls
   - Custom visualization logic
   - Caching for performance
5. Runs the viewer in your browser

## Tips

- The first run for a dataset will take longer as it generates the viewer
- Subsequent runs use the cached viewer unless `--force` is specified
- Use `--prompt` to customize how your data is displayed
- Different splits get their own cached viewers
- The viewer automatically handles dataset reloading and navigation

## Contributing

Contributions are welcome! Feel free to:

- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Suggest new features or enhancements
- Help improve documentation

Please feel free to check out the [Issues](https://github.com/cedricrupb/dataviewer/issues) page to:
- Report bugs
- Suggest new features
- Join ongoing discussions

All contributions, from code to documentation improvements, are appreciated.

## License

This project is licensed under the MIT License - see the LICENSE file for details.