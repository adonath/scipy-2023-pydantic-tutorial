# Serialization and Deserialization

**Concepts:**
* Motivation - Need for serialization and deserialization of Python objects
* Introduce JSON / YAML / TOML formats
* Serialize Pydantic models to from JSON / YAML
* Deserialize Pydantic models to from JSON / YAML
* Implementing JSON encoders for custom types
* Config of serialization, excluding and including fields

In order to make use of Pydantic models we will need to get data in and/or out of instances of our models. This is known as deserialization and serialization, respectively. Pydantic was originally designed with the primary use case being web development where data is frequently serialized and deserialized in order to send and receive data between client and server. But Pydantic models can be useful in many other situations including, but not limited to, configuration files and data storage. The native Python serialization protocol is the pickle format, which is compatible with Pydantic, but pickling only works in a pure Python system. If interfacing with other systems, pickling may not be possible. Furthermore, you may not always have control of the data files you need to validate. Common file formats used in the Python ecosystem are JSON (Javascript object notation), YAML (yet another markup language), and TOML (Tom's obvious, minimal language). Before we see examples of each of these, let's first create a function that takes in a serialization function and a deserialization function. The function will serialize a global data dict to string and print the string. It will then deserialize the string back to a Python object and print the object.


```python
from typing import Any, Callable, Optional

data = {
    "data": [0, 1, 1, 2, 3, 5],
    "attributes": {
        "is_fibonacci": True,
        "base_cases": {"f0": 0, "f1": 1},
    },
}


def serialize_then_deserialize(
    serialization_function: Callable[[Any], str],
    deserialization_function: Callable[[str], Any],
    serialization_kwargs: Optional[dict[str, Any]] = None,
    deserialization_kwargs: Optional[dict[str, Any]] = None,
) -> None:
    if serialization_kwargs is None:
        serialization_kwargs = {}
    if deserialization_kwargs is None:
        deserialization_kwargs = {}

    data_serialized = serialization_function(
        data,
        **serialization_kwargs,
    )
    print("Serialized data to string:")
    print(data_serialized)

    data_serialized_deserialized = deserialization_function(
        data_serialized,
        **deserialization_kwargs,
    )
    print("\nDeserialized data from string:")
    print(data_serialized_deserialized)
```

**JSON**

Python has native JSON support in the standard library module `json`. Deserialization can be accomplished using `json.load` and `json.loads`, with the former taking a file pointer (an object with a `.read()` method) and the latter taking a `str`, `bytes`, or `bytearray`. The analogous counterparts (serialization) can be accomplished with `json.dump` and `json.dumps`, respectively.


```python
import json

serialize_then_deserialize(
    serialization_function=json.dumps,
    deserialization_function=json.loads,
    serialization_kwargs={"indent": 2},
)
```

    Serialized data to string:
    {
      "data": [
        0,
        1,
        1,
        2,
        3,
        5
      ],
      "attributes": {
        "is_fibonacci": true,
        "base_cases": {
          "f0": 0,
          "f1": 1
        }
      }
    }
    
    Deserialized data from string:
    {'data': [0, 1, 1, 2, 3, 5], 'attributes': {'is_fibonacci': True, 'base_cases': {'f0': 0, 'f1': 1}}}


**YAML**

Python does not natively support YAML files but third-party libraries exist such as PyYAML. Deserialization is accomplished with `yaml.load` and serialization is accomplished with `yaml.dump`. WARNING: The YAML specification is much more flexible than JSON and allows for execution of arbitrary Python functions. Thus it is recommended to use `yaml.load` only if your data comes from a trusted source. PyYAML also has `yaml.safe_load` and `yaml.safe_dump` that do not recognize arbitray Python objects.


```python
import yaml

serialize_then_deserialize(
    serialization_function=yaml.safe_dump,
    deserialization_function=yaml.safe_load,
    serialization_kwargs={"sort_keys": False},
)
```

    Serialized data to string:
    data:
    - 0
    - 1
    - 1
    - 2
    - 3
    - 5
    attributes:
      is_fibonacci: true
      base_cases:
        f0: 0
        f1: 1
    
    
    Deserialized data from string:
    {'data': [0, 1, 1, 2, 3, 5], 'attributes': {'is_fibonacci': True, 'base_cases': {'f0': 0, 'f1': 1}}}


**TOML**

Starting with Python 3.11, Python does have native support for TOML files in the `tomllib` module. Earlier versions of python can use the `toml` third-party library. Like the `json` module, deserialization and serialization is accomplished with the `load`, `loads`, `dump`, and `dumps` functions.


```python
import toml

serialize_then_deserialize(
    serialization_function=toml.dumps,
    deserialization_function=toml.loads,
)
```

    Serialized data to string:
    data = [ 0, 1, 1, 2, 3, 5,]
    
    [attributes]
    is_fibonacci = true
    
    [attributes.base_cases]
    f0 = 0
    f1 = 1
    
    
    Deserialized data from string:
    {'data': [0, 1, 1, 2, 3, 5], 'attributes': {'is_fibonacci': True, 'base_cases': {'f0': 0, 'f1': 1}}}


## Pydantic integration

For deserialization Pydantic models have the `parse_raw`, `parse_obj`, and `parse_file` methods for `str`, `dict`, and `pathlib.Path` objects, respectively. Let's see each one in action by using the weather data in `my-data.json`. First we need to inspect the data and create a Pydantic model to represent the schema of the data.


```python
import datetime

from pydantic import BaseModel


class TemperatureSample(BaseModel):
    date: datetime.date
    time: datetime.time
    temperature: float


class TemperatureData(BaseModel):
    data: list[TemperatureSample]
```

Let's start by reading the data in as a string and deserializing the string...


```python
from pathlib import Path

fpath_temperature_data = Path.cwd() / "my-data.json"

raw_temperature_data = fpath_temperature_data.read_text()
print("Raw, unparsed, unvalidated data in string form:")
display(raw_temperature_data)

temperature_data = TemperatureData.parse_raw(raw_temperature_data)
print("\nDeserialized data as a Pydantic model instance:")
display(temperature_data)
```

    Raw, unparsed, unvalidated data in string form:



    '{\n  "data": [\n    {\n      "date": "2023-06-01",\n      "time": "00:00:00",\n      "temperature": 18.5\n    },\n    {\n      "date": "2023-06-01",\n      "time": "01:00:00",\n      "temperature": 18.2\n    },\n    {\n      "date": "2023-06-01",\n      "time": "02:00:00",\n      "temperature": 17.8\n    },\n    {\n      "date": "2023-06-01",\n      "time": "03:00:00",\n      "temperature": 17.4\n    },\n    {\n      "date": "2023-06-01",\n      "time": "04:00:00",\n      "temperature": 16.9\n    },\n    {\n      "date": "2023-06-01",\n      "time": "05:00:00",\n      "temperature": 16.5\n    },\n    {\n      "date": "2023-06-01",\n      "time": "06:00:00",\n      "temperature": 16.1\n    },\n    {\n      "date": "2023-06-01",\n      "time": "07:00:00",\n      "temperature": 16.3\n    },\n    {\n      "date": "2023-06-01",\n      "time": "08:00:00",\n      "temperature": 17.2\n    },\n    {\n      "date": "2023-06-01",\n      "time": "09:00:00",\n      "temperature": 18.8\n    },\n    {\n      "date": "2023-06-01",\n      "time": "10:00:00",\n      "temperature": 20.4\n    },\n    {\n      "date": "2023-06-01",\n      "time": "11:00:00",\n      "temperature": 21.9\n    },\n    {\n      "date": "2023-06-01",\n      "time": "12:00:00",\n      "temperature": 23.1\n    },\n    {\n      "date": "2023-06-01",\n      "time": "13:00:00",\n      "temperature": 24.0\n    },\n    {\n      "date": "2023-06-01",\n      "time": "14:00:00",\n      "temperature": 24.3\n    },\n    {\n      "date": "2023-06-01",\n      "time": "15:00:00",\n      "temperature": 23.8\n    }\n  ]\n}'


    
    Deserialized data as a Pydantic model instance:



    TemperatureData(data=[TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(0, 0), temperature=18.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(1, 0), temperature=18.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(2, 0), temperature=17.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(3, 0), temperature=17.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(4, 0), temperature=16.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(5, 0), temperature=16.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(6, 0), temperature=16.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(7, 0), temperature=16.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(8, 0), temperature=17.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(9, 0), temperature=18.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(10, 0), temperature=20.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(11, 0), temperature=21.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(12, 0), temperature=23.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(13, 0), temperature=24.0), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(14, 0), temperature=24.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(15, 0), temperature=23.8)])


