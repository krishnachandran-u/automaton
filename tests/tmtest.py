from pykleene.tm import TM
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json
from pprint import pprint

FILENAME = 'tms.json'

if __name__ == '__main__':
    TMs: Dict[str, TM] = {}
    with open(INPUTPATH(FILENAME), 'r') as file:
        TMs = json.load(file)
        # pprint(TMs)

    for tmName, tmData in TMs.items():
        tm = TM()
        tm.loadFromJSONDict(tmData)
        tm.image(dir=OUTPUTDIR(), save=True)
        print(tm.accepts('1111#11111', verbose=False))