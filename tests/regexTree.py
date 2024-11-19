from typing import Dict
from config import INPUTPATH, OUTPUTDIR
from pykleene.re import RE
from pykleene._helpers import BinaryTreeNode
import json

FILENAME = 'regexes.json'

if __name__ == '__main__':
    regexes: Dict[str, str]
    with open(INPUTPATH(FILENAME), 'r') as file:
        regexes = json.load(file)

    for regexName, regex in regexes.items():
        print(f"Regex for {regexName}: {regex}")
        formattedRegex = RE.format(regex)
        print(f"Formatted regex for {regexName}: {formattedRegex}")
        regexTree = RE.expressionTree(regex) 
        RE.image(param=regexTree, type='regexTree', dir=OUTPUTDIR(), save=True)
        