from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json
from pykleene.grammar import Grammar
from typing import Any

FILENAME = 'cfgs.json'

if __name__ == '__main__':
    CFGs: Dict[str, Any]
    with open(INPUTPATH(FILENAME), 'r') as file:
        CFGs  = json.load(file)

    for cfgName, cfg in CFGs.items():
        grammar = Grammar()
        grammar.loadFromJSONDict(cfg)
        if grammar.isRegular():
            print(f"CFG for {cfgName} is regular")
        if grammar.isContextFree():
            print(f"CFG for {cfgName} is context-free")
        if grammar.inCNF():
            print(f"CFG for {cfgName} is in Chomsky Normal Form")
        if grammar.inGNF():
            print(f"CFG for {cfgName} is in Greibach Normal Form")
        if grammar.isContextSensitive():
            print(f"CFG for {cfgName} is context-sensitive")