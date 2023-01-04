To minifi the python, the following was used:

https://python-minifier.com/

To get the tests to work with the minified version, some modifications need to be made.
- `from sim_model import sim` to `from sim_model_mini import sim`
- `from sim_model import io_sim` to `# from sim_model import io_sim`