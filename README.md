[![Build Status](https://travis-ci.org/neurobin/python-ocd.svg?branch=release)](https://travis-ci.org/neurobin/python-ocd)

Do you come from a C++ background? Are you very fond of the popular access modifiers such as `public`, `private`, `protected` etc? Do you worry that some of your python programs will be used by new pythonists and they will abuse your private variables?

Well, veteran pythonists will tell you, that, this behavior is over-obsessive and programmers in the python world are all adult people (which is true). In python, you don't usually worry about public or private, instead, you think of internal variables and follow a convention: use a single leading underscore for internal variables (e.g `_varname`) and two leading underscores if you want name mangling inside a class (e.g `__varname`). This does not make them protected or private, but python programmers will know whether they are internal, from the leading underscore.

Now, some people may still want to protect some of their variables from unknown changes, make them readonly, undeletable, etc. For example:

```python
class Defaults():
    STRONG = 2
    WEAK = 1
```

Let's say, some new python programmer is using this piece of code and passing `Defaults.WEAK` in some methods. Suddenly, he decides that, he will use `STRONG` instead of `WEAK` and instead of going through all occurrences of `Defaults.WEAK` usage, he does the laziest thing to do: he monkey patches the code:

```python
Defaults.WEAK = Defaults.STRONG
```

With this single line of code, his goal will be accomplished but it's going to be catastrophic if he is not careful (which he is obviously not). This guy may later go to your issue page and open an issue saying that some part of your code is not working as expected.

To mitigate this kind of scenario, your obsession might not be that bad of an idea. Now, introducing `ocd` aka <mark>Obsessive Coder's Day</mark> (made different from Obsessive Compulsive Disorder on purpose :D). Using `ocd` you can make your variables readonly, undeletable or both. They can be protected from class or class instances or both.

# Auto property creation

## Readonly property

```python
from ocd.prop import Prop
from ocd.mixins import PropMixin

class Defaults(PropMixin):
    STRONG = Prop(2, readonly=True)
    WEAK =  Prop(1, readonly=True)

# use is the same as before: Defaults.STRONG and Defaults.WEAK
```

This time, that monkey patch code will raise an exception:

```python
Defaults.WEAK = Defaults.STRONG # exception, readonly property value can not be changed.
```

The class attributes have been made into readonly properties, but they are still deletable, which exposes the following vulnerability:

```python
del Defaults.WEAK
Defaults.WEAK = Defaults.STRONG # now it's OK
```

and we have the following solution:

## Undead property

```python
class Defaults(PropMixin):
    STRONG = Prop(2, readonly=True, undead=True)
    WEAK =  Prop(1, readonly=True, undead=True)
```

You just need to say, it's an undead property. This time, the monkey patching will fail again:

```python
del Defaults.WEAK # exception, undead property can not be deleted
Defaults.WEAK = Defaults.STRONG
```

## More intuitive way to make readonly and undead properties

You may think that writing `Prop(2, readonly=True, undead=True)` and just `2` is a big difference and it is. So, we have a solution for this:

```python
from ocd import defaults

class Defaults(PropMixin):
    VarConf = defaults.VarConfAllUnro

    STRONG = 2
    WEAK =  1
```

Now, all the attributes that do not start with an underscore('_') will be converted to readonly, undead properties. This is because of `VarConf = defaults.VarConfAllUnro`. `VarConf` is a configuration class that needs to define a method `get_conf`. The above is roughly equivalent to:

```python
class Defaults(PropMixin):
    class VarConf(defaults.VarConfNone):
        def get_conf(self, name, value):
            return Prop(readonly=True, undead=True)

    STRONG = 2
    WEAK =  1
```

As you can see, the `get_conf` method has two parameters: name (property name) and value (value of the property), thus, you can decide which one will be what kind of property according to their names and values. You can match names/values with a pattern and make them readonly, match with another pattern and make them non-readonly, or match with another pattern to make them both readonly and undead, etc. You can return `None` for an attribute to not apply any property conversion on that specific attribute.

## Notes

* We do not allow variables starting with an underscores to be converted to property.
* Variables with leading underscore can store `Prop` class objects without getting converted to property.

# Other access obsessions

We have several classes to allow different level of obsessions over attribute access, for example:

1. Should the attribute be changeable through class or class instance or both?
2. Should the attribute be deletable through class or class instance or both?
3. Should the attributes be allowed to be accessed as items (e.g `obj['name']` instead of `obj.name`)?

You can check out these classes at [https://docs.neurobin.org/ocd/latest/unro.html](https://docs.neurobin.org/ocd/latest/unro.html)

# Other obsessions

## Deprecate in future

So, you want to deprecate a function or method from version 2.0 and remove it in 3.0 and the current version is 1.0! No problem, you can obsess on your deprecation plan too:

```python
from ocd.deprecate import deprecate

# If you do not specify the versions, it will be deprecated immediately
@deprecate(by='method2', ver_cur=package.__version__, ver_dep='2.0', ver_eol='3.0')
def method1(self):
    return self.method2()
```

When the version reaches 2.0, you will get a warning like this:

```
DeprecatedWarning: `<function method1 at 0x7faf2c362c10>` is deprecated by `method2` from version `2.0` and will be removed in version `3.0`. Current version: `1.0`.
```

and when the version reaches 3.0, you will get a warning like this:

```
UnsupportedWarning: `<function method1 at 0x7faf2c362c10>` was deprecated by `method2` from version `2.0` and planned to be removed in version `3.0`. Current version: `3.0`.
```

The unsupported warning is not that helpful, but you can raise this warning into error in your test suite and force yourself or your team to remove this deprecated method in the planned version. For that, you can use the `raiseUnsupportedWarning` decorator:

```python
from ocd.deprecate import raiseUnsupportedWarning

@raiseUnsupportedWarning
def test_method1(self):
    # your test code
    pass
```

You can find the detailed documentation at [https://docs.neurobin.org/ocd/latest/](https://docs.neurobin.org/ocd/latest/).

# Install

```bash
pip install ocd
```
