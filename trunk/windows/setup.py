###
##	py2exe generator EXE
###

#from distutils.core import setup
#import py2exe

#setup(console=['CSSMiami.py'])

from distutils.core import setup
import py2exe

setup(windows=[{"script":"CSSMiami.py"}], options={"py2exe":{"includes":["sip"]}})