The output is not so human friendly but we successfuly deserialized the raw JSON string into an instance of `TemperatureData`. Note that because the data is now in a `TemperatureData` instance, the data is also parsed and validated! Now what if we already had the data in memory as a Python object. Then we could use the `parse_obj` method...


```python
raw_temperature_data_dict = json.loads(raw_temperature_data)
print("Raw, unparsed, unvalidated data in dictionary form:")
display(raw_temperature_data_dict)

temperature_data = TemperatureData.parse_obj(raw_temperature_data_dict)
print("\nDeserialized data as a Pydantic model instance:")
display(temperature_data)
```

    Raw, unparsed, unvalidated data in dictionary form:



    {'data': [{'date': '2023-06-01', 'time': '00:00:00', 'temperature': 18.5},
      {'date': '2023-06-01', 'time': '01:00:00', 'temperature': 18.2},
      {'date': '2023-06-01', 'time': '02:00:00', 'temperature': 17.8},
      {'date': '2023-06-01', 'time': '03:00:00', 'temperature': 17.4},
      {'date': '2023-06-01', 'time': '04:00:00', 'temperature': 16.9},
      {'date': '2023-06-01', 'time': '05:00:00', 'temperature': 16.5},
      {'date': '2023-06-01', 'time': '06:00:00', 'temperature': 16.1},
      {'date': '2023-06-01', 'time': '07:00:00', 'temperature': 16.3},
      {'date': '2023-06-01', 'time': '08:00:00', 'temperature': 17.2},
      {'date': '2023-06-01', 'time': '09:00:00', 'temperature': 18.8},
      {'date': '2023-06-01', 'time': '10:00:00', 'temperature': 20.4},
      {'date': '2023-06-01', 'time': '11:00:00', 'temperature': 21.9},
      {'date': '2023-06-01', 'time': '12:00:00', 'temperature': 23.1},
      {'date': '2023-06-01', 'time': '13:00:00', 'temperature': 24.0},
      {'date': '2023-06-01', 'time': '14:00:00', 'temperature': 24.3},
      {'date': '2023-06-01', 'time': '15:00:00', 'temperature': 23.8}]}


    
    Deserialized data as a Pydantic model instance:



    TemperatureData(data=[TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(0, 0), temperature=18.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(1, 0), temperature=18.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(2, 0), temperature=17.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(3, 0), temperature=17.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(4, 0), temperature=16.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(5, 0), temperature=16.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(6, 0), temperature=16.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(7, 0), temperature=16.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(8, 0), temperature=17.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(9, 0), temperature=18.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(10, 0), temperature=20.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(11, 0), temperature=21.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(12, 0), temperature=23.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(13, 0), temperature=24.0), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(14, 0), temperature=24.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(15, 0), temperature=23.8)])


