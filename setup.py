from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("setup_requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-therapy-assistant",
    version="1.0.0",
    author="AI Therapy Assistant Team",
    author_email="support@aitherapy.com",
    description="A comprehensive multi-modal therapy chatbot with emotional support features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-therapy-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai-therapy=app:main",
        ],
    },
    keywords="therapy, ai, chatbot, mental health, emotional support, streamlit",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-therapy-assistant/issues",
        "Source": "https://github.com/yourusername/ai-therapy-assistant",
        "Documentation": "https://github.com/yourusername/ai-therapy-assistant/blob/main/README.md",
    },
)