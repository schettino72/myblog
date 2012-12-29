<!--
.. title: python code coverage & multiprocessing
.. slug: python-code-coverage-multiprocessing
.. date: 2012/12/30 06:45
.. tags: python
-->


I wanted to get code [coverage](http://nedbatchelder.com/code/coverage)
for my python code that uses the [multiprocessing](http://docs.python.org/2.7/library/multiprocessing.html) module.

The default way of coverage [measuring in subprocess](http://nedbatchelder.com/code/coverage/subprocess.html)
is to set the python interpreter to turn on code coverage right on start-up.
But this technique won't work if the process being measured *forks*
(as it does in multiprocessing).
See [issue](https://bitbucket.org/ned/coveragepy/issue/117/enable-coverage-measurement-of-code-run-by).

I solved this by monkey-patching the multiprocess to programmatically
start the coverage.
Only the method `Process._bootstrap` needs to be monkey-patched.
It is just wrapped with some code to start the coverage and
save it when it is done.


~~~~{.python}

from multiprocessing import Process

def coverage_multiprocessing_process(): # pragma: no cover
    try:
        import coverage
    except:
        # give up monkey-patching if coverage not installed
        return

    from coverage.collector import Collector
    from coverage.control import coverage
    # detect if coverage was running in forked process
    if Collector._collectors:
        class Process_WithCoverage(Process):
            def _bootstrap(self):
                cov = coverage(data_suffix=True)
                cov.start()
                try:
                    return Process._bootstrap(self)
                finally:
                    cov.stop()
                    cov.save()
        return Process_WithCoverage

ProcessCoverage = coverage_multiprocessing_process()
if ProcessCoverage:
    Process = ProcessCoverage

~~~~


Note that the monkey-patch is only applied when the original process
was being covered.
This is done by checking if there are any `Collector`.

When running the `coverage` you need use the `parallel-mode` and
than combine the results before creating report:

~~~~{.shell}

$ coverage run --parallel-mode my_program.py
$ coverage combine
$ coverage report

~~~~