Again we have deserialized, parsed, and validated the data into a `TemperatureData` instance. Finally, if we only have the path to a file containing the data, we can use the `parse_file` method...


```python
temperature_data = TemperatureData.parse_file(fpath_temperature_data)
print("Deserialized data as a Pydantic model instance:")
display(temperature_data)
```

    Deserialized data as a Pydantic model instance:



    TemperatureData(data=[TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(0, 0), temperature=18.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(1, 0), temperature=18.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(2, 0), temperature=17.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(3, 0), temperature=17.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(4, 0), temperature=16.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(5, 0), temperature=16.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(6, 0), temperature=16.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(7, 0), temperature=16.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(8, 0), temperature=17.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(9, 0), temperature=18.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(10, 0), temperature=20.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(11, 0), temperature=21.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(12, 0), temperature=23.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(13, 0), temperature=24.0), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(14, 0), temperature=24.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(15, 0), temperature=23.8)])


Notes:
* Currently pydantic only supports JSON and pickle files in the `parse_file` method. `pydantic-yaml` is an extension to Pydantic that provides this support, but a workaround is to load the data into memory and then use `parse_obj` or `parse_raw`.
* `parse_obj` expects a dictionary, so other Python types cannot be used in this method

The same temperature data exists in `my-data.yaml`, but it is a list of data points. Let's try this out...


