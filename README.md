# Building better data structures, APIs and configuration systems for scientific software using Pydantic

Presented by **Axel Donath** and **Nick Langellier**

This tutorial is an introduction to [Pydantic](https://pydantic.dev), a library for data validation and settings management using Python type annotations. Using a semi-realistic ML and / or scientific software pipeline scenario we demonstrate how Pydantic can be used to support type validations for scientific data structures, APIs and configuration systems. We show how the use of Pydantic in scientific and ML software leads to a more pleasant user experience as well as more robust and easier to maintain code. A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required.

**Prerequisites**: A minimum knowledge of Python type annotations, class definitions and data structures will be helpful for beginners but not required. Some minimal knowledge of Pandas and Numpy for the hands-on exercises and Jupyter notebooks.

**Prior Python Programming Level of Knowledge Expected**: Advanced beginners


## Setup instructions

To execute the notebooks and examples from this tutorial, you are expected to have a working Python >=3.9 installation of your choice and `git` installed. First clone this repository:

```bash
git clone https://github.com/adonath/scipy-2023-pydantic-tutorial

```
:warning: **Note:** If you have cloned the repository before July 10, 2023, please make sure to update it to the latest version following the [instructions below](#updating-the-repository).


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

```
******************************************************************
* Congratulations! You are ready to begin the Pydantic tutorial! *
******************************************************************
```
To execute the notebooks along with the presentation, start the Jupyter server:

```bash
jupyter notebook
```

### Updating the repository

If you have cloned the repository before July 10, 2023, please make sure to update it to the latest version.
In case you have local changes, we would recommend to store those in a separate branch before updating the repository. To do so, change to the cloned folder and execute the following commands:

```bash
git checkout -b my-local-changes
git add .
git commit -m "My local changes"
```

Then you can update the repository using:

```bash
git checkout main
git pull origin main
```

Now you should have the latest version of the repository.


## Binder 
If you do not have a working installation (for whatever reason) before the tutorial starts, you can also execute the tutorial in the browser using Binder. Just click on the following badge to start the Binder service:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/adonath/scipy-2023-pydantic-tutorial/HEAD)

This will open a new tab with a clone of the repository and a running instance of [Jupyter Lab](https://jupyter.org) in your browser. The loading of the environment might take some time.

**Important:** The Binder service might not work reliably if a large number of participants is using it the same time. Installing and executing the tutorials locally is the preferred option. 


## Content Overview
We will cover the following chapters:

  1. [Introduction and Installation](notebooks/1-introduction-and-refreshers.ipynb)
  1. [Basic Usage](notebooks/2-basic-usage.ipynb)
  1. [Advanced Usage I](notebooks/3-advanced-usage-part-I.ipynb)
  1. [Advanced Usage II](notebooks/3-advanced-usage-part-II.ipynb)
  1. [Serialisation and Deserialisation](notebooks/4-serialisation-and-deserialisation.ipynb)
  1. [Summary and Conclusion](notebooks/5-summary-and-conclusion.ipynb)

Here is a more complete [overview](overview.md).

You can find the rendered notebooks and smaple solutions to the exercises on the [GitHub pages](https://adonath.github.io/scipy-2023-pydantic-tutorial/) of this repository.

