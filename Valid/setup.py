from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('valid.pyx'))
# 进入这个目录，然后 python setup.py build_ext -i