```python
fpath_temperature_data_yaml = Path.cwd() / "my-data.yaml"
raw_temperature_data = yaml.safe_load(fpath_temperature_data_yaml.read_text())
temperature_data = TemperatureData.parse_obj(
    {"data": raw_temperature_data},
)

print("Deserialized data as a Pydantic model instance:")
display(temperature_data)
```

    Deserialized data as a Pydantic model instance:



    TemperatureData(data=[TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(0, 0), temperature=18.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(1, 0), temperature=18.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(2, 0), temperature=17.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(3, 0), temperature=17.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(4, 0), temperature=16.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(5, 0), temperature=16.5), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(6, 0), temperature=16.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(7, 0), temperature=16.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(8, 0), temperature=17.2), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(9, 0), temperature=18.8), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(10, 0), temperature=20.4), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(11, 0), temperature=21.9), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(12, 0), temperature=23.1), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(13, 0), temperature=24.0), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(14, 0), temperature=24.3), TemperatureSample(date=datetime.date(2023, 6, 1), time=datetime.time(15, 0), temperature=23.8)])


Now let's try serializing this data. Pydantic models have the `dict` and `json` methods to serialize to dictionaries and JSON strings, respectively. But first let's reduce the dataset to the first 3 entries so we dont flood our screen with a long list of data.


```python
shortened_temperature_data = TemperatureData(data=temperature_data.data[:3])
```

Now let's serialize the shortened dataset to a JSON string...


```python
print(shortened_temperature_data.json(indent=2))
```

    {
      "data": [
        {
          "date": "2023-06-01",
          "time": "00:00:00",
          "temperature": 18.5
        },
        {
          "date": "2023-06-01",
          "time": "01:00:00",
          "temperature": 18.2
        },
        {
          "date": "2023-06-01",
          "time": "02:00:00",
          "temperature": 17.8
        }
      ]
    }


Once we have the serialized string, we could send the string to an API endpoint or write to disk. Now let's serialize to a Python dictionary...


```python
shortened_temperature_data.dict()
```




    {'data': [{'date': datetime.date(2023, 6, 1),
       'time': datetime.time(0, 0),
       'temperature': 18.5},
      {'date': datetime.date(2023, 6, 1),
       'time': datetime.time(1, 0),
       'temperature': 18.2},
      {'date': datetime.date(2023, 6, 1),
       'time': datetime.time(2, 0),
       'temperature': 17.8}]}



Once again, we can then do with the serialized object as we please. For example, if we wanted to write to a TOML file, we could pass the serialized object into `toml.dump`.

## Serialization of custom types

What if we want to serialize a custom data type. Let's return to the `Point` class from Part-2-Basic-Usage...


```python
class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def distance_to(self, other: "Point") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5
```

