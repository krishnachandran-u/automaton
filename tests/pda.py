from pykleene.pda import PDA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json

FILENAME = 'pdas.json'

if __name__ == '__main__':
    PDAs: Dict[str, PDA] = {}
    with open(INPUTPATH(FILENAME), 'r') as file:
        PDAs = json.load(file)

    for pdaName, pdaData in PDAs.items():
        pda = PDA()
        pda.loadFromJSONDict(pdaData)
        pda.image(dir=OUTPUTDIR(), save=True)
        print(pda.accepts('bbaba'))
        PDAs[pdaName] = pda