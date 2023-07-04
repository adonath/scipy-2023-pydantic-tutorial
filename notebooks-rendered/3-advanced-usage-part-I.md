# 3. Advanced Usage I

**Concepts:**
- Complex types, typed lists and dictionaries
- Complex types, Enums and Unions
- Datetime types
- Custom types / hierarchical structures
- Private attributes and class variables



## Complex Types

We have already seen how to define classes / models using simple types, such as `int`, `float`, `str`, `bool`, etc. However in practice data structures are often more complex. They include for examples dictionaries, list of lists, or mutiple allowed types. Of course Pydantic also supports these more complex types, such as lists, dictionaries, enums, and unions. In the following we will see an overview of those types and how to use them:


### Typed Lists and Dictionaries

Lists and dictionaries are very common data structures in Python. Pydantic supports typed lists and dictionaries, which means that we can also define the type of the elements in the list or the type of the values in the dictionary.
Typed lists and dictionaries are defined using the `list` and `dict` generic types. For example, we can define a model with a list of floats as follows:


```python
from pydantic import BaseModel


class LineV1(BaseModel):
    """A Line object represented by two lists of coordinates"""

    x: list[float]
    y: list[float]

    def length(self):
        """Line length computed by summing over the distance between points"""
        length = 0

        for idx in range(len(self.x) - 1):
            length += (
                (self.x[idx] - self.x[idx + 1]) ** 2
                + (self.y[idx] - self.y[idx + 1]) ** 2
            ) ** 0.5

        return length
```

Instantiation of the model works as expected:


```python
line_v1 = LineV1(x=[0, 1, 3], y=[0, 1, 2])
display(line_v1)
```


    LineV1(x=[0.0, 1.0, 3.0], y=[0.0, 1.0, 2.0])



```python
print(line_v1.length())
```

    3.6502815398728847


The behavior is exactly the same as for simple types. So values are converted to the specified type if possible:


```python
line_v1 = LineV1(x=[0, 1, "3"], y=[0, True, 2])
display(line_v1)
```


    LineV1(x=[0.0, 1.0, 3.0], y=[0.0, 1.0, 2.0])


If the type cannot be converted a `ValidationError` is raised:


```python
line_v1 = LineV1(x=[0, 1, "10^-2"], y=[0, 1, 2])
display(line_v1)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[5], line 1
    ----> 1 line_v1 = LineV1(x=[0, 1, "10^-2"], y=[0, 1, 2])
          2 display(line_v1)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for LineV1
    x -> 2
      value is not a valid float (type=type_error.float)


Note that pydantic indicates the index of the invalid value in the error message using `x -> 2`.

Typed dictionaries are defined in a similar way using the `dict` generic type:


```python
from pydantic import BaseModel


class LineV2(BaseModel):
    """A Line object represented by two lists of coordinates"""

    coordinates: dict[str, list[float]]

    def length(self):
        """Line length computed by summing over the distance between points"""
        length = 0
        x = self.coordinates["x"]
        y = self.coordinates["y"]

        for idx in range(len(x) - 1):
            length += ((x[idx] - x[idx + 1]) ** 2 + (y[idx] - y[idx + 1]) ** 2) ** 0.5

        return length
```

Now we define some data an create the model:


```python
coordinates = {
    "x": [0, 1, 3],
    "y": [0, 1, 2],
}

line_v2 = LineV2(coordinates=coordinates)
```

For illustration purposes we also create a model with invalid data:


```python
coordinates = {
    "x": [0, "one", 3],
    "y": [0, 1, "three"],
}

line_v2 = LineV2(coordinates=coordinates)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[8], line 6
          1 coordinates = {
          2     "x": [0, "one", 3],
          3     "y": [0, 1, "three"],
          4 }
    ----> 6 line_v2 = LineV2(coordinates=coordinates)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 2 validation errors for LineV2
    coordinates -> x -> 1
      value is not a valid float (type=type_error.float)
    coordinates -> y -> 2
      value is not a valid float (type=type_error.float)


Again pydantic raises a meaningful error message and also indicates the keys and indices of the invalid values.

