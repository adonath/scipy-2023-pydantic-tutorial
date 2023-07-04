# 2. Basic Usage

**Concepts:**
* Creation of a simple Pydantic model
* Initializing models and setting model attributes
* Type parsing
* Atomic types
* Type validation (sneak peak)
* Default values and optional values
* Model Config and Config.extra = “forbid”

For comparison we fisrt start with the simple class definitons we saw in the introduction:


```python
class PointV1:
    """Representation of a two-dimensional point coordinate."""

    def __init__(self, x, y):
        """Initializes a PointV1 with the given coordinates."""
        self.x = x
        self.y = y

    def distance_to(self, other):
        """Computes the distance to another `PointV1`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5
```

And the version with type annotations:


```python
class PointV2:
    """Representation of a two-dimensional point coordinate."""

    def __init__(self, x: float, y: float) -> None:
        """Initializes a PointV2 with the given coordinates."""
        self.x = x
        self.y = y

    def distance_to(self, other: "PointV2") -> float:
        """Computes the distance to another `PointV2`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5
```


## Pydantic models

Now that we've reviewed type hints and class defintions, let's convert the above example to a Pydantic model. This will involve only a few changes and will noticeably improve the code readability even further...


```python
from pydantic import BaseModel


class PointV3(BaseModel):
    """Representation of a two-dimensional point coordinate."""

    x: float
    y: float

    def distance_to(self, other: "PointV3") -> float:
        """Computes the distance to another `PointV3`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5


p2 = PointV3(x=-1, y=4)
display(p2)
```


    PointV3(x=-1.0, y=4.0)


That's it! We only need to import `BaseModel` from Pydantic, use it as the parent class of `PointV3`, and list the instance attributes (with their type hints) as if they were class attributes. Pydantic automatically creates an `__init__` method for us using the provided class attributes and their type hints. Notice, Pydantic also provides a `__repr__` method that prints out a nice representation of `p2`.

After instantiation of a Pydantic model, the instance will, under most circumstances, behave as a normal Python class. For example we can update attributes after instantiation, just as with a normal Python class...


```python
p2 = PointV3(x=-1, y=4)
display(p2)

p2.y = 0
display(p2)
```


    PointV3(x=-1.0, y=4.0)



    PointV3(x=-1.0, y=0)


## Type parsing

Recall the bug we had earlier when trying to instantiate a `PointV1` with stringified integers. With Pydantic, this is no longer a bug! If the input arguments `x` and `y` are not of the expected type, Pydantic uses the argument type hints to attempt to coerce the input arguments into the expected types. Let's see this in action


```python
x1, y1, x2, y2 = "5", "7", -1, 4

p1_v1 = PointV1(x=x1, y=y1)
p2_v1 = PointV1(x=x2, y=y2)

p1_v3 = PointV3(x=x1, y=y1)
p2_v3 = PointV3(x=x2, y=y2)

for point in [p1_v1, p2_v1, p1_v3, p2_v3]:
    print("\n", repr(point))
    print(f"{point.x = } and {type(point.x) = }")
    print(f"{point.y = } and {type(point.y) = }")
```

    
     <__main__.PointV1 object at 0x7f54c49532e0>
    point.x = '5' and type(point.x) = <class 'str'>
    point.y = '7' and type(point.y) = <class 'str'>
    
     <__main__.PointV1 object at 0x7f54c4953070>
    point.x = -1 and type(point.x) = <class 'int'>
    point.y = 4 and type(point.y) = <class 'int'>
    
     PointV3(x=5.0, y=7.0)
    point.x = 5.0 and type(point.x) = <class 'float'>
    point.y = 7.0 and type(point.y) = <class 'float'>
    
     PointV3(x=-1.0, y=4.0)
    point.x = -1.0 and type(point.x) = <class 'float'>
    point.y = 4.0 and type(point.y) = <class 'float'>


Notice that for `PointV1` (which is not a Pydantic model), the `x` and `y` attributes are exactly as provided, i.e. strings and integers. But for `PointV3` (which is a Pydantic model), the `x` and `y` attributes were converted to floats because they were type hinted as such. Pydantic applied the `float` constructor to the provided values i.e. `float("5") == 5.0`, `float("7") == 7.0`, `float(-1) == -1.0`, and `float(4) == 4.0`. Later, we will discuss the case when this conversion is not possible e.g. `float("hello world")`.

Note: `PointV1` and `PointV2` only differ in type hints and have no run-time difference. We would have obtained the same results with `PointV2` as we did with `PointV1`. Try it!

We can further elucidate this point by attempting to compute the distances between the points for each version:


