from distutils.core import setup, Extension
module1 = Extension('Multi',
                    sources = ['multiWrapper.c'])

setup(name = 'Multi',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])