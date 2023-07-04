# 3. Advanced Usage II

**Concepts:**
- Type Validation
- `validator` decorator
- `root_validator` decorator
- Skipping validation
- `validate_arguments` decorator


## Type Validation

We saw a sneak peak of type validation in Part 2. Basic Usage. Now we are going to take a deep dive in type validation with Pydantic.

### `validator` decorator

If custom validation is required above and beyond what Pydantic provides out of the box, the `validator` decorator may be used to create validation class methods as part of the Pydantic model defintion. For example, imagine we want to create a model representing a user, with fields for the user's given name, surname, username, and passwords from two separate password creation inputs. We may want to impose the following restrictions:
1. Username must contain only ascii characters
1. Both provided passwords must be identical
1. Given name and surname must be alphabetic characters only and must start with a capital letter

We can accomplish this using the following model:


```python
from typing import Any
from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    password1: str
    password2: str
    given_name: str
    surname: str

    @validator("username")
    def username_must_be_ascii(cls, username: str) -> str:
        if not username.isascii():
            raise ValueError("must be alphanumeric")
        return username

    @validator("password2")
    def passwords_must_match(cls, password2: str, values: dict[str, Any]) -> str:
        if ("password1" in values) and (password2 != values["password1"]):
            raise ValueError("Passwords do not match")
        return password2

    @validator("given_name", "surname")
    def names_must_be_alphabetic(cls, name: str) -> str:
        if not name.isalpha():
            raise ValueError("must be alphabetic")
        return name.capitalize()
```

Now let's create a valid user and see what happens...


```python
display(
    User(
        username="scipy.2023.is.fun",
        password1="sup3rSecurePa$$w0rd",
        password2="sup3rSecurePa$$w0rd",
        given_name="joHn",
        surname="doe",
    )
)
```


    User(username='scipy.2023.is.fun', password1='sup3rSecurePa$$w0rd', password2='sup3rSecurePa$$w0rd', given_name='John', surname='Doe')


Notice that even though the provided name "joHn doe" was not properly capitalized, we were able to correct this by using the `str.capitalize` method and thus did not need to throw any errors. Now let's create an invalid user and see what happens...


```python
display(
    User(
        username="§cipy.2023.is.fun",
        password1="sup3rSecurePa$$w0rd",
        password2="sup3rSecurePa$$w0rd2",
        given_name="John Harry",
        surname="Doe-Smith",
    )
)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[3], line 2
          1 display(
    ----> 2     User(
          3         username="§cipy.2023.is.fun",
          4         password1="sup3rSecurePa$$w0rd",
          5         password2="sup3rSecurePa$$w0rd2",
          6         given_name="John Harry",
          7         surname="Doe-Smith",
          8     )
          9 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 4 validation errors for User
    username
      must be alphanumeric (type=value_error)
    password2
      Passwords do not match (type=value_error)
    given_name
      must be alphabetic (type=value_error)
    surname
      must be alphabetic (type=value_error)


Notice that Pydantic does not stop at the first validation error. It keeps track of all validation errors and gives a detailed summary of all validation errors in one error message. This allows the user to fix multiple problems at once instead of fixing a problem and then running into the next problem.

Some notes to keep in mind when using the `validator` decorator:
* The name of the validation method can be any valid Python name, but it helps to be descriptive
* The method will be a class method and not an instance method, so it is customary to name the first methd parameter `cls`
* The second method parameter will refer to the parsed value of the field under inspection and can be any valid Python name
* An optional third method parameter called `values` will refer to a dictionary of all previously parsed fields (fields are parsed in the order they are defined in the model)
  * If a field fails validation, it will not be present in the `values` dictionary in remaining validation methods
* The same method may be used to validate multiple fields by passing the name of each field as multiple arguments to the decorator
* Validation methods can perform additional parsing of fields on top of any parsing automatically provided by Pydantic
* Validation methods should either return the parsed value or raise one of `ValueError`, `TypeError`, or `AssertionError`

By default, `validator` will perform validation *after* other validation such as coercing `"5"` to an `int`. But we can create validation methods that operate *before* other validation by using `pre=True` in the `validator` keyword arguments.

`validator` also has an `each_item` keyword argument that will apply the method to each item of a list-like field.

Let's see `pre` and `each_item` in action...



```python
class Foo(BaseModel):
    positive_ints: list[int]

    @validator("positive_ints", pre=True)
    def split_comma_separated_values(cls, positive_ints: Any) -> Any:
        if isinstance(positive_ints, str):
            return positive_ints.split(",")
        return positive_ints

    @validator("positive_ints", each_item=True)
    def must_be_positive(cls, item: int) -> int:
        if item <= 0:
            raise ValueError(f"{item} is not positive")
        return item


