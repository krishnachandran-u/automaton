from pykleene.lba import LBA
from typing import Dict
from config import INPUTPATH, OUTPUTDIR
import json
from pprint import pprint

FILENAME = 'lbas.json'

if __name__ == '__main__':
    LBAs: Dict[str, LBA] = {}
    with open(INPUTPATH(FILENAME), 'r') as file:
        LBAs = json.load(file)
        # pprint(TMs)

    for lbaName, lbaData in LBAs.items():
        lba = LBA()
        lba.loadFromJSONDict(lbaData)
        lba.image(dir=OUTPUTDIR(), save=True)
        print(lba.accepts('1111#11111', verbose=False, tapeLenFunc=lambda x: x+10))