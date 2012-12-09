<!--
.. title: power up your tools
.. slug: power-up-your-tools
.. date: 2012/12/06 16:36:33
.. tags: python, doit
.. link: 
.. description: 
-->

Goal
------

[pyflakes](http://pypi.python.org/pypi/pyflakes>) is a static checker for python.
It is great but it lacks a few features:

 * no parallel multi-processing execution
 * no cache to avoid checking files that were not modified
 * no option to have a long running process that watches the file system
   and automatically re-executes the checker when files are modified

These features are not specific to a static checker and are nice to have
to many other tools.
This post shows how to create an application adding those features.
It uses pyflakes as an example but it could be applied to other tools also.


 static checker tasks
------------------------

[doit](http://pydoit.org) is an "automation tool" that can execute **tasks**
and provide the features which we are interested into. So the first step is to
transform pyflakes operations into **doit tasks**.

In *doit* a *task* is composed of **actions**, and some other **metadata**.

### actions

The *action* describes what the *task* does
(some code to be executed). It can be a python function...

For pyflakes the function `pyflakes.scripts.pyflakes.checkPath`
checks a file and returns the number of *flakes* or
warnings found, so it is successful when zero flakes were found.

The action's return value is used to indicate if the execution
was successful or not. So the action must return `True` if it has zero *flakes*

pyflakes checker action:

~~~~{.python}
from pyflakes.scripts.pyflakes import checkPath

def check_path(filename):
    return not bool(checkPath(filename))
~~~~

### dependencies

A **dependency** indicates something that is required for a task execution.

For the pyflakes task the file being checked is a *file dependency* for the task.
That is, the task can not be executed if the file is not present.

Explicit information of task dependencies are important for two factors:

1) cache results, if dependencies are not modified since last time the task
   was executed. It can use the results saved in a cache instead of re-executing
   the task.

2) execution order, when dealing with the execution of several tasks,
   the dependencies contains information on the order tasks should be executed
   and whether they can be executed simultaneously (in parallel).



task creation
-----------------

In *doit* usually task creation is done in a python module. Where you have
functions that return/yield new tasks as a dict with metadata.

Something like:

~~~~{.python}
import os
import glob

from pyflakes.scripts.pyflakes import checkPath


DOIT_CONFIG = {
    # output from actions should be sent to the console
    'verbosity': 2,
    # does not stop execution on first task failure
    'continue': True,
    # doit itself should not produce any output (use only actions output)
    'reporter': 'zero',
    # use multi-processing / parallel execution
    'num_process': 2,
    }


def check_path(filename):
    """execute pyflakes checker"""
    return not bool(checkPath(filename))

def task_pyflakes():
    """generate task for each file to be checked"""
    for filename in glob.glob('*.py'):
        path = os.path.abspath(filename)
        yield {
            'name': path, # name required to identify tasks
            'file_dep': [path], # file dependency
            'actions': [(check_path, (filename,)) ],
            }
~~~~

If you drop the content above in a file called *dodo.py* in a folder.
Executing `doit` from the command line you would execute pyflakes in
all python modules in that folder.

It already has multi-process support.
And it would execute only tasks that were failing or which checked
module file was changed.

To execute in a long running process that watched the file system and re-execute
tasks you could execute it as `doit auto`.


creating a new tool
----------------------

Creating tasks in *dodo.py* works fine if you are working on your own project.
But sometimes you just want to create a new application that you can easily
distribute to other users without requiring than to add any special file into their
project.

*doit* latest release (0.18) has exposed some of its internal API so you can
create new applications and still use its task execution model.

The idea is that instead of loading tasks from a *dodo.py* module,
the application itself create tasks and execute *doit*.

### custom task loader

To create a custom task loader you should subclass `doit.cmd_base.TaskLoader`
and implement the method `load_tasks`

*pyflakes* command line is extremely simple. It doesn't even support a `--help`
option. It only takes positional parameter that specify python modules or
folders containing python modules.

The first change from the previous example using *dodo.py* is to get
a list of files in the same way pyflakes does instead of just getting
all modules from a folder...

So on `__init__` the loader will find the list of files
to be checked.

~~~~{.python}
from doit.cmd_base import TaskLoader

class FlakeTaskLoader(TaskLoader):
    """create pyflakes tasks on the fly based on cmd-line arguments"""

    def __init__(self, args):
        """set list of files to be checked
        @param args (list - str) file/folder path to apply pyflakes
        """
        self.files = []
        for arg in args:
            if os.path.isdir(arg):
                for dirpath, dirnames, filenames in os.walk(arg):
                    for filename in filenames:
                        if filename.endswith('.py'):
                            self.files.append(os.path.join(dirpath, filename))
            else:
                self.files.append(arg)

        for path in self.files:
            if not os.path.exists(path):
                sys.stderr.write('%s: No such file or directory\n' % path)
~~~~


Than we need to change the function generating tasks to use the computed files.

~~~~{.python}
    @staticmethod
    def check_path(filename):
        """execute pyflakes checker"""
        return not bool(checkPath(filename))

    def _gen_tasks(self):
        """generate doit tasks for each file to be checked"""
        for filename in self.files:
            path = os.path.abspath(filename)
            yield {
                'name': path,
                'file_dep': [path],
                'actions': [(self.check_path, (filename,))],
                }
~~~~


Usually *doit* creates a file named `.doit.db` to store some information
that will be used to determine which tasks are up-to-date. This file is
created in the same location path as the *dodo.py* file. Since our new
application works independent from the current path we specify the
*store* file (`dep_file`) to be saved in the user's directory.

~~~~{.python}
    DOIT_CONFIG = {
        'verbosity': 2,
        'continue': True,
        'reporter': 'zero',
        'dep_file': os.path.join(os.path.expanduser("~"), '.doflakes'),
        'num_process': 2,
        }
~~~~

And finally we implement the `TaskLoader` interface:

~~~~{.python}
    def load_tasks(self, cmd, params, args):
        """implements loader interface, return (tasks, config)"""
        return generate_tasks('pyflakes', self._gen_tasks()), self.DOIT_CONFIG
~~~~


We also need to add a `-w` command line option to use the *watch* mode where
the process keeps waiting for modifications in the file system.

~~~~{.python}
from doit.doit_cmd import DoitMain

if __name__ == "__main__":
    cmd = 'run' # default doit command
    args = [] # list of positional args from cmd line
    for arg in sys.argv[1:]:
        if arg == '-w': # watch for changes
            cmd = 'auto'
        else:
            args.append(arg)
    doit_main = DoitMain(FlakeTaskLoader(args))
    sys.exit(doit_main.run([cmd]))
~~~~

The full code can be found here [doflakes.py](https://bitbucket.org/schettino72/doit-recipes/src/tip/doflakes/doflakes.py) .


power up your tools!
----------------------

Using *doit* you can easily add some nice features to external tools
or leverage its power in the tools you are the author!

*doit* has a very flexible dependency system that can be used to perform
tasks much more complex than simple static checkers.

For more information check [doit website](http://pydoit.org).