display(
    Foo(positive_ints=(67.4, 2, True)),
)
display(
    Foo(positive_ints="2,4,6,8"),
)
display(
    Foo(positive_ints=["-4", 4, 0, 7]),
)
```


    Foo(positive_ints=[67, 2, 1])



    Foo(positive_ints=[2, 4, 6, 8])



    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[4], line 24
         17 display(
         18     Foo(positive_ints=(67.4, 2, True)),
         19 )
         20 display(
         21     Foo(positive_ints="2,4,6,8"),
         22 )
         23 display(
    ---> 24     Foo(positive_ints=["-4", 4, 0, 7]),
         25 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 2 validation errors for Foo
    positive_ints -> 0
      -4 is not positive (type=value_error)
    positive_ints -> 2
      0 is not positive (type=value_error)


Notice the first example successfully converted `(67.4, 2, True)` into the list of integers `[67, 2, 1]`. And thanks to `pre=True`, the second example converted `"2,4,6,8"` to `[2, 4, 6, 8]`. Had we set `pre=False` or left the default value, the string `"2,4,6,8"` would have led to a validation error. The third example returns a validation error as the input list contains non-positive integers. The error message even tells us which indices of the input list are leading to the validation error.

Another default behavior of `validator` is to not validate fields when a value is not provided. But there may be scenarios where this is not the desired behavior. Let's see an example. Let's return to our `User` class from above. Let's create a `NewUser` class which is the same as the `User` class but contains an additional `created_at` field. This will take an optional `datetime`. When not supplied, the default value should be the current UTC time. A naive implementation might look like:


```python
from datetime import datetime


class NewUser(User):
    created_at: datetime = datetime.utcnow()
```

But there is a problem with this implementation. The default time will represent the time the class was defined, not when it was instantiated...


```python
import time


class NewUser(User):
    created_at: datetime = datetime.utcnow()


print(f"NewUser class defined at:     {datetime.utcnow()}")

time.sleep(3)

new_user = NewUser(
    username="joe",
    password1="1234",
    password2="1234",
    given_name="joe",
    surname="davis",
)
print(f"new_user instance created at: {new_user.created_at}")
```

    NewUser class defined at:     2023-07-25 15:18:26.099273
    new_user instance created at: 2023-07-25 15:18:26.097606


Notice that despite occurring 3 seconds apart, the class definition and class instantiation are reporting as just milliseconds apart. We can solve this by creating a validation method where we set `always=True` in the `validator` keyword arguments. A correct implemention of this class looks like...


```python
from typing import Optional, Union


class NewUser(User):
    created_at: Optional[datetime]

    @validator("created_at", always=True)
    def set_default_time(cls, created_at: Union[datetime, None]) -> datetime:
        return datetime.utcnow() if created_at is None else created_at


print(f"NewUser class defined at:     {datetime.utcnow()}")

time.sleep(3)

new_user = NewUser(
    username="joe",
    password1="1234",
    password2="1234",
    given_name="joe",
    surname="davis",
)
print(f"new_user instance created at: {new_user.created_at}")
```

    NewUser class defined at:     2023-07-25 15:18:29.114991
    new_user instance created at: 2023-07-25 15:18:32.118412


Now we get the expected behavior that the `new_user` was created 3 seconds after the `NewUser` class was defined.

### `root_validator` decorator

It is possible to perform validation on the entire model data in one validation method using the `root_validator` decorator. Recall in our `User` class we validated that `password1` and `password2` matched using the `validator` decorator. The same functionality can be implemented with the `root_validator` decorator...


```python
from pydantic import root_validator