### Enums and Union Types

In many cases it is useful to provide users with a selection of valid values, such as a choice of strings. The data structure to handle this is called `Enum`. Enums are defined using the `Enum` generic type in Python. For example, we can define a selection for the addtional property of a line color:



```python
from pydantic import BaseModel
from enum import Enum


class LineColor(str, Enum):
    """Line color enum"""

    red = "red"
    green = "green"
    blue = "blue"
```

And add this to the definiton of the line class:


```python
class ColoredLine(BaseModel):
    """A Line object that can be used to represent a line."""

    x: list[float]
    y: list[float]
    color: LineColor = LineColor.red

    def length(self):
        """Length of the line"""
        length = 0

        for idx in range(len(self.x) - 1):
            length += (
                (self.x[idx] - self.x[idx + 1]) ** 2
                + (self.y[idx] - self.y[idx + 1]) ** 2
            ) ** 0.5

        return length
```

On initialisation we can now pass a color:


```python
colored_line = ColoredLine(x=[0, 1, 2], y=[0, 1, 2], color="red")
display(colored_line)
```


    ColoredLine(x=[0.0, 1.0, 2.0], y=[0.0, 1.0, 2.0], color=<LineColor.red: 'red'>)


Now let's try an invalid color:


```python
colored_line = ColoredLine(x=[0, 1, 2], y=[0, 1, 2], color="purple")
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[12], line 1
    ----> 1 colored_line = ColoredLine(x=[0, 1, 2], y=[0, 1, 2], color="purple")


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for ColoredLine
    color
      value is not a valid enumeration member; permitted: 'red', 'green', 'blue' (type=type_error.enum; enum_values=[<LineColor.red: 'red'>, <LineColor.green: 'green'>, <LineColor.blue: 'blue'>])


Pydantic now gives a useful error message, saying that the value is not a valid enumeration member; and it also lists the valid choices.

Now we try to modify the color of an exising instance:


```python
colored_line.color = "violet"
```

By default pydantic only validates / parses the values on initialisation. If we want to validate the values on modification we can use the `validate_assignment` configuaration option:


```python
class ColoredLine(BaseModel):
    """A Line object that can be used to represent a line."""

    x: list[float]
    y: list[float]
    color: LineColor = LineColor.red

    class Config:
        """Pydantic Config object"""

        validate_assignment = True
```


```python
colored_line = ColoredLine(x=[0, 1, 2], y=[0, 1, 2], color="red")
colored_line.color = "purple"
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[15], line 2
          1 colored_line = ColoredLine(x=[0, 1, 2], y=[0, 1, 2], color="red")
    ----> 2 colored_line.color = "purple"


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:384, in pydantic.main.BaseModel.__setattr__()


    ValidationError: 1 validation error for ColoredLine
    color
      value is not a valid enumeration member; permitted: 'red', 'green', 'blue' (type=type_error.enum; enum_values=[<LineColor.red: 'red'>, <LineColor.green: 'green'>, <LineColor.blue: 'blue'>])


**Note:** that there is https://github.com/pydantic/pydantic-extra-types, which provides support for validation of CSS colors. `from pydantic.color import Color`, so there is actually no reason to implement this ourselves.


```python
from typing import Union

from pydantic import BaseModel
from enum import Enum


class LineColor(str, Enum):
    """Line color enum"""

    red = "red"
    green = "green"
    blue = "blue"


class LineV2(BaseModel):
    """A Line object that can be used to represent a line."""

    x: list[float]
    y: list[float]
    color: Union[LineColor, None] = LineColor.red
```


### Datetime Types

