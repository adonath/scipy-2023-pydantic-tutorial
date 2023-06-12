# Building better data structures, APIs and configuration systems for scientific software using Pydantic

This tutorial is an introduction to [Pydantic](https://pydantic.dev), a library for data validation and settings management using Python type annotations. Using a semi-realistic ML and / or scientific software pipeline scenario we demonstrate how Pydantic can be used to support type validations for scientific data structures, APIs and configuration systems. We show how the use of Pydantic in scientific and ML software leads to a more pleasant user experience as well as more robust and easier to maintain code. A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required.

**Prerequisites**: A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required. Some minimal knowledge of Pandas and Numpy for the hands-on exercises and Jupyter notebooks.

**Prior Python Programming Level of Knowledge Expected**: Advanced beginners


## Setup instructions

To execute the notebooks and examples from this tutorial, you are expected to have a working Python >=3.9 installation of your choice and `git` installed. First clone this repository:

```bash
git clone https://github.com/adonath/scipy-2023-pydantic-tutorial
```
And change to the cloned folder:

```bash
cd scipy-2023-pydantic-tutorial
```
We recommend to use a virtual environment to install the required dependencies for this tutorial. For this we provide two options:

- **System Python:** If you use a normal system Python installation you can create and activate the environment using:
  
  ```bash
  python -m venv scipy-2023-pydantic-tutorial
  ./scipy-2023-pydantic-tutorial/bin/activate
  python -m pip install -r requirements.txt
  ```

- **Conda / Mamba:** If you prefer to use a package manager such as [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) or [mamba](https://mamba.readthedocs.io/en/latest/installation.html) we also provide an `environment.yaml` file. In this case you can create and activate the environment using:

  ```bash
  conda env create -f environment.yaml
  conda activate scipy-2023-pydantic-tutorial
  ```

Once the environment is created and activated execute the following script to check your setup:

```bash
python check-setup.py
```

If everything is installed correctly you should see the following message:

```bash
******************************************************************
* Congratulations! You are ready to begin the Pydantic tutorial! *
******************************************************************
```
To execute the notebooks along with the presentation, start the Jupyter server:

```bash
jupyter notebook
```

## Binder 
If you don not have a working installation (for whatever reason) until the tutorial starts, you can also execute the tutorial in the browser using Binder.
Just click on the following badge to start the Binder service:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/adonath/scipy-2023-pydantic-tutorial/HEAD)

This will open a new tab with a clone of the repository and a running instance of [Jupyter Lab](https://jupyter.org) in your browser. The loading of the environment might take some time.

**Important:** The Binder service might not work reliably if a large number of participants is using it the same time. Installing and executing the tutorials locally is the preferred option. 


## Content Overview
We will cover the following chapters:

  1. [Introduction and Installation](notebooks/1-introduction-and-installation.ipynb)
  2. [Basic Usage](notebooks/2-basic-usage.ipynb)
  3. [Advanced Usage](notebooks/3-advanced-usage.ipynb)
  4. [Serialisation and Deserialisation](notebooks/4-serialisation-and-deserialisation.ipynb)
  5. [Summary and Conclusion](notebooks/5-summary-and-conclusion.ipynb)

Here is a more complete [overview](overview.md).