class UserPassword(BaseModel):
    password1: str
    password2: str

    @root_validator
    def passords_must_match(cls, values: dict[str, Any]) -> dict[str, Any]:
        pw1, pw2 = values.get("password1"), values.get("password2")
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("passwords do not match")
        return values


display(
    UserPassword(password1="1234", password2="1234"),
)
display(
    UserPassword(password1="1234", password2="12345"),
)
```


    UserPassword(password1='1234', password2='1234')



    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[8], line 20
         13         return values
         16 display(
         17     UserPassword(password1="1234", password2="1234"),
         18 )
         19 display(
    ---> 20     UserPassword(password1="1234", password2="12345"),
         21 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for UserPassword
    __root__
      passwords do not match (type=value_error)


Root validators also accept a `pre=True` keyword argument just like the `validator` decorator.

The full documentation on validators can be found at https://docs.pydantic.dev/latest/usage/validators/

### Skipping validation

Type validation can be a slow process that you may want to skip for performance reasons. If you know you have data from a trusted source that is pre-validated, then you may use the `construct` method of your Pydantic model when instantiating the class.


```python
user_data = {
    "username": "scipy.2023.is.fun",
    "password1": "1234",
    "password2": "1234",
    "given_name": "john",
    "surname": "doe",
}
```


```python
%%timeit
User(**user_data)
```

    16.5 µs ± 522 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)



```python
%%timeit
User.construct(**user_data)
```

    3.34 µs ± 100 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)


We can see that instatiating the `User` class with `construct` is much faster than with validation. But be mindful that skipping validation can result in invalid field values if the data is not pre-validated. Look what happens if we use the previous example that led to 4 validation errors...


```python
display(
    User.construct(
        username="§cipy.2023.is.fun",
        password1="sup3rSecurePa$$w0rd",
        password2="sup3rSecurePa$$w0rd2",
        given_name="John Harry",
        surname="Doe-Smith",
    )
)
```


    User(username='§cipy.2023.is.fun', password1='sup3rSecurePa$$w0rd', password2='sup3rSecurePa$$w0rd2', given_name='John Harry', surname='Doe-Smith')


As expected we see no validation error and the resulting `User` instance has several invalid values.

### `Config` type validation settings

Recall we can customize our Pydantic model by setting certain attributes in the `Config` class in our model. There are several settings related to type validation that can reduce the amount of validation methods needed.
* `anystr_strip_whitespace` - strip leading and trailing whitespaces for all `str` and `bytes` (default: `False`)
* `anystr_upper` - convert all characters to uppercase for `str` and `bytes` (default: `False`)
* `anystr_lower` - convert all characters to lowercase for `str` and `bytes` (default: `False`)
* `min_anystr_length` - minimum length for all `str` and `bytes` (default: `0`)
* `max_anystr_length` - maximum length for all `str` and `bytes` (default: `None`)
* `validate_all` - whether to validate fields when no value is provided (default: `False`)
* `validate_assignment` - whether to validate when fields are updated after instantiation (default: `False`)

Let's see some of these in action...


```python
class Foo(BaseModel):
    bar: str

    class Config:
        anystr_strip_whitespace = True
        anystr_upper = True
        min_anystr_length = 8
        max_anystr_length = 32
        validate_assignment = True


