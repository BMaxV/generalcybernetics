import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "generalcybernetics",
    version = "0.1",
    author = "Me",
    author_email = "bruno.m.voss@gmail.com",
    description = ("various scripts that should help with cybernetics"),
    
    license = "I don't license this. If you have it, delete it.",
    keywords = "cyber",
   
    packages=['generalcybernetics'],#this will be the importname
    #long_description=read('README'),
 #   classifiers=[
 #       "Development Status :: 3 - Alpha",
 #       "Topic :: Utilities",
 #       "License :: OSI Approved :: BSD License",
 #   ],
)