```python
p1_v1.distance_to(p2_v1)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[6], line 1
    ----> 1 p1_v1.distance_to(p2_v1)


    Cell In[1], line 11, in PointV1.distance_to(self, other)
          9 def distance_to(self, other):
         10     """Computes the distance to another `PointV1`."""
    ---> 11     dx = self.x - other.x
         12     dy = self.y - other.y
         13     return (dx**2 + dy**2) ** 0.5


    TypeError: unsupported operand type(s) for -: 'str' and 'int'


Without Pydantic we get the expected error, but with Pydantic...


```python
p1_v3.distance_to(p2_v3)
```




    6.708203932499369



we obtain the distance between the two points! This is thanks to Pydantic's type parsing.

## Atomic types

From this point on, I will refer to Pydantic model attributes as fields, as is done in the Pydantic documentation.

Pydantic supports a large variety of field types but the most basic are `None`, `bool`, `int`, `float`, `str` and `bytes`.

### `None`

The only allowed value is `None`.

### `bool`

The allowed values for `True` are `{True, 1, "1", "on", "t", "true", "y", "yes"}`. The allowed values for `False` are `{False, 0, "0", "off", "f", "false", "n", "no"}`.

### `int`

`int(v)` will be used to coerce values to the `int` type. WARNING: This can lead to a loss of information. If `x` is type hinted as `int` and the provided value is `2.72`, the resulting value of `x` will be `2` because `int(2.72) == 2`.

### `float`

`float(v)` will be used to coerce values to the `float` type.

### `str`

`str(v)` will be used to coerce numeric types and `v.decode()` will be used to coerce `bytes` and `bytearray`.

### `bytes`

`bytes(v)` will be used to coerce `bytearray`, `v.encode()` will be used to coerce `str`, and `str(v).encode()` will be used to coerce numeric types.

Let's see an example of type coercion for each of these types (with the exception of `None` which does not use coercion).


```python
class TypeCoercionExample(BaseModel):
    v_bool: bool
    v_int: int
    v_float: float
    v_str: str
    v_bytes: bytes


