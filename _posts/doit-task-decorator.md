<!--
.. title: doit task decorator
.. slug: doit-task-decorator
.. date: 2012/12/11 11:45:00
.. tags: python, doit
.. link: 
.. description: 
-->

[doit](http://pydoit.org) uses plain python dictionaries to define *tasks*.
Many, many people ask for a decorator based syntax. So here it is:

~~~~{.python}

##########################################################
## the decorator

def task(*args, **meta):
    """decorator to attach task metadata to a function
    decorated function will become the task's action
    """
    def make_task(func):
        func._doit_task = True
        func._doit_meta = meta
        return func

    if args:
        # decorator without parameters
        return make_task(args[0])
    else:
        # decorator with task metadata
        return make_task


###########################################################
## task definition

DOIT_CONFIG = {'verbosity': 2}


@task
def simple():
    print "ho"

@task(file_dep=['dodo.py'])
def hello():
    print "hi"




############################################################
### boilerplate - convert decorated stuff to default doit style tasks

def task_all():
    for name, obj in globals().iteritems():
        if getattr(obj, '_doit_task', False):
            task_dict = {'basename': name, 'actions': [obj]}
            task_dict.update(obj._doit_meta)
            yield task_dict
~~~~

Note that this will work with any version of *doit* there is no need
to have any modification in *doit* internal code.

*doit* is a generic tool that aims to by different kinds of applications.
There is no **one** task definition interface that will make everyone happy.
*doit* provides the most basic and flexible one based on dicts...

I must agree that this decorator interface looks more readable :)
But it has many limitations and can be used only for trivial tasks.

Limitations:

 * only one action per task
 * no support for command line (shell) actions
 * not easy to create several tasks with same actions

You could go one step further and create a
[custom task loader](http://python-doit.sourceforge.net/extending.html),
so you could get rid of the `task_all`.
I might add something like this for next *doit* release...