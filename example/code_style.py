# script to demo python code style
# not 100% scientific, refer to PEP for strict rules
# created by Fan Zhang



# NOTE: IMPORT
# 1. import always on the top of the script
# 2. first general packages then specific ones
# lastly private ones
# 3. one package per line
# 4. can import multiple sub-modules on one line
# 5. for commonly used packages can assign alias

# have them here to align with the style

import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, roc_auc_score

from private_package import hello_world
import private_package

hello_world()
private_package.hello_world()

# NOTE: (optional) user defined modules is by default location relevant to 
# where the python executable initiates


# NOTE: NAMING
# 1.
# 
# 
# 
# 
# 
# 
# 



# NOTE: SPACING
# 1. use 4 space for indentation
# 2. normal space for arithmatic equations
# 3. tight space for parameters or inside nested structures
# 4. no multiple commands on the same line
# 5. do not try to align space around multiple lines


def bar(x=233):
    if x >= 0:
        x = 250 + x
    print('bar = ',x) # freestyle inside the string, WYSIWYG

bar()


# 6. blank lines after structure, higher the structure level
# more blank lines there should be (e.g. after class, chunk of comments)

class Demo:
        """a demo class to admire the code style, not to understand the content
        """ 
        N = 123

        def __repr__(self):
                return str(self.N)


d = Demo()

d
type(d)

# NOTE: (optional) though d shows as numbered string it is of an arbitrary class


# 6. comments and codes cannot be longer than 72 characters
# consider to wrap to new line is your command is long

# ways to wrap code / comments

print('this is an looooooooooooooooooooooooooooooooooooooooooooooo'+
        'oooooooooooooooooooooooooooooooooooooooooooooog string')

print('''this is an looooooooooooooooooooooooooooooooooooooooooooooo
        oooooooooooooooooooooooooooooooooooooooooooooog string''')

foo = 1
foo = foo**2 + foo**3 + foo**4 + foo**5 + \
        foo**6
print(foo)

# 7. you don't need to wrap long hyperlinks both in code or comments
# source http://looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooglink.com