If we build a Pydantic model that uses this class as a type hint, we won't be able to serialize using the `json` method...


```python
class LineSegment(BaseModel):
    p1: Point
    p2: Point

    class Config:
        arbitrary_types_allowed = True


line_segment = LineSegment(
    p1=Point(x=1, y=3),
    p2=Point(x=8, y=2),
)

line_segment.json()
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    Cell In[14], line 14
          6         arbitrary_types_allowed = True
          9 line_segment = LineSegment(
         10     p1=Point(x=1, y=3),
         11     p2=Point(x=8, y=2),
         12 )
    ---> 14 line_segment.json()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:504, in pydantic.main.BaseModel.json()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/json/__init__.py:234, in dumps(obj, skipkeys, ensure_ascii, check_circular, allow_nan, cls, indent, separators, default, sort_keys, **kw)
        232 if cls is None:
        233     cls = JSONEncoder
    --> 234 return cls(
        235     skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        236     check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        237     separators=separators, default=default, sort_keys=sort_keys,
        238     **kw).encode(obj)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/json/encoder.py:199, in JSONEncoder.encode(self, o)
        195         return encode_basestring(o)
        196 # This doesn't pass the iterator directly to ''.join() because the
        197 # exceptions aren't as detailed.  The list call should be roughly
        198 # equivalent to the PySequence_Fast that ''.join() would do.
    --> 199 chunks = self.iterencode(o, _one_shot=True)
        200 if not isinstance(chunks, (list, tuple)):
        201     chunks = list(chunks)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/json/encoder.py:257, in JSONEncoder.iterencode(self, o, _one_shot)
        252 else:
        253     _iterencode = _make_iterencode(
        254         markers, self.default, _encoder, self.indent, floatstr,
        255         self.key_separator, self.item_separator, self.sort_keys,
        256         self.skipkeys, _one_shot)
    --> 257 return _iterencode(o, 0)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/json.py:90, in pydantic.json.pydantic_encoder()


    TypeError: Object of type 'Point' is not JSON serializable


We get an error message informing us the `Point` is not JSON serializable. We can fix this using the `json_encoders` attribute of the `Config` class. This attribute is a dictionary that maps field types to functions that serialize those types. So we can modify the `Point` class to include an instance method that will serialize the data in the `Point` instance...


```python
class SerializablePoint(Point):
    def serialize(self) -> dict[str, Any]:
        return {"x": self.x, "y": self.y}
```

Then we can modify our `LineSegment` model to include this JSON encoder...


```python
class LineSegment(BaseModel):
    p1: SerializablePoint
    p2: SerializablePoint

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            SerializablePoint: SerializablePoint.serialize,
        }
```

Now we can serialize an instance of `LineSegment`...


```python
line_segment = LineSegment(
    p1=SerializablePoint(x=1, y=3),
    p2=SerializablePoint(x=8, y=2),
)

line_segment.json()
```




    '{"p1": {"x": 1, "y": 3}, "p2": {"x": 8, "y": 2}}'



We could have chosen to serialize `Point` in any number of reasonable ways. We chose to simply record the coordidates in a dictionary, but the possibilities are endless.

What if we want to deserialize data for `Point` fields. Currently, this will not work...


```python
line_segment_data = {"p1": {"x": 1, "y": 3}, "p2": {"x": 8, "y": 2}}

line_segment = LineSegment.parse_obj(line_segment_data)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[18], line 3
          1 line_segment_data = {"p1": {"x": 1, "y": 3}, "p2": {"x": 8, "y": 2}}
    ----> 3 line_segment = LineSegment.parse_obj(line_segment_data)


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:526, in pydantic.main.BaseModel.parse_obj()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 2 validation errors for LineSegment
    p1
      instance of SerializablePoint expected (type=type_error.arbitrary_type; expected_arbitrary_type=SerializablePoint)
    p2
      instance of SerializablePoint expected (type=type_error.arbitrary_type; expected_arbitrary_type=SerializablePoint)