Another very useful advanced type is the `datetime`, which lets users handle dates and times. Pydantic natively supports parsing and validation of datetime types. This relies on the Python standard library (see https://docs.python.org/3/library/datetime.html). Let's take a look at an example:




```python
from datetime import datetime


class LonLatTimeVector(BaseModel):
    """Represents a position on earth with time."""

    lon: float = 0.0
    lat: float = 0.0
    time: datetime = None


position = LonLatTimeVector(lon=1.0, lat=2.0, time=datetime.now())
display(position)
```


    LonLatTimeVector(lon=1.0, lat=2.0, time=datetime.datetime(2023, 7, 25, 15, 18, 23, 759435))


Remember you can always check the type using `type()`:


```python
type(position.time)
```




    datetime.datetime



So `datetime.now()` already creates a `datetime` object, but pydantic also supports other valid formats, such as:


```python
# Time in ISO format
position = LonLatTimeVector(time="2021-01-01T00:00:00")
display(position)
```


    LonLatTimeVector(lon=0.0, lat=0.0, time=datetime.datetime(2021, 1, 1, 0, 0))



```python
# Ints or floats interpred as unix time, i.e. seconds since 1970-01-01T00:00:00
position = LonLatTimeVector(time=1609459200)
display(position)
```


    LonLatTimeVector(lon=0.0, lat=0.0, time=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))


Let's try to pass an invalid datetime:


```python
position = LonLatTimeVector(time="2021-01-01")
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[21], line 1
    ----> 1 position = LonLatTimeVector(time="2021-01-01")


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for LonLatTimeVector
    time
      invalid datetime format (type=value_error.datetime)


There is variety of other date and time related quantities, which might be useful:


```python
from datetime import date, datetime, time, timedelta
from pydantic import BaseModel


class Model(BaseModel):
    d: date = None
    dt: datetime = None
    t: time = None
    td: timedelta = None


m = Model(
    d=1966280412345.6789,  # Unix time in seconds
    dt="2032-04-23T10:20:30.400+02:30",  # Time in ISO format
    t=time(4, 8, 16),  # Time object hours, minutes, seconds, [milliseconds]
    td="P3DT12H30M5S",  # ISO 8601 duration format
)

display(m)
```


    Model(d=datetime.date(2032, 4, 22), dt=datetime.datetime(2032, 4, 23, 10, 20, 30, 400000, tzinfo=datetime.timezone(datetime.timedelta(seconds=9000))), t=datetime.time(4, 8, 16), td=datetime.timedelta(days=3, seconds=45005))


### Other Types

Pydantic has a few useful factory functions for building types that have additional validations built in. For example, `pydantic.conint` is a function with parameters that allow you to build a constrained integer. This could be used to create a `MovieRating` type that only allows integers from 0 to 100:
```python
from pydantic import BaseModel, conint

MovieRating = conint(ge=0, le=100)

class Movie(BaseModel):
    name: str
    year: int
    rating: MovieRating
```

On top of the normal integer validations, `Movie` will throw a validation error if the value provided is an integer less than 0 or greater than 100.

Other useful type factories exist, such as `conlist`, `confloat`, `constr`, `condate`, and more. Pydantic has also exposed specific instantiations of some of these type factories that are commonly used. A few examples include, but are not limited to, `NegativeInt`, `NonNegativeInt`, `PositiveInt`, `NonPositiveInt`, and the `float` counterparts. You can guess how each of these are created from `conint` and `confloat`.

There are a variety of other useful types built into pydantic. We have already mentioned several above. Most of the types not mentioned above are mostly relevant for web development but it is nonetheless good to know that they exist. For an overview of those types see https://docs.pydantic.dev/1.10/usage/types/#pydantic-types and also https://github.com/pydantic/pydantic-extra-types (unreleased).

### Custom Data Types / Hierarchical Structures

One of the most powerful features of Pydantic is the ability to combine models to create hierarchical structures. This is done simply by using an existing pydantic model as a new type. For example we easily define a triangle using three points:



```python
from pydantic import BaseModel


