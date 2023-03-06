# Building better data structures, APIs and configuration systems for scientific software using Pydantic

Proposed Outline:

## I. Introduction (10 min)
 * Common pitfalls of Python dynamic typing, delayed code failure, bad user experiences, and difficult-to-find bugs
 * Explain what Pydantic is and how it can help to solve the problem
 * Give a high level overview of Pydantic's key features and main use in web applications

## II. Installation (5 min)

* Provide step-by-step instructions for installing Pydantic
* Check if Pydantic is installed correctly
* Pydantic v2.0 vs. v1.x. If available we will use Pydantic v2.0

## III. Basic Usage (30 min)

* Refresher on Python type annotations and class definitions
* Creation of a simple Pydantic model
* Initializing models and setting model attributes
* Overview of common “atomic” types, such as float, int, str, bool, etc.
* Type parsing (without validation)
* Default values, optional values and Optional type
* Model Config and Config.extra = “forbid”

### Hands on Exercises (15 min)

## IV. Advanced Usage (45 min)

### IV.a Complex Types

* More complex data types, such as typed lists and dictionaries
* Working with Enums and Union types
* Working with datetime types
* Defining custom data types
* Building hierarchical structures / recursive models
* Defining private attributes via ClassVar, PrivateAttr and Config 

### IV.b Type Validation

* Validators and validation functions
* Pre and post init validation 
* Root validators
* Introduce validate_arguments decorator
* Skip validation and .construct() method
* Config settings related to validation

### IV.c Dynamic Model Definition

* Refresher on builtin Python data structures
* Model creation from NamedTuple, TypedDict or dataclasses
* Dynamic model creation using create_model

### Hands on Exercises (30 - 45 min)

## V. Serialization and Deserialization (30 min)

* Motivate need for serialization and deserialization of Python objects, Why not just pickle?
* Introduce JSON / YAML formats, also mention TOML
* Serialize Pydantic model to and from JSON / YAML
* Introduce .dict() and .json()
* Implementing JSON encoders for custom types
* Fields and extending schema definitions
* Config of serialization, excluding and including fields 
* Performance remarks for serialization

### Hands on Exercises (30 min)

## BREAK (10 min)

## VI. Best Practices (15 min)

* Mention Pycharm, VSCode, MyPy plugins etc.
* Show best practices for using Pydantic in projects
* List common mistakes and pitfalls

## VII. Conclusion and Q&A(15 min)

* Summarize of key takeaways from the tutorial
* List additional resources for learning Pydantic

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
