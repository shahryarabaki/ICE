#!/usr/bin/python3.5

from paver.easy import *
from paver.setuputils import setup
import paver.doctools
import os
import glob
import shutil

setup(
    name="CollocationExtractor",
    packages=['src'],
    version="0.5",
    url="http://www.uh.edu/",
    author="RedAs Lab UH",
    author_email="anqnguyen@outlook.com",
    install_requires=["nltk", 
    	"unidecode>=0.04.19"]
)

@task
@needs(['sdist'])
def install_dependencies():
	sh('pip install -r CollocationExtractor.egg-info/requires.txt')
	pass

@task
def test():
    sh('nosetests --with-coverage --cover-erase --cover-package=src --cover-html test')
    pass


@task
def clean():
    for pycfile in glob.glob("*/*.pyc"): os.remove(pycfile)
    for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
    for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
    for pycache in glob.glob("./__pycache__"): shutil.rmtree(pycache)
    pass


@task
@needs(['test', 'clean'])
def default():
    pass