display(
    Foo(bar="   hello SciPy!      "),
)
```


    Foo(bar='HELLO SCIPY!')



```python
display(
    Foo(bar="    baz   "),
)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[14], line 2
          1 display(
    ----> 2     Foo(bar="    baz   "),
          3 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for Foo
    bar
      ensure this value has at least 8 characters (type=value_error.any_str.min_length; limit_value=8)


Notice that in this example the provided string has 10 characters, surpassing the 8 character minimum, but after stripping leading and trailing whitespaces, the string only has 3 characters. Thus a validation error arises exclaiming that `bar` is not at least 8 characters long.


```python
foo = Foo(bar="   hello SciPy!      ")
foo.bar = 80 * "-"
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[15], line 2
          1 foo = Foo(bar="   hello SciPy!      ")
    ----> 2 foo.bar = 80 * "-"


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:384, in pydantic.main.BaseModel.__setattr__()


    ValidationError: 1 validation error for Foo
    bar
      ensure this value has at most 32 characters (type=value_error.any_str.max_length; limit_value=32)


Here we try to change the value of `foo.bar` after instantiation, but we get a validation error exclaiming that the provided string is too long. Note that if `validate_assignment` were set to `False`, this would not have raised a validation error.

### `validate_arguments` decorator

Until now we have been discussing type validation in the context of Pydantic models, but Pydantic also provides a way to enforce function argument types at runtime via the `validate_arguments` decorator. This decorator will perform type coercion and type validation just like any Pydantic model.

Continuing our example with the `User` class, suppose a user wants to login to a service and we want to validate the provided credentials. We could write a function `validate_credentials` to compare a user provided username/password pair to a list of `User` instances. We may want to be sure the provided type are of the expected types.

**DISCLAIMER:** The following is **not** intended to be used as a model for sensitive date storage and/or credentials authentication. This example serves only to demonstrate the usage of the `validate_arguments` decorator.


```python
from pydantic import validate_arguments


def login():
    print("Successfully logged in!")


def logout():
    print("Invalid username or password")


@validate_arguments
def validate_credentials(
    username: str,
    password: str,
    registered_users: list[User],
) -> None:
    for user in registered_users:
        if (user.username == username) and (user.password1 == password):
            login()
            return

    logout()
```

Now let's create a database of users, but we will not create any `User` classes. Each user will just be a dictionary that conforms to the `User` model definition.


```python
registered_users = [
    {
        "username": "abc",
        "password1": "123",
        "password2": "123",
        "given_name": "Joe",
        "surname": "Smith",
    },
    {
        "username": "def",
        "password1": "321",
        "password2": "321",
        "given_name": "Jane",
        "surname": "Davidson",
    },
]
```

Now let's attempt to login in to the service...


```python
username, password = "def", "321"

validate_credentials(
    username=username,
    password=password,
    registered_users=registered_users,
)
```

    Successfully logged in!


We successfully logged in! But notice the magic that happened here. Our database of users is just a list of dictionaries. None of the users in our database have `username` or `password1` attributes, yet our `validate_credentials` function was able to access these attributes without raising an exception. Evidently the `validate_arguments` decorator coerced the list of dictionaries into a list of `User` instances. Presumably, if we then alter our database to include invalid users, then we should get a validation error when we try to call `validate_credentials`. Let's see if we are right...


```python
registered_users.append(
    {
        "username": "ghi",
        "password1": "pass",
        "password2": "different-pass",
        "given_name": "John",
        "surname": "Johnson",
    },
)

validate_credentials(
    username=username,
    password=password,
    registered_users=registered_users,
)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    Cell In[19], line 11
          1 registered_users.append(
          2     {
          3         "username": "ghi",
       (...)
          8     },
          9 )
    ---> 11 validate_credentials(
         12     username=username,
         13     password=password,
         14     registered_users=registered_users,
         15 )


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/decorator.py:40, in pydantic.decorator.validate_arguments.validate.wrapper_function()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/decorator.py:133, in pydantic.decorator.ValidatedFunction.call()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/decorator.py:130, in pydantic.decorator.ValidatedFunction.init_model_instance()


    File /opt/hostedtoolcache/Python/3.9.17/x64/lib/python3.9/site-packages/pydantic/main.py:341, in pydantic.main.BaseModel.__init__()


    ValidationError: 1 validation error for ValidateCredentials
    registered_users -> 2 -> password2
      Passwords do not match (type=value_error)


So even though we provided the same, valid username and password, the function did not complete and instead raised a validation error because it could not coerce the list of registered user dictionaries into a list of `User` instances.

The `validate_arguments` decorator can provide peace of mind when developing code, because you know the input arguments will have the specified type inside the function body. As with any validation, this does take time so the drawback is a decrease in performance. Though, in practice, this drop in speed is almost never important.

## Exercise 4

Now let's extend the script from the previous exercise with validation functionality, to make sure we work with valid data. 
Here are some things to consider:

- Are the time and temperature lists the same length?
- Are all temperatures above absolute zero?
- Are longitude and latitude values within the expected range?
- Any other meaningful validation you can think of


