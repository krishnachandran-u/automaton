from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json
from pykleene.grammar import Grammar
from pprint import pprint

FILENAME = 'llgs.json'

if __name__ == '__main__':
    rlgs: Dict[str, str]
    with open(INPUTPATH(FILENAME), 'r') as file:
        rlgs  = json.load(file)

    for rlgName, rlg in rlgs.items():
        print(f"RLG for {rlgName}: {rlg}") 
        grammar = Grammar()     
        grammar.loadFromJSONDict(rlg)
        grammar = grammar.toRightLinear() 
        pprint(grammar.__dict__)

