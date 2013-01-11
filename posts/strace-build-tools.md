<!--
.. title: strace & build-tools
.. slug: strace-build-tools
.. date: 2013/01/11 05:00
.. tags: python, doit
-->

[strace](https://en.wikipedia.org/wiki/Strace) is a utility to monitor
system calls. I.e. it can report all files open by a process.

[fabricate.py](https://code.google.com/p/fabricate/)
is a build-tool based on strace.
The idea is pretty cool. It will execute all commands through strace.
Than it can automatically figure out the dependencie and targets
by looking at the strace output.
So you don't need to explicitly specifying the dependencies and targets.


But these approach has a few problems:

 * strace will slow down the execution

   (not only because of strace itself but also becaue it will have
    to parse strace output)

 * not always correct. i.e. `run('cp', '-r', 'src', 'out')`

   If you just add a file to the `src` it can not figure out that a "dependency"
   was added.

 * confuse targets & dependencies

   It checks the mode files were open, if open in write mode it is *target*.
   The problem is that some programs have their own cache system,
   so a target might be taken as a dependency.


Where these limitations are a problem or not depends on your use-case...

### doit & strace

[doit](http://pydoit.org/) takes a very different approach
to dependency handling.
All dependencies must be explicitly defined.

`doit` doesn't support any kind of implicit dependency
but it now comes with a `strace` command that lets you easily check
which files are being used.

The idea is that you can use this feature while developing your tasks
and make sure you are setting the dependencies correctly.

Example:

~~~~{.python}
def task_o():
    return {'actions': ['cp abc abc2', 'touch xyz']}
~~~~

~~~~{.python}
$ doit strace -f traceme.py o
.  o
.  strace_report
R /xxx/abc2
R /xxx/abc
W /xxx/abc2
W /xxx/xyz
~~~~

For more details check the [docs](http://pydoit.org/cmd_other.html#strace).
