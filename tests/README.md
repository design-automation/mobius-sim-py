For information anbout unit testing:
- https://docs.python.org/3/library/unittest.html

To run all the unit test:

 - Execute `run_tests.bat` in the project root

 To run just one testm change to the `tests` fiolder and run:

- `python -m unittest -v "test_graph"`

The `-m` flag in Python searches the sys.path for the named module and executes its contents as the __main__ module. When the `-m` flag is used with a command on the command-line interface, followed by a <module_name> (in this case `unittest`), it allows the module to be executed as an executable file.

The `-v` flag runs tests with more detail (higher verbosity). 

The `-p` flag specifies a pattern to match test files (test*.py default).
