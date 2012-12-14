<!--
.. title: doit task creation
.. slug: doit-task-creation
.. date: 2012/12/15 05:45:00
.. tags: python, doit
.. link: 
.. description: 
-->


On my previous [post](http://blog.schettino72.net/posts/doit-task-decorator.html)
I explained one way to create tasks for [doit](http://pydoit.org)
in a higher level than the default plain python dictionaries.

I just pushed a [change](https://bitbucket.org/schettino72/doit/commits/136e7fc9b1f779a22546a787ddb01048db74b264)
that will allow the creation of not only decorators to generate tasks but also
classes and instance objects.

The idea is very simple. Apart from collect functions that start with the
name `task_`. The *doit* loader will now also execute the `create_doit_task`
callable from any object that contains this attribute.

Note you will need the developement version of `doit` to run this code.

### decorator example


~~~~{.python}

##########################################################
## the decorator

def task(*args, **meta):
    def decorated(func):
        def create():
            task_dict = {'basename': func.__name__, 'actions': [func]}
            task_dict.update(meta)
            return task_dict
        func.create_doit_tasks = create
        return func

    if args:
        # decorator without parameters
        return decorated(args[0])
    else:
        return decorated


###########################################################
## task definition

DOIT_CONFIG = {'verbosity': 2}


@task
def simple():
    print "ho"

@task(file_dep=['dodo.py'])
def hello():
    print "hi"

~~~~

### class example

This interface was suggested by Thomas [here](https://groups.google.com/d/topic/python-doit/hp6wFvjcw1k/discussion).

~~~~{.python}

class Task(object):
    @classmethod
    def create_doit_tasks(cls):
        if cls is Task:
            return # avoid create tasks from base class 'Task'
        instance = cls()
        kw = dict((a, getattr(instance, a)) for a in dir(instance) if not a.startswith('_'))
        kw.pop('create_doit_tasks')
        if 'actions' not in kw:
            kw['actions'] = [kw.pop('run')]
        if 'doc' not in kw:
            kw['doc'] = cls.__doc__
        return kw



class hello(Task):
    """Hello from Python."""
    targets = ['hello.txt']

    def run(self):
        with open(self.targets[0], "a") as output:
            output.write("Hello world.")

class checker(Task):
    """Run pyflakes."""
    actions = ['pyflakes sample.py']
    file_dep = ['sample.py']

~~~~


### Object example

~~~~{.python}

class TaskHello(object):
    REG = [] # save instances

    def __init__(self, name):
        self.name = name
        self.REG.append(self)

    def say_hello(self):
        print "hello", self.name

    @classmethod
    def create_doit_tasks(cls):
        for inst in cls.REG:
            yield {
                'basename': inst.name,
                'actions': [inst.say_hello],
                }

######################

DOIT_CONFIG = {'verbosity': 2}

for name in ('foo', 'bar', 'spam'):
    TaskHello(name)

~~~~