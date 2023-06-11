[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/adonath/scipy-2023-pydantic-tutorial/HEAD)

# Building better data structures, APIs and configuration systems for scientific software using Pydantic

This tutorial is an introduction to [Pydantic](https://pydantic.dev), a library for data validation and settings management using Python type annotations. Using a semi-realistic ML and / or scientific software pipeline scenario we demonstrate how Pydantic can be used to support type validations for scientific data structures, APIs and configuration systems. We show how the use of Pydantic in scientific and ML software leads to a more pleasant user experience as well as more robust and easier to maintain code. A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required.

## Setup instructions

Participants will clone the https://github.com/adonath/scipy-2023-pydantic-tutorial repository. They should have a working Python >=3.9 installation of their choice. In the repository we will provide a “requirements.txt” file such that participants can create a self contained environment for the tutorial:

```bash
python -m venv scipy-2023-pydantic-tutorial
./scipy-2023-pydantic-tutorial/bin/activate
python -m pip install -r requirements.txt
```

We will also provide an “environment.yaml” file for people who prefer to use conda or mamba:

```bash
conda env create -f environment.yaml
```

For each section outlined above we will provide jupyter notebooks for demonstration as well as exercises. We will also setup an instance of Binder as a “fall back” solution. However local execution is preferred.

**Prerequisites**: A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required. Some minimal knowledge of Pandas and Numpy for the hands-on exercises.

**Prior Python Programming Level of Knowledge Expected**: Advanced beginners

## Overview
We will cover the following chapters:

#. [Introduction and Installation](notebooks/1-introduction-and-installation.ipynb)
#. [Basic Usage](notebooks/2-basic-usage.ipynb)
#. [Advanced Usage](notebooks/3-advanced-usage.ipynb)
#. [Serialisation and Deserialisation](notebooks/4-serialisation-and-deserialisation.ipynb)
#. [Summary and Conclusion](notebooks/5-summary-and-conclusion.ipynb)

Here is a more complete [overview](overview.md).

