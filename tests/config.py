import sys

TESTSINPUTDIR = 'inputs'
TESTSOUTPUTDIR = 'outputs'

INPUTPATH = lambda filename: f'./{TESTSINPUTDIR}/{filename}'
OUTPUTDIR = lambda: f'./{TESTSOUTPUTDIR}/{sys.argv[0][:-3]}/'