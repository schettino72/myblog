<!--
.. title: Merging dicts using singledispatch
.. slug: python-mergedict-singledispatch
.. date: 2013/12/15 00:00
.. tags: python
-->


I am working on some code that reads config values from different sources.
I would like to merge them in a way that values that are themselves dicts
get the items from both sources, something like:

~~~{.python}
source_1 = {'foo': 10, 'options': {'a':1, 'b':1}
source_2 = {'foo': 20, 'options': {'a':2, 'c':3}

# merging source_1 and source_2 would give me:
{'foo': 20, 'options': {'a':2, 'b':1, 'c':3}
~~~

Notice how this is different from a simple dict.update()
because `options` contains an item 'b'.
Apart from that I would like list to be merged, that is
merging `[1, 2]` and `[3, 4]` would result in `[1 ,2, 3, 4]`.

I found some implementations but it seems that everybody has a
different use-case for what "merge" should exactly do.
So I decided to create a `MergeDict` that can be easily extended/configured.


singledispatch
-----------------

The merge operation is specific depending on the type of the item.
That makes a perfect opportunity to use `singledispatch`.
Python 3.4 added support for single dispatch (see [PEP 443](http://www.python.org/dev/peps/pep-0443/)). I am not using python 3.4 yet but there is also a [package on pypi](https://pypi.python.org/pypi/singledispatch).

A single-dispatch is form of generic programming where you register
different functions to be executed depending on the type of the first argument.


Here is a simple example:

~~~{.python}
from singledispatch import singledispatch

# the function to be executed by default gets a singledispatch decorator
@singledispatch
def fun(arg):
    print("default: {}".format(arg))

# register alternate function when argument is an int
@fun.register(int)
def _(arg):
    print("int: {}".format(arg))

# register alternate function when argument is a list
@fun.register(list)
def _(arg):
    print("list: {}".format(" ".join(str(a) for a in arg)))


fun('hi')
# default: hi

fun(1)
# int: 1

fun([1,2,3])
# list: 1 2 3

~~~


MergeDict
------------

A `MergeDict` defines a `merge()` method.
Each item is merged using the `merge_value()` function,
by default it works the same as `update()` just replacing
the value...


~~~{.python}
class MergeDict(dict):

    def merge(self, other):
        """merge other dict into self"""
        class Sentinel: pass
        for key, other_value in other.items():
            this_value = self.get(key, Sentinel)
            if this_value is Sentinel:
                self[key] = other_value
            else:
                self[key] = self.merge_value(this_value, other_value)

    @staticmethod
    def merge_value(this, other):
        """default merge operation, just replace the value"""
        return other
~~~

Applying `singledispatch` to class methods is a bit tricky,
but ideally users would sub-class from `MergeDict` and define new
`merge()` methods with a decorator similar to singledispatch.

The idea is to just annotate the methods but really register the dispatch
only on object initialization.

~~~{.python}

class MergeDict(dict):

    def __init__(self, *args, **kwargs):
        super(MergeDict, self).__init__(*args, **kwargs)
        # register singlesingle dispatch methods
        self.merge_value = singledispatch(self.merge_value)
        for val in self.__class__.__dict__.values():
            _type = getattr(val, 'merge_dispatch', None)
            if _type:
                self.merge_value.register(_type, val)


    class dispatch:
        """decorator to mark methods as single dispatch functions."""
        def __init__(self, _type):
            self._type = _type
        def __call__(self, func):
            func.merge_dispatch = self._type
            return func
~~~

An example of a merge that sum up `int` values:

~~~{.python}
from mergedict import MergeDict

class SumDict(MergeDict):

    @MergeDict.dispatch(int)
    def merge_int(this, other):
        return this + other

a = SumDict({'a':2, 'b':3})
a.merge({'a':2, 'c':5})
print(a)
# {'a':4, 'b':3, 'c':5}
~~~

TL;DR;
-------

Check `mergedict` on [pypi](https://pypi.python.org/pypi/mergedict).
