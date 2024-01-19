# Python - C++ Bindings

I work predominately in Python and C++, and find a lot of duplicated code
between the 2.

Python is useful for quickly getting setup and experimenting.

While C++ is what our production-level code is written in.

As a company, I don't see us choosing one over the other, so we're stuck in
this middle ground, with the bleeding edge in Python, and some trailing C++
following, but not quite matching.

A significant portion of work is often dedicated to just porting the Python to
C++. We've actually worked at making an automatic Python to C++ transpiler and
got it working quite well, it's not exactly what we want though. At some point
we'd like to "harden" interfaces, and leave them set in C++ and hopefully
remove the redundant python.

Note, that we do have a fairly robust Ipc framework setup that makes use of
protobufs for encoding data and calling RPCs, but in some cases we may not want
to deal with the overhead of an RPC / setting up all that boilerplate.

One way that might look is replacing Python methods, functions, classes with
thing wrappers that call the underlying C++. As you harden the leaf nodes, and
go up the tree, you can harden all underlying leafs. Ideally it'd be
straightforward to define these bindings. I know numpy has some c-bindings,
I've never used them myself; this is an experiment to determine the best/a good
way to do this.

I'd like to be able to switch over to replacing:
* constants
* functions
* classes / structs
* methods
* enums

Bonus points:
* functors / lambdas

## Investigation

I found [this link](https://realpython.com/python-bindings-overview/) and I'm
going to try it out.

Options:
- ctypes: stdlib, needs lots of type declarations
- cffi: automated, build system almost
- PyBind11: C++ based, generated from C++
- cython: write python-like code that compiles down to C/C++

others:
- pybindgen
- boost.python
- sip
- [CPPYY](https://cppyy.readthedocs.io/en/latest/)
- Swig
