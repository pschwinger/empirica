#!/usr/bin/env python3
"""
Setup script for Semantic Self-Aware Kit
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="semantic-self-aware-kit",
    version="1.0.0",
    author="Nubaeon",
    description="A comprehensive AI framework for building self-aware, collaborative AI systems with semantic reasoning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nubaeon/semantic-self-aware-kit",
    project_urls={
        "Bug Tracker": "https://github.com/Nubaeon/semantic-self-aware-kit/issues",
        "Documentation": "https://github.com/Nubaeon/semantic-self-aware-kit/tree/main/web",
        "Source Code": "https://github.com/Nubaeon/semantic-self-aware-kit",
        "Discord": "https://discord.gg/collaborative-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research", 
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
        "web": [
            "flask>=2.0",
            "jinja2>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "semantic-kit=semantic_self_aware_kit.cli:main",
            "bootstrap-kit=semantic_self_aware_kit.bootstrap:main",
            "empirica=semantic_self_aware_kit.cli:main",  # Alias for empirica
        ],
    },
    include_package_data=True,
    package_data={
        "semantic_self_aware_kit": ["config/*.json", "config/*.yaml"],
    },
    keywords=[
        "ai", "artificial-intelligence", "semantic", "self-aware", 
        "uncertainty", "collaboration", "metacognitive", "empirical",
        "consciousness", "reasoning", "framework", "empirica"
    ],
)
