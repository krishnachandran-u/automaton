from pykleene.dfa import DFA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json

FILENAME = 'dfas.json'

if __name__ == '__main__':
    DFAs: Dict[str, DFA]
    with open(INPUTPATH(FILENAME), 'r') as file:
        DFAs = json.load(file)

    for dfaName, dfaData in DFAs.items():
        dfa = DFA()
        dfa.loadFromJSONDict(dfaData)
        dfa.image(dir=OUTPUTDIR(), save=True)
        DFAs[dfaName] = dfa

    for dfaName1, dfa1 in DFAs.items():
        for dfaName2, dfa2 in DFAs.items():
            if dfaName1 != dfaName2:
                if dfa1.isomorphic(dfa2):
                    print(f"{dfaName1} is equivalent to {dfaName2}")
                else:
                    print(f"{dfaName1} is not equivalent to {dfaName2}")