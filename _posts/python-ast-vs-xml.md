<!--
.. title: python AST vs XML
.. slug: ast-vs-xml
.. date: 2014-09-16 09:46:57 UTC+08:00
.. tags: python, pyRegurgitator
.. link:
.. type: text
-->

One of the things that I really like in python is its introspection
capabilities. It goes as far as exposing its own syntax tree with
the [ast](https://docs.python.org/3/library/ast.html) module.

AST
=====

The `ast` module is usually used to do progammatically analysis,
generation, refactoring/transformation of python code. But is it
the right tool for the job?

API
-----

The `ast` provides a very simple API with `NodeVisitor` subclasses being
called for every node in the tree. It also provides a similar
`NodeTransformer` to modify nodes in-place. This API feels a lot like
[SAX](https://en.wikipedia.org/wiki/Simple_API_for_XML)
(Simple API for XML), an event sequential access parser API.

SAX style is simple, efficient and very useful in some situations,
but not very powerful compared to DOM or other API's that support XPath.
XPath is a very expressive query language for selecting nodes.
In python there are several libraries that support it (on stdlib,
[lxml](http://lxml.de/), ...)


Comments and Formatting
-------------------------

The `ast` throws away every information that is not important for the compiler,
like code comments and formatting (white-space, new-lines, etc).
This makes it very hard to modify existing code without messing up
with other parts of the original source code.


The node tree
---------------

The AST tree is designed to be used by the compiler.
It might no be optional for other uses...


py2xml
=========

[py2xml](http://pythonhosted.org/pyRegurgitator/#py2xml-experimental) is
a tool to covert python code into XML. It is already good enough to do
lose-less (preserve formatting and comments) round-trip conversion of
python to XML and back to python.

py2xml is still WIP (work in progress). The next step is to define a
XML structure to make it easy for querying and transforming source code.
Development is going on [github](https://github.com/schettino72/pyRegurgitator).