display(
    TypeCoercionExample(
        v_bool="no",
        v_int=25.7,
        v_float=True,
        v_str=False,
        v_bytes="hello",
    )
)
```


    TypeCoercionExample(v_bool=False, v_int=25, v_float=1.0, v_str='False', v_bytes=b'hello')


As expected
* `v_bool="no"` was coerced to `v_bool=False`
* `v_int=25.7` was coerced to `v_int=25`    (Note the loss of information mentioned above)
* `v_float=True` was coerced to `v_float=1.0`
* `v_str=False` was coerced to `v_str='False'`
* `v_bytes="hello"` was coerced to `v_bytes=b'hello'`

A detailed description of supported types can be found in the "Field Types" documentation page: https://docs.pydantic.dev/latest/usage/types/

## Type validation (sneak peak)

What happens when type coercion fails? This brings us to one of the main benefits of using Pydantic -- type validation. We will be discussing this in much more detail in part 3 of this tutorial, but let's get a sense of what will happen now while type coercion is still fresh in our minds.

Recall our earlier example of the two-dimensional coordinate points. If we provided invalid arguments for `PointV1` and `PointV2` (recall these were not Pydantic models), the classes would happily instantiate and we would not see an error until later when trying to compute the distance between two points. And the error message didn't really point to the root cause of the problem, which was the invalid arguments during instantiation. We also showed that when using a Pydantic model (`PointV3`), Pydantic would attempt to correct our mistake for us using type coercion. But what if we provide arguments where type coercion fails? Let's find out. Returning to the earlier example, let's now provide arguments that will not pass type coercion.


```python
class PointV3(BaseModel):
    """Representation of a two-dimensional point coordinate."""

    x: float
    y: float

    def distance_to(self, other: "PointV3") -> float:
        """Computes the distance to another `PointV3`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5


PointV3(
    x=5,
    y="this string cannot be coerced to a float",
)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[9], line 14
         10         dy = self.y - other.y
         11         return (dx**2 + dy**2) ** 0.5
    ---> 14 PointV3(
         15     x=5,
         16     y="this string cannot be coerced to a float",
         17 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for PointV3
    y
      value is not a valid float (type=type_error.float)


Pydantic throws an error at the root cause and provides a helpful message! The message tells us that the provided value for field `y` is not valid for type `float`. This is potentially a big time saver when it comes to debugging. As mentioned above we will be diving much deeper into type validation later, but hopefully you now have a sense of what it is and why it is useful.

## Default and optional values

We can provide default field values by providing an `=` followed by the default value. We can create optional fields by importing `typing.Optional` and surrounding the type hint with `Optional`. The value of optional fields when not supplied by the user will be `None`.

Let's provide an example by creating a new class that represents a line segment consisting of two x-y coordinates and an optional label. The first x-y coordinate will have default values set to the origin.


```python
from typing import Optional


class LineSegment(BaseModel):
    x1: float = 0.0
    y1: float = 0.0
    x2: float
    y2: float
    label: Optional[str]
```

So `x1` and `y1` will default to `0.0` if not provided, `x2` and `y2` are required, and `label` is a string that defaults to `None` if not provided. Let's create a few `LineSegment` examples.


```python
display(
    LineSegment(x1=5, y1=6, x2=1, y2=9, label="red"),
)
display(
    LineSegment(x2=1, y2=9, label="red"),
)
display(
    LineSegment(x2=1, y2=9),
)
```


    LineSegment(x1=5.0, y1=6.0, x2=1.0, y2=9.0, label='red')



    LineSegment(x1=0.0, y1=0.0, x2=1.0, y2=9.0, label='red')



    LineSegment(x1=0.0, y1=0.0, x2=1.0, y2=9.0, label=None)


And we get the expected behavior.

## Model configuration

Pydantic provides custamizable options for models. The model just needs to define a class called `Config` as an attribute. The attributes of `Config` serve as a configuration for the model.

As an example, let's explore what happens when you instantiate a Pydantic model with fields that are not part of the model definition. By default, Pydantic models will ignore these additional fields. Let's provide our `LineSegment` model with an unexpected field...


```python
display(
    LineSegment(x2=1, y2=9, hello="world"),
)
```


    LineSegment(x1=0.0, y1=0.0, x2=1.0, y2=9.0, label=None)


As expected the field `hello` was ignored and not included in the instantiated model. But we can configure the model to either allow or forbid extra fields not defined in the class...


```python
from pydantic import Extra


class LineSegment(BaseModel):
    x1: float = 0.0
    y1: float = 0.0
    x2: float
    y2: float
    label: Optional[str]

    class Config:
        extra = Extra.allow


display(
    LineSegment(x2=1, y2=9, hello="world"),
)
```


    LineSegment(x1=0.0, y1=0.0, x2=1.0, y2=9.0, label=None, hello='world')



```python
class LineSegment(BaseModel):
    x1: float = 0.0
    y1: float = 0.0
    x2: float
    y2: float
    label: Optional[str]

    class Config:
        extra = Extra.forbid


display(
    LineSegment(x2=1, y2=9, hello="world"),
)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[14], line 13
          8     class Config:
          9         extra = Extra.forbid
         12 display(
    ---> 13     LineSegment(x2=1, y2=9, hello="world"),
         14 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for LineSegment
    hello
      extra fields not permitted (type=value_error.extra)


Class inheritance works as expected with Pydantic models...


```python
class A(BaseModel):
    x: int

    class Config:
        extra = Extra.forbid


class B(A):
    y: bool


class C(BaseModel):
    z: str


print(f"{A.Config.extra = }\t{A.__fields__.keys() = }")
print(f"{B.Config.extra = }\t{B.__fields__.keys() = }")
print(f"{C.Config.extra = }\t{C.__fields__.keys() = }")
```

    A.Config.extra = <Extra.forbid: 'forbid'>	A.__fields__.keys() = dict_keys(['x'])
    B.Config.extra = <Extra.forbid: 'forbid'>	B.__fields__.keys() = dict_keys(['x', 'y'])
    C.Config.extra = <Extra.ignore: 'ignore'>	C.__fields__.keys() = dict_keys(['z'])


Notice that `B`, which inherits from `A`, inherits the field, `x`, and configuration, `extra = Extra.forbid`, of `A`, while `C`, which is a base Pydantic model, does not contain the field `x` and obtains the default value of `Extra.ignore` for the `extra` configuration.

A detailed description of possible configurations can be found in the "Model Config" documentation page: https://docs.pydantic.dev/latest/usage/model_config/

## Exercise 2

Consider the following set of weather data for the city of Murmansk, Russia:

```python
data_samples = [
    {
        "date": "2023-05-20",
        "temperature": 62.2,
        "isCelsius": False,
        "airQualityIndex": "24",
        "sunriseTime": "01:26",
        "sunsetTime": "00:00",
    },
    {
        "date": "2023-05-21",
        "temperature": "64.4",
        "isCelsius": "not true",
        "airQualityIndex": 23,
        "sunriseTime": "01:10",
        "sunsetTime": "00:16",
    },
    {
        "date": "2023-05-22",
        "temperature": 14.4,
        "airQualityIndex": 21,
    },
]
```

Write a script that computes and prints the average temperature (in celsius) in Murmansk for the dates provided. In your script, you should include a Pydantic model capable of parsing a single sample from the list of data samples above. You should parse each data sample one at a time using a `for` loop. (We will see how to parse the entire list simultaneously in the next section of this tutorial.)

Some potentially helpful notes:
* Some samples are missing data. You should decide how to handle these without inserting new data yourself (but modification of existing data is OK). Hint: refer to the "Default and optional values" section 
* Some values may produce errors and may need modification.
* You may parse dates and times as strings for this exercise. (We will see a better way to parse dates and times later in this tutorial.)
* You may assume `airQualityIndex` is an integer valued categorical variable.
