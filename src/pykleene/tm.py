from pykleene.symbols import Symbols

class TM:
    states: set[str]
    inputAlphabet: set[str]
    tapeAlphabet: set[str]
    startState: str
    transitions: dict[tuple[str, str], tuple[str, str, str]]
    leftEndMarker: str = Symbols.VDASH
    blankSymbol: str = Symbols.FLAT
    acceptState: str
    rejectState: str

    tapeLength: int = 1e5

    def _setNone(self) -> None:
        for key, _ in self.__annotations__.items():
            setattr(self, key, None)

    def isValid(self) -> bool:
        if self.startState: assert self.startState in self.states, f"Start state {self.startState} not in states"
        if self.acceptState: assert self.acceptState in self.states, f"Accept state {self.acceptState} not in states"
        if self.rejectState: assert self.rejectState in self.states, f"Reject state {self.rejectState} not in states"
        if self.leftEndMarker: assert self.leftEndMarker in self.tapeAlphabet, f"Left end marker {self.leftEndMarker} not in tape alphabet"
        if self.blankSymbol: assert self.blankSymbol in self.tapeAlphabet, f"Blank symbol {self.blankSymbol} not in tape alphabet"
        for (state, symbol), (nextState, writeSymbol, direction) in self.transitions.items():
            assert state in self.states, f"State {state} not in states"
            assert symbol in self.tapeAlphabet, f"Symbol {symbol} not in tape alphabet"
            assert nextState in self.states, f"Next state {nextState} not in states"
            assert writeSymbol in self.tapeAlphabet, f"Write symbol {writeSymbol} not in tape alphabet"
            assert direction in ['L', 'R', 'S'], f"Direction {direction} not in ['L', 'R', 'S']"
        return True

    def __init__(self, 
                 states: set[str] = set(), 
                 inputAlphabet: set[str] = set(), 
                 tapeAlphabet: set[str] = set(), 
                 startState: str = None,
                 transitions: dict[tuple[str, str], tuple[str, str, str]] = dict(),
                 acceptState: str = None,
                 rejectState: str = None) -> None:

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.tapeAlphabet = tapeAlphabet
        self.startState = startState
        self.transitions = transitions
        self.acceptState = acceptState
        self.rejectState = rejectState
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()

    def loadFromJSONDict(self, jsonDict: dict) -> None:
        self.states = set(jsonDict['states'])
        self.inputAlphabet = set(jsonDict['inputAlphabet'])
        self.tapeAlphabet = set(jsonDict['tapeAlphabet'])
        for [state, symbol, nextState, writeSymbol, direction] in jsonDict['transitions']:
            self.transitions[(state, symbol)] = (nextState, writeSymbol, direction)
        self.startState = jsonDict['startState']
        self.acceptState = jsonDict['acceptState']
        self.rejectState = jsonDict['rejectState']
        try:
            self.isValid()
        except AssertionError as e:
            print(e)
            self._setNone()