We need to add validators to the `SerializablePoint` class definition...


```python
from pydantic.validators import float_validator


class DeserializablePoint(SerializablePoint):
    @classmethod
    def __get_validators__(cls):
        yield cls.deserialize

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> "DeserializablePoint":
        if ("x" not in data) or ("y" not in data):
            raise ValueError("Missing attributes x and/or y")

        x = float_validator(data["x"])
        y = float_validator(data["y"])

        return cls(x=data["x"], y=data["y"])
```

Now we have a `Point` class that is both serializable and deserializable...


```python
class LineSegment(BaseModel):
    p1: DeserializablePoint
    p2: DeserializablePoint

    class Config:
        json_encoders = {
            DeserializablePoint: DeserializablePoint.serialize,
        }


line_segment_data = {"p1": {"x": 1, "y": 3}, "p2": {"x": 8, "y": 2}}

line_segment = LineSegment.parse_obj(line_segment_data)
display(line_segment)

line_segment.json()
```


    LineSegment(p1=DeserializablePoint(x=1, y=3), p2=DeserializablePoint(x=8, y=2))





    '{"p1": {"x": 1, "y": 3}, "p2": {"x": 8, "y": 2}}'



For simplicity, I implemented our deserializer to assume the incoming data is a dictionary. A more flexible deserializer would require more logic.

## Include and exclude

Both `model.dict()` and `model.json()` have `include` and `exclude` parameters that specify which field to include or exclude when serializing model data. Other parameters exist as well, see [Exporting models](https://docs.pydantic.dev/latest/usage/exporting_models/).


```python
print(line_segment.json(indent=2, exclude={"p1"}))
```

    {
      "p2": {
        "x": 8,
        "y": 2
      }
    }


## `Config` related to serialization and deserialization

Certain attributes in the `Config` class relate to serialization and deserialization. A description of a select few are:
* `use_enum_values` - For `Enum` fields, the enumeration values will be used (as opposed to the Enum itself) when serializing with `model.dict()`.
* `arbitrary_types_allowed` - Setting this to `True` allows the use of arbitrary types for fields (i.e. classes that do not define the `__get_validators__` method. This could be useful is you want to use `PIL.Image.Image` as a field type for example.
* `json_loads` - A custom function for decoding JSON; see [custom JSON (de)serialisation](https://docs.pydantic.dev/latest/usage/exporting_models/#custom-json-deserialisation)
* `json_dumps` - A custom function for encoding JSON; see [custom JSON (de)serialisation](https://docs.pydantic.dev/latest/usage/exporting_models/#custom-json-deserialisation)
* `json_encoders` - A dict used to customise the way types are encoded to JSON; see [JSON Serialisation](https://docs.pydantic.dev/latest/usage/exporting_models/#modeljson)

## Exercise 5

Now let's build upon the previous exercise and compare this year's weather in Austin, TX to historical trends. The file located at `exercises_data/noaa_long_term_avgs.json` contains long-term daily averages and standard deviations of temperature data for Austin, TX (the airport weather station). This data was obtained from https://www.ncdc.noaa.gov/cdo-web/webservices/v2. You should examine the data and build a Pydantic model capable of parsing and validating this file (e.g. using `pydantic.BaseModel.parse_file`). Your model should also have methods to compute the upper and lower bounds of each daily average based on the standard deviations provided in the data.

Tasks:
* Extend and/or modify your script from Exercise 3 to parse this data file using the Pydantic model you created.
* Take the 2023 data obtained in Exercise 3 and compute daily averages with upper and lower bounds.
* Plot the two datasets on top of one another and compare this years temperature data to the long-term averages.
* Create yet another Pydantic model to combine the two datasets into one. The design of this structure is up to you, but it must be a Pydantic model.
* Serialize the combined dataset to disk (e.g. using `pydantic.BaseModel.dict` or `pydantic.BaseModel.json`).
