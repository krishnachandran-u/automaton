from pykleene.nfa import NFA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json

FILENAME = 'nfas.json'

if __name__ == '__main__':
    NFAs: Dict[str, NFA]
    with open(INPUTPATH(FILENAME), 'r') as file:
        NFAs = json.load(file)

    for nfaName, nfaData in NFAs.items():
        nfa = NFA()
        nfa.loadFromJSONDict(nfaData)
        # print(nfa.__dict__)
        nfa.image(dir=OUTPUTDIR(), save=True)
        NFAs[nfaName] = nfa 

    for nfaName, nfa in NFAs.items():
        nfa.image(dir=OUTPUTDIR(), save=True)
        dfa = nfa.dfa()
        dfa.image(dir=OUTPUTDIR(), save=True) 