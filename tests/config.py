import sys

TESTSINPUTDIR = 'inputs'
TESTSOUTPUTDIR = 'outputs'

INPUTPATH = lambda filename: f'./{TESTSINPUTDIR}/{filename}'
# OUTPUTDIR = lambda: f'./{TESTSOUTPUTDIR}/{sys.argv[1][:-3]}/'
OUTPUTDIR = lambda arg: f'./{TESTSOUTPUTDIR}/{arg[:-3]}/'