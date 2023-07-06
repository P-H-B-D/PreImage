import os
import sys
from math import sqrt

from urllib.request import urlopen
from flask import Flask, render_template
from testdependency import addtwo


def main():
    print("Hello, world!")
    print(addtwo(2, 3)) 

if __name__ == "__main__":
    main()