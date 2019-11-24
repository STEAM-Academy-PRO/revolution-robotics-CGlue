CGlue
=====

__CGlue is in its early stages of development. It is not recommended for use in
production software and every part can change significantly.__

CGlue is a software framework for project written in C. It defines a component-based
architecture and provides tools to support this architecture.

A CGlue project has two main layers:
 - a component layer where you define the boundaries (ports, public types) of your software
   components
 - and a runtime layer where you define connections between your components

CGlue is capable of generating the skeleton structure of software components
and the implementation of the runtime layer.

CGlue provides plugin based extensibility.

CGlue requires python 3.x (TODO check minimum python version) and chevron.

Got any issues or suggestions? Head on to the issues page and open a ticket!

Running tests
=============

To set up the required packages, run the following:

```
pip install -r requirements.txt
pip install -r requirements_tests.txt
```

Use `python setup.py test` to run the tests.
