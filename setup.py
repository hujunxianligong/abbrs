from distutils.core import setup
from Cython.Build import cythonize

# build task code to .so for example
setup(ext_modules=cythonize(["load/load_model.py","bin/term_tuple.py"]))
