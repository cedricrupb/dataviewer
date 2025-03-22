from setuptools import setup, find_packages

setup(
    name="dataviewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "datasets>=2.15.0",
        "streamlit>=1.30.0",
        "anthropic>=0.8.0",
        "click>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'dataviewer=dataviewer.cli:main',
        ],
    },
    author="Cedric Richter",
    author_email="cedricr.upb@gmail.com",
    description="AI-powered Streamlit viewer for Hugging Face datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cedricrupb/dataviewer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 