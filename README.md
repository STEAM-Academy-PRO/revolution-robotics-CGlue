CGlue ![Python package](https://github.com/RevolutionRobotics/CGlue/workflows/Python%20package/badge.svg) [![codecov](https://codecov.io/gh/RevolutionRobotics/CGlue/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionRobotics/CGlue)
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

Create a new project
=============

`cglue --new-project ProjectName [--project=project_file.json] [--cleanup]`

This command will create a new CGlue project file and the default directories.
There is no makefile added to the project - you'll need to write your own
or use a script to generate based on the CGlue project file.

Create a new software component
=============

`cglue --new-component ComponentName [--cleanup]`

This will create a new folder in the `SwComponents` folder (by default), create an empty source and 
header file as well as a component configuration json.

Updating a software component
=============

After you edit a component configuration json, you may call the following command to re-generate
the header and source files:

`cglue --update-component ComponentName [--cleanup]`

Alternatively, if you want to update all components, call `cglue --update-all-components [--cleanup]`
