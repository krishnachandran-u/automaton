from pykleene.dfa import DFA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json

FILENAME = 'dfas.json'
NEWOUTPUTDIR = lambda x: f"{OUTPUTDIR()}{x}/"

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
        print(f"Complement of {dfaName1} is:")
        dfa1.complement().image(dir=NEWOUTPUTDIR(f"complement/{dfaName1}"), save=True)
        for dfaName2, dfa2 in DFAs.items():
            print(f"Intersection of {dfaName1} and {dfaName2} is:")
            dfa1.intersection(dfa2).image(dir=NEWOUTPUTDIR(f"intersection/{dfaName1 + dfaName2}"), save=True)
            print(f"Union of {dfaName1} and {dfaName2} is:")
            dfa1.union(dfa2).image(dir=NEWOUTPUTDIR(f"union/{dfaName1 + dfaName2}"), save=True)
            print(f"Difference of {dfaName1} and {dfaName2} is:")
            dfa1.difference(dfa2).image(dir=NEWOUTPUTDIR(f"difference/{dfaName1 + dfaName2}"), save=True)
            print(f"Symmetric Difference of {dfaName1} and {dfaName2} is:")
            dfa1.symmetricDifference(dfa2).image(dir=NEWOUTPUTDIR(f"symmetricDifference/{dfaName1 + dfaName2}"), save=True)