class Point(BaseModel):
    """Representation of a two-dimensional point coordinate."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Computes the distance to another `PointV3`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5


class Triangle(BaseModel):
    """Representation of a triangle"""

    point_a: Point = Point(x=0, y=0)
    point_b: Point = Point(x=1, y=0)
    point_c: Point = Point(x=0, y=1)

    def circumference(self):
        """Circumference of the triangle"""
        return (
            self.point_a.distance_to(self.point_b)
            + self.point_b.distance_to(self.point_c)
            + self.point_c.distance_to(self.point_a)
        )


triangle = Triangle(
    point_a=Point(x=0, y=0),
    point_b=Point(x=0.5, y=0),
    point_c=Point(x=0, y=0.5),
)

display(triangle)
```


    Triangle(point_a=Point(x=0.0, y=0.0), point_b=Point(x=0.5, y=0.0), point_c=Point(x=0.0, y=0.5))



```python
print(triangle.circumference())
```

    1.7071067811865475


Alternatively in this case we can also pass a dictionary to the model without creating the `Point` instances first:


```python
triangle = Triangle(
    point_a={"x": 0, "y": 0.5},
    point_b={"x": 0.5, "y": 0},
    point_c={"x": 0, "y": 0},
)

print(triangle.circumference())
```

    1.7071067811865475


Pydantic will automatically convert the dictionaries to `Point` instances by passing the arguments to `Point(**kwargs)`. This is already a preview of the serialization and deserialization of models into dictionaries and hierarchical languages such as JSON, YAML and TOML. Let's quickly verify the type of the point:


```python
type(triangle.point_a)
```




    __main__.Point



Of course this also works for list of `Point` objects. For example we can rewrite the definition of the `Line` class we introduced above as follows:


```python
from pydantic import BaseModel


class Point(BaseModel):
    """Representation of a two-dimensional point coordinate."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Computes the distance to another `PointV3`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5


class LineV3(BaseModel):
    """Line object represented by a list of points"""

    points: list[Point]

    def length(self):
        """Line length computed by summing over the distance between points"""
        length = 0

        for point, next_point in zip(self.points[:-1], self.points[1:]):
            length += point.distance_to(next_point)

        return length
```

Which can now be used as follows:


```python
line_v3 = LineV3(points=[Point(x=0, y=0), Point(x=1, y=1)])
display(line_v3)
```


    LineV3(points=[Point(x=0.0, y=0.0), Point(x=1.0, y=1.0)])



```python
print(line_v3.length())
```

    1.4142135623730951


If you compare to our first implementation at the beginning, `LineV3` is more compact, readable and elegant. 


### Private Attributes and Class Variables

Because of the way model attributes are defined in Pydantic, we cannot simply define a normal class attribute or "normal" Python attribute for a class. However in some cases we might want to introduce e.g. an internal attribute that is not part of the Pydantic model. The usual Python convention for non-public attributes is to prefix them with an underscore `_`. By convention attributes starting with an underscore are excluded from the Pydantic model.

Let's try the following first:


```python
from pydantic import BaseModel


class LineV4(BaseModel):
    """Line object represented by a list of points"""

    points: list[Point]
    _color: LineColor = LineColor.red

    def is_red(self):
        return self._color == LineColor.red
```

Let's instantiate the model:


```python
line_with_hidden_color = LineV4(
    points=[Point(x=0, y=0), Point(x=1, y=1)],
)
```

You can see that the `_color` attribute is not part of the model:


```python
line_with_hidden_color.__fields__
```




    {'points': ModelField(name='points', type=List[Point], required=True)}



But you can access it internally as usual, e.g. in the `is_red()` method we defined above:


```python
line_with_hidden_color.is_red()
```




    True



However it cannot be modified from the outside:


```python
line_with_hidden_color._color = "blue"
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    Cell In[34], line 1
    ----> 1 line_with_hidden_color._color = "blue"


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:357, in pydantic.main.BaseModel.__setattr__()


    ValueError: "LineV4" object has no field "_color"


This behaviour is obviously is different from a "normal" Python class attribute. 

Howver if you need to vary or manipulate internal attributes on instances of the model, you can declare them using `PrivateAttr` instead:


```python
from pydantic import BaseModel, PrivateAttr


class LineV5(BaseModel):
    """Line object represented by a list of points"""

    points: list[Point]
    _color: LineColor = PrivateAttr(LineColor.red)

    # as this now behaves as a "normal" Python attribute, we need to set it on init
    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("_color", LineColor.red)

    def is_red(self):
        return self._color == LineColor.red
```

Let's try the behaviour now:


```python
line_with_hidden_color = LineV5(
    points=[Point(x=0, y=0), Point(x=1, y=1)], _color="violet"
)

line_with_hidden_color.is_red()
```




    False




```python
line_with_hidden_color._color = "red"
line_with_hidden_color.is_red()
```




    True



Now this behaves like a normal Python class attribute. But note that it is also not being validated, just as a normal Python attribute. That's why we could set it to violet, even though it is not a valid color.

In case you have many private attributes you can also use the config setting to achieve the equivalent behaviour:


```python
from pydantic import BaseModel


class LineV6(BaseModel):
    """Line object represented by a list of points"""

    points: list[Point]
    _color: LineColor = LineColor.red

    class Config:
        underscore_attrs_are_private = True

    # as this now behaves as a "normal" Python attribute, we need to set it on init
    def __init__(self, **data):
        super().__init__(**data)
        self._color = data.get("_color", LineColor.red)

    def is_red(self):
        return self._color == LineColor.red
```


```python
line_with_hidden_color = LineV5(points=[Point(x=0, y=0), Point(x=1, y=1)], _color="red")
line_with_hidden_color.is_red()
```




    True



Theres is one more rare case to be covered: in some cases you might want to define a class variable, which is shared by all instances of the model. The "normal" syntax is occupied by the Pydantic model declaration. However we can still define class variables using the `ClassVar` type:


```python
from typing import ClassVar
from pydantic import BaseModel


class LineV6(BaseModel):
    """Line object represented by a list of points"""

    points: list[Point]
    color: ClassVar[LineColor] = LineColor.red

    def is_red(self):
        return self._color == LineColor.red
```

Again the variable is not part of the pydantic model:


```python
line_global_color = LineV6(
    points=[Point(x=0, y=0), Point(x=1, y=1)],
)
line_global_color.__fields__
```




    {'points': ModelField(name='points', type=List[Point], required=True)}



However it can be accessed and modified as a normal Python class variable:


```python
other_line_global_color = LineV6(
    points=[Point(x=0, y=0), Point(x=1, y=1)],
)

# We modify the class variable
LineV6.color = LineColor.green

# The change is reflected in both instances
print(line_global_color.color)
print(other_line_global_color.color)
```

    LineColor.green
    LineColor.green


## Exercise 3


We will be using the [open-meteo](https://open-meteo.com/en/docs) free weather API to make a request to the <https://api.open-meteo.com/v1/forecast> endpoint. We will fetch temperature data for Austin, TX on an hourly cadence for all of 2023.

To do this we will use the [requests](https://requests.readthedocs.io/en/latest/) third-party Python library. For anyone new to `requests`, here is a quick primer. Imagine you want to receive the response from the example URL: <https://example.com/api/v2/foo?bar=1&bap=scipy2023&baz=false>. Then the response can be obtained with:
```python
import requests

api_endpoint = "https://example.com/api/v2/foo"
params = {"bar": 1, "bap": "scipy2023", "baz": False}
response = requests.get(url=api_endpoint, params=params)
print(response.content)
```
The requests library has many additional features that you can find in the documentation linked above, but for this exercise, this should be all you need.

Task: Write a script that makes a request to the open-meteo API enpoint with the following constraints:

* Use Austin, TX as the location. Hint: you may need to look up the latitude and longitude.
* You should request the hourly temperature 2m above ground.
* Use GMT as the timezone.
* The range of dates is from the beginning of 2023 to today.

You should create a Pydantic model that parses and validates the response from the request. Your Pydantic model should be precise (i.e. include as many validations and specific type hints as possible) but also flexible (examples may include (a) allowing for accepting either celsius or fahrenheit or (b) allowing for either ISO8601 or unix time). Your model should also be hierarchical to account for the nested structure of the API response. In order to understand the expected response needed to build your model, you may want to spend a few minutes reading the open-meteo documentation (linked above) and/or playing around with the open-meteo UI (also at the linked documentation).

After receiving the response, compute the daily average temperature and plot it as a function of time. You can use any plotting library you like, but we recommend [matplotlib](https://matplotlib.org/stable/index.html) and for the averaging you could use e.g. [pandas](https://pandas.pydata.org/).




