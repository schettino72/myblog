<!--
.. title: github pull request workflow
.. slug: github-pull-request-workflow
.. date: 2013/07/22 10:00
.. tags: git
-->

A quick reference so I don't need to re-learn these steps every time
I do a pull-request...

* clone the repo in github

* clone the repo on your machine

~~~~{.shell}
git clone xxx
~~~~

* create a branch

~~~~{.shell}
git branch fix-something
~~~~

* use the branch
~~~~{.shell}
git checkout fix-something
~~~~

* hack something then commit
~~~~{.shell}
git commit -a
~~~~

* push new branch
~~~~{.shell}
git push origin fix-something
~~~~

* on github click `create pull request` (or something like that)

