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
-------------

To set up the required packages, run the following:

```shell
pip install -r requirements.txt
pip install -r requirements_tests.txt
```

Use `python setup.py test` to run the tests.

Create a new project
--------------------

`cglue --new-project ProjectName [--project=project_file.json] [--cleanup]`

This command will create a new CGlue project file and the default directories.
There is no makefile added to the project - you'll need to write your own
or use a script to generate based on the CGlue project file.

Create a new software component
-------------------------------

`cglue --new-component ComponentName [--cleanup]`

This will create a new folder in the `SwComponents` folder (by default), create an empty source and
header file as well as a component configuration json.

Updating a software component
-----------------------------

After you edit a component configuration json, you may call the following command to re-generate
the header and source files:

`cglue --update-component ComponentName [--cleanup]`

Alternatively, if you want to update all components, call `cglue --update-all-components [--cleanup]`

CGlue managed software architecture
-----------------------------------

A CGlue project consists of a set of generated components, and a generated runtime that connects
the components.

__This description is incomplete and CGlue
may implement features that are not described here__

### Components

Components are independent, isolated pieces of software, connected by the runtime via their ports
and runnables. Normally, they are singletons and use
static global memory to manage their state, but CGlue supports components with multiple instances,
in which case the runtime passes a pointer to the instance's state memory to the generated functions.

Each component has a `config.json` that describes the interface and properties of the component.
This file contains:

- the set of component dependencies
- versioning information
- the set of state variables if the component supports multiple instances.

This file also lists the `*.c` source files
that implement the component.

#### Ports

```json
"ports": {
   "<PortName>": {
      "port_type": "<PortType>",
      ... other properties specific to port type ...
   }
},
```

Each port has a name and a type. The current set of port types:

- Constant
- ConstantArray
- ReadValue
- ReadIndexedValue
- WriteData
- WriteIndexedData
- Event
- ServerCall
- AsyncServerCall

#### Runnables

Runnables are special ports that always provide some logic or procedure.

```json
"runnables": {
   "<RunnableName>": {
      "port_type": "<PortType>",
      "arguments": {
         "<ArgumentName>": {
            "data_type": "<DataType>",
            "direction": "<Direction>"
         }
      },
      "return_type": "<ReturnType>",
   }
   ...
}
```

Runnable types:

- Runnable (default, no need to specify): a normal function.
  Runnables can be connected to `Event`, `ServerCall` and `AsyncServerCall` ports, or they can be
  called by runtime callables. If an `AsyncServerCall` port calls a non-async runnable, the
  runnable's result will be immediately available.
- AsyncRunnable: A runnable backed by some state machine. Used to represent longer
  procedures that don't immediately complete. The runtime will periodically poll these runnables.
  `AsyncRunnable`s can be called by `AsyncServerCall` ports.

Argument directions:

- `in`
- `out`
- `inout`

Argument and return types can be any type that is visible to the component. This includes types
defined by the runtime and other components that are listed as a component's dependency (in the
`requires` section).

#### Example async runnable definition

```json
"runnables": {
   "MyAsyncRunnable": {
      "port_type": "AsyncRunnable",
      "arguments": {
         "double_this": {
            "data_type": "uint8_t",
            "direction": "in"
         }
      },
      "return_type": "uint8_t",
   }
}
```

### Runtime

The runtime is generated from a file called `project.json`. This file defines:

- global types
- the set of components in the project
- global includes and additional source files not managed by CGlue
- the top-level runnable functions that users have to call periodically
- and most importantly, the connections between the components

CGlue defines a number of different connections. Each connection needs two components, and a pair
of compatible provided and consumed ports.

#### Connecting ports

Only compatible ports can be connected. A provider port may have multiple consumer ports, depending
on the port type. Currently, CGlue may silently generate incorrect code for incorrect configuration.

```json
"port_connections": [
   {
      "provider": "<ProviderComponent>/<PortName>",
      "consumer": "<ConsumerComponent>/<PortName1>"
   }
]
```

```json
"port_connections": [
   {
      "provider": "<ProviderComponent>/<PortName>",
      "consumers": [
         "<ConsumerComponent>/<PortName1>",
         "<ConsumerComponent2>/<PortName2>",
      ]
   }
]
```

Provider ports:

- WriteData - supports multiple consumers
- WriteIndexedData - supports multiple consumers
- Constant - supports multiple consumers
- ConstantArray - supports multiple consumers
- Event - supports multiple consumers
- Runnable - does __not__ support multiple consumers

Consumer ports:

- Runnable - provider: Event
- ReadValue - provider: Contant, WriteData
- ReadIndexedValue - provider: ConstantArray, WriteIndexedData
- ServerCall - provider: Runnable
- AsyncServerCall - provider: Runnable, AsyncRunnable

#### Queues

WriteData and ReadData can be connected using FIFO queues. In this case the runtime will generate
the queue. This may be useful when the provider runs with a faster loop time than the consumer.

```json
{
      "provider": "<ProviderComponent>/<PortName>",
      "consumer": "<ConsumerComponent>/<PortName1>",
      "queue_length": 32
